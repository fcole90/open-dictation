import time

from open_dictation.logger import logger
from open_dictation.hotkey.main import HotkeyListener
from open_dictation.recording.main import AudioRecorder
from open_dictation.speech_to_text.main import SpeechToText
from open_dictation.text_injection.main import TextInjector
from open_dictation.tray_icon.main import TrayIcon


class OpenDictationApp:
    def __init__(self):
        self.recorder = AudioRecorder()
        self.stt = SpeechToText()
        self.injector = TextInjector()
        self.hotkey_listener = HotkeyListener(
            on_press_callback=self._on_hotkey_press,
            on_release_callback=self._on_hotkey_release,
        )
        self.tray_icon = TrayIcon("Open Dictation", self.stop)
        self._running = False

    def _on_hotkey_press(self):
        logger.info("Recording started...")
        self.recorder.start()

    def _on_hotkey_release(self):
        logger.info("Recording stopped...")
        audio_data = self.recorder.stop()
        if audio_data.size > 0:
            logger.info("Transcribing...")
            text = self.stt.transcribe(audio_data.flatten())
            logger.info(f"Transcribed: {text}")
            self.injector.inject(text)
        else:
            logger.info("No audio recorded.")

    def start(self):
        logger.info("Open Dictation started.")
        self._running = True
        self.hotkey_listener.start()
        self.tray_icon.start()
        while self._running:
            time.sleep(1)

    def stop(self):
        logger.info("Shutting down Open Dictation...")
        self._running = False
        self.hotkey_listener.stop()
        self.tray_icon.stop()


def main() -> None:
    app = OpenDictationApp()
    app.start()


if __name__ == "__main__":
    main()
