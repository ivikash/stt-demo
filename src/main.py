from loguru import logger


def hello_world():
    return "Hello World"


def main():
    logger.debug("Starting...")
    print(hello_world())  # noqa: T201 print only used as placeholder :)


if __name__ == "__main__":
    main()
