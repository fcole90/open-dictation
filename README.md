# Open Dictation

A simple, open-source dictation tool to convert speech to text.

## Requirements

- macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
or
- Windows: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`

uv can manage Python versions directly. To install Python 3.14 via uv: `uv python install 3.14`

## Installation

```sh
uv sync
```

After this step you may want to close and reopen your terminal or IDE to ensure that the uv-managed virtual environment is activated correctly.

## Usage

There are two main commands available:

### Recording

To record audio from your microphone:

```sh
uv run poe recorder
```

This will save the recording to a file.

### Speech-to-text

To transcribe an audio file to text:

```sh
uv run poe main <path_to_audio_file>
```

## Development

### Tests

```sh
uv run poe test
```

### Linting

```sh
uv run poe lint
```

### Typechecking

```sh
uv run poe typecheck
```
