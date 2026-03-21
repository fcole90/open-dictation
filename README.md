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

## Known Issues

### Failed install of `pywhispercpp`

You may be encountering a long path issue on Windows, this is a known issue.

#### Long Path Issue

When compiling `pywhispercpp` from source on Windows, the build process relies on CMake to fetch and compile external C++ dependencies. This generates a heavily nested directory structure (e.g., within `build/_deps/...`). By default, Windows enforces a legacy 260-character limit on file paths (`MAX_PATH`). When the build path exceeds this limit, the compiler cannot find or write the necessary files, resulting in cryptic `FileNotFoundError` exceptions or catastrophic C++ compiler crashes.

#### Long Path Workaround

You need to enable Long Path support in Windows to bypass the 260-character limit before compiling:

1. Open a **Windows PowerShell (Admin)**.
2. Execute the following command:

   ```powershell
   New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
   ```

3. `uv sync`

##### If you want to revert it

   ```powershell
   New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 0 -PropertyType DWORD -Force
   ```

#### Tracking This Issue

- <https://www.google.com/search?q=https://github.com/absadiki/pywhispercpp/issues/156&authuser=1>

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
