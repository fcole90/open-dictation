import tempfile
from pathlib import Path

from pydantic_settings import SettingsConfigDict

from open_dictation.config import Settings


class TestSettingsDefaults:
    """Test that default values are correctly applied."""

    def test_default_hotkey(self):
        """Test that default hotkey is 'f4'."""
        settings = Settings()
        assert settings.HOTKEY == "f4"

    def test_default_model_size(self):
        """Test that default model size is 'base.en'."""
        settings = Settings()
        assert settings.MODEL_SIZE == "base.en"

    def test_default_compute_device(self):
        """Test that default compute device is 'cpu'."""
        settings = Settings()
        assert settings.COMPUTE_DEVICE == "cpu"


class TestSettingsEnvFileLoading:
    """Test loading settings from .env file."""

    def test_settings_from_env_file(self):
        """Test that settings are loaded from .env file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            env_file = Path(tmpdir) / ".env"
            env_file.write_text(
                "HOTKEY=shift+f5\nMODEL_SIZE=small\nCOMPUTE_DEVICE=cuda"
            )

            # Create a new Settings instance pointing to our temp .env file
            class TempSettings(Settings):
                model_config = SettingsConfigDict(
                    env_file=str(env_file),
                    env_file_encoding="utf-8",
                    extra="ignore",
                )

            settings = TempSettings()
            assert settings.HOTKEY == "shift+f5"
            assert settings.MODEL_SIZE == "small"
            assert settings.COMPUTE_DEVICE == "cuda"

    def test_settings_partial_env_file(self):
        """Test that missing env vars use defaults."""
        with tempfile.TemporaryDirectory() as tmpdir:
            env_file = Path(tmpdir) / ".env"
            env_file.write_text("HOTKEY=shift+f6")

            class TempSettings(Settings):
                model_config = SettingsConfigDict(
                    env_file=str(env_file),
                    env_file_encoding="utf-8",
                    extra="ignore",
                )

            settings = TempSettings()
            assert settings.HOTKEY == "shift+f6"
            assert settings.MODEL_SIZE == "base.en"  # default
            assert settings.COMPUTE_DEVICE == "cpu"  # default


class TestSettingsValidation:
    """Test settings validation and edge cases."""

    def test_settings_ignores_extra_fields(self):
        """Test that extra fields in .env are ignored."""
        with tempfile.TemporaryDirectory() as tmpdir:
            env_file = Path(tmpdir) / ".env"
            env_file.write_text("HOTKEY=f4\nEXTRA_FIELD=value\nANOTHER_FIELD=123")

            class TempSettings(Settings):
                model_config = SettingsConfigDict(
                    env_file=str(env_file),
                    env_file_encoding="utf-8",
                    extra="ignore",
                )

            settings = TempSettings()
            assert settings.HOTKEY == "f4"
            assert not hasattr(settings, "EXTRA_FIELD")
            assert not hasattr(settings, "ANOTHER_FIELD")

    def test_settings_string_values(self):
        """Test that settings are stored as strings."""
        settings = Settings()
        assert isinstance(settings.HOTKEY, str)
        assert isinstance(settings.MODEL_SIZE, str)
        assert isinstance(settings.COMPUTE_DEVICE, str)

    def test_settings_valid_model_sizes(self):
        """Test that valid model sizes can be set."""
        valid_sizes = ["tiny", "base", "small", "medium", "large"]
        for size in valid_sizes:
            with tempfile.TemporaryDirectory() as tmpdir:
                env_file = Path(tmpdir) / ".env"
                env_file.write_text(f"MODEL_SIZE={size}")

                class TempSettings(Settings):
                    model_config = SettingsConfigDict(
                        env_file=str(env_file),
                        env_file_encoding="utf-8",
                        extra="ignore",
                    )

                settings = TempSettings()
                assert settings.MODEL_SIZE == size

    def test_settings_valid_compute_devices(self):
        """Test that valid compute devices can be set."""
        valid_devices = ["cpu", "cuda", "auto"]
        for device in valid_devices:
            with tempfile.TemporaryDirectory() as tmpdir:
                env_file = Path(tmpdir) / ".env"
                env_file.write_text(f"COMPUTE_DEVICE={device}")

                class TempSettings(Settings):
                    model_config = SettingsConfigDict(
                        env_file=str(env_file),
                        env_file_encoding="utf-8",
                        extra="ignore",
                    )

                settings = TempSettings()
                assert settings.COMPUTE_DEVICE == device
