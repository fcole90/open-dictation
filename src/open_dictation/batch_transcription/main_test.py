from pathlib import Path

from open_dictation.batch_transcription.main import (
    collect_media_files,
    format_timestamp,
    transcript_path,
)


def test_collect_media_files(tmp_path: Path):
    """Folders are searched recursively; unsupported files are dropped."""
    (tmp_path / "sub").mkdir()
    (tmp_path / "b.webm").touch()
    (tmp_path / "sub" / "a.OGG").touch()
    (tmp_path / "notes.txt").touch()
    single = tmp_path / "c.mp3"
    single.touch()

    files = collect_media_files(
        [tmp_path / "sub", tmp_path / "b.webm", single, tmp_path / "notes.txt"]
    )

    assert files == [tmp_path / "sub" / "a.OGG", tmp_path / "b.webm", single]


def test_transcript_path_mirrors_base(tmp_path: Path):
    source = tmp_path / "course" / "lectures" / "1-intro.webm"

    target = transcript_path(source, tmp_path / "course", tmp_path / "out", "it")

    assert target == tmp_path / "out" / "lectures" / "1-intro.transcript.it.md"


def test_transcript_path_outside_base_uses_file_name(tmp_path: Path):
    source = tmp_path / "elsewhere" / "note.ogg"

    target = transcript_path(source, tmp_path / "course", tmp_path / "out", "en")

    assert target == tmp_path / "out" / "note.transcript.en.md"


def test_format_timestamp():
    assert format_timestamp(0) == "00:00:00"
    assert format_timestamp(59.9) == "00:00:59"
    assert format_timestamp(3725.4) == "01:02:05"
