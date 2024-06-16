from loguru import logger

from .stt import STT


def main():
    logger.debug("Starting...")
    STT()
    logger.debug("Done!")


if __name__ == "__main__":
    main()
