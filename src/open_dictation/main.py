import time
from open_dictation.recording.main import AudioRecorder
from open_dictation.speech_to_text.main import SpeechToText
from open_dictation.text_injection.main import TextInjector
from open_dictation.hotkey.main import HotkeyListener
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
        print("Recording started...")
        self.recorder.start()

    def _on_hotkey_release(self):
        print("Recording stopped...")
        audio_data = self.recorder.stop()
        if audio_data.size > 0:
            print("Transcribing...")
            text = self.stt.transcribe(audio_data.flatten())
            print(f"Transcribed: {text}")
            self.injector.inject(text)
        else:
            print("No audio recorded.")

    def start(self):
        print("Open Dictation started. Press and hold F4 to dictate.")
        self._running = True
        self.hotkey_listener.start()
        self.tray_icon.start()
        while self._running:
            time.sleep(1)

    def stop(self):
        print("Shutting down Open Dictation...")
        self._running = False
        self.hotkey_listener.stop()
        self.tray_icon.stop()


def main() -> None:
    app = OpenDictationApp()
    app.start()


if __name__ == "__main__":
    main()
