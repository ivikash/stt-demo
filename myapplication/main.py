import threading

from loguru import logger

from .signals import Signals
from .stt import STT


def main():
    signals = Signals()
    stt = STT(signals)
    stt_thread = threading.Thread(target=stt.listen_loop, daemon=True)
    stt_thread.start()

    stt_thread.join()

    logger.debug("Done!")


if __name__ == "__main__":
    main()
