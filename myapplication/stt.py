import time

import pyaudio
from loguru import logger
from RealtimeSTT import AudioToTextRecorder


class STT:
    def __init__(self, signals):
        self.recorder = None
        self.signals = signals
        self.API = self.API(self)
        self.enabled = True

    def text_detected(self, text):
        # logger.debug(text)
        pass

    def process_text(self, text):
        if not self.enabled:
            return

        logger.debug("STT OUTPUT: " + text)
        self.signals.history.append({"role": "user", "content": text})

        self.signals.last_message_time = time.time()
        if not self.signals.AI_speaking:
            self.signals.new_message = True

    def recording_start(self):
        self.signals.human_speaking = True

    def recording_stop(self):
        self.signals.human_speaking = False

    def feed_audio(self, data):
        self.recorder.feed_audio(data)

    def listen_loop(self):
        def find_input_device():
            pa = pyaudio.PyAudio()
            for device_index in range(pa.get_device_count()):
                dev = pa.get_device_info_by_index(device_index)
                logger.debug(f"Device: {dev}")
                if dev["name"].lower() in ["mic", "input"]:
                    logger.info(f"Listening from: {dev}")
                    return device_index + 1
            return None

        input_device = find_input_device()

        logger.debug(f"Input device: {input_device}")

        logger.debug("STT Starting")
        recorder_config = {
            "compute_type": "auto",
            "enable_realtime_transcription": True,
            "input_device_index": input_device,
            "language": "en",
            "min_gap_between_recordings": 0.2,
            "min_length_of_recording": 0,
            "on_realtime_transcription_update": self.text_detected,
            "on_recording_start": self.recording_start,
            "on_recording_stop": self.recording_stop,
            "post_speech_silence_duration": 0.4,
            "realtime_model_type": "tiny.en",
            "realtime_processing_pause": 0.2,
            "silero_sensitivity": 0.6,
            "silero_use_onnx": True,
            "spinner": False,
            "use_microphone": True,
        }

        with AudioToTextRecorder(**recorder_config) as recorder:
            self.recorder = recorder
            logger.debug("STT Ready")
            self.signals.stt_ready = True
            while not self.signals.terminate:
                if not self.enabled:
                    time.sleep(0.2)
                    continue
                recorder.text(self.process_text)

    class API:
        def __init__(self, outer):
            self.outer = outer

        def set_STT_status(self, status):
            self.outer.enabled = status
            self.outer.signals.sio_queue.put(("STT_status", status))

        def get_STT_status(self):
            return self.outer.enabled

        def shutdown(self):
            self.outer.recorder.stop()
            self.outer.recorder.interrupt_stop_event.set()
