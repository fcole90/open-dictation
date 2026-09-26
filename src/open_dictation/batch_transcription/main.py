"""Batch-transcribe audio or video files into timestamped Markdown transcripts.

Unlike the live dictation loop, this reads files from disk, so it suits long recordings such as
lectures. Each input becomes `<out-dir>/<path relative to --base>.transcript.<language>.md`, with a
header and one `[hh:mm:ss] text` line per segment. Existing transcripts are skipped and each one is
written to a `.part` file first, so a run can be stopped and restarted without losing work.
"""

import argparse
import importlib.util
import json
import os
import sys
import time
from pathlib import Path

from faster_whisper import WhisperModel  # type: ignore

from open_dictation.logger import logger

MEDIA_SUFFIXES = {".webm", ".ogg", ".opus", ".mp3", ".m4a", ".wav", ".mp4", ".mkv"}
CUDA_LIBRARY_MODULES = ("nvidia.cublas.lib", "nvidia.cudnn.lib")
LIBRARIES_SET_FLAG = "_OPEN_DICTATION_CUDA_LIBS_SET"


def collect_media_files(inputs: list[Path]) -> list[Path]:
    """Expand folders recursively and keep only supported media files, in a stable order."""
    files: list[Path] = []
    for path in inputs:
        if path.is_dir():
            files += sorted(
                p for p in path.rglob("*") if p.suffix.lower() in MEDIA_SUFFIXES
            )
        elif path.suffix.lower() in MEDIA_SUFFIXES:
            files.append(path)
        else:
            logger.warning(f"Skipping unsupported input: {path}")
    return files


def transcript_path(source: Path, base: Path, out_dir: Path, language: str) -> Path:
    """Mirror the source's path under `base` into `out_dir`; fall back to its file name."""
    try:
        relative = source.resolve().relative_to(base.resolve())
    except ValueError:
        relative = Path(source.name)
    return out_dir / relative.parent / f"{relative.stem}.transcript.{language}.md"


def format_timestamp(seconds: float) -> str:
    whole = int(seconds)
    return f"{whole // 3600:02d}:{whole % 3600 // 60:02d}:{whole % 60:02d}"


def cuda_library_dirs() -> list[str]:
    """Folders of the pip-installed cuBLAS and cuDNN libraries (the `cuda` extra), if present."""
    dirs: list[str] = []
    for module in CUDA_LIBRARY_MODULES:
        spec = importlib.util.find_spec(module)
        if spec is not None and spec.submodule_search_locations:
            dirs += list(spec.submodule_search_locations)
    return dirs


def ensure_cuda_libraries():
    """Re-execute with the CUDA wheel libraries on LD_LIBRARY_PATH, which is only read at start."""
    if os.environ.get(LIBRARIES_SET_FLAG):
        return
    dirs = cuda_library_dirs()
    if not dirs:
        return
    env = dict(os.environ)
    current = env.get("LD_LIBRARY_PATH")
    env["LD_LIBRARY_PATH"] = ":".join(dirs + ([current] if current else []))
    env[LIBRARIES_SET_FLAG] = "1"
    os.execve(sys.executable, [sys.executable, *sys.argv], env)


def transcribe_file(
    model: WhisperModel, source: Path, target: Path, language: str, header: str
) -> float:
    """Write the transcript of `source` to `target` and return the audio duration in seconds."""
    segments, info = model.transcribe(
        str(source),
        language=language,
        beam_size=5,
        vad_filter=True,
        condition_on_previous_text=False,
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_name(target.name + ".part")
    with partial.open("w", encoding="utf-8") as out:
        out.write(f"<!-- source-audio: {source.name} -->\n")
        out.write(f"<!-- {header}, duration: {format_timestamp(info.duration)} -->\n\n")
        for segment in segments:
            out.write(f"[{format_timestamp(segment.start)}] {segment.text.strip()}\n")
            out.flush()
    partial.rename(target)
    return info.duration


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch-transcribe audio or video files into timestamped Markdown."
    )
    parser.add_argument("inputs", nargs="+", type=Path, help="files or folders")
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument(
        "--base",
        type=Path,
        default=Path.cwd(),
        help="input paths are mirrored under --out-dir relative to this folder",
    )
    parser.add_argument("--model", default="medium")
    parser.add_argument("--language", default="it")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--compute-type", default="int8_float16")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    files = collect_media_files(args.inputs)
    pending = [
        (source, target)
        for source in files
        if not (
            target := transcript_path(source, args.base, args.out_dir, args.language)
        ).exists()
    ]
    logger.info(
        f"{len(files)} files, {len(files) - len(pending)} done, {len(pending)} to do"
    )
    if args.dry_run:
        for source, target in pending:
            logger.info(f"{source} -> {target}")
        return

    if args.device == "cuda":
        ensure_cuda_libraries()
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    header = f"model: {args.model} ({args.compute_type}), language: {args.language}"
    failed: list[str] = []
    for index, (source, target) in enumerate(pending, 1):
        started = time.monotonic()
        logger.info(f"[{index}/{len(pending)}] {source}: start")
        try:
            duration = transcribe_file(model, source, target, args.language, header)
        except Exception as error:  # keep going; the file is retried on the next run
            failed.append(f"{source}: {error}")
            logger.error(f"[{index}/{len(pending)}] {source}: failed: {error}")
            continue
        minutes = (time.monotonic() - started) / 60
        logger.info(
            f"[{index}/{len(pending)}] {source}: done in {minutes:.1f} min "
            f"({format_timestamp(duration)} audio)"
        )
    print(json.dumps({"done": len(pending) - len(failed), "failed": failed}))
