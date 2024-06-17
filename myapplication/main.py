import signal
import sys
import threading
import time

from loguru import logger

from .signals import Signals
from .socketioServer import SocketIOServer
from .stt import STT


def main():
    logger.info("Starting Project")

    # Register signal handler so that all threads can be exited.
    def signal_handler(sig, frame):
        logger.debug(
            "Received CTRL + C, attempting to gracefully exit. Close all dashboard windows to speed up shutdown."
        )
        signals.terminate = True
        stt.API.shutdown()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # CORE FILES
    # Singleton object that every module will be able to read/write to
    signals = Signals()
    logger.info("Core components initialized.")

    # MODULES
    # Modules that start disabled CANNOT be enabled while the program is running.
    modules = {}
    module_threads = {}

    stt = STT(signals)
    logger.info("STT module initialized.")

    # Create Socket.io server
    sio = SocketIOServer(signals, stt, modules=modules)
    logger.info("SocketIO server initialized.")

    stt_thread = threading.Thread(target=stt.listen_loop, daemon=True)
    sio_thread = threading.Thread(target=sio.start_server, daemon=True)

    sio_thread.start()
    logger.info("Starting SocketIO server thread")

    stt_thread.start()
    logger.info("Starting STT listening thread")

    # Create and start threads for modules
    for name, module in modules.items():
        logger.info(f"Starting {name} module thread")
        module_thread = threading.Thread(target=module.init_event_loop, daemon=True)
        module_threads[name] = module_thread
        module_thread.start()

    logger.info("All threads started, entering main loop.")
    while not signals.terminate:
        time.sleep(0.1)

    logger.info("Shutdown signal received, waiting for threads to terminate")
    for module_thread in module_threads.values():
        module_thread.join()

    sio_thread.join()

    logger.info("Shutdown complete, all threads terminated.")
    sys.exit(0)


if __name__ == "__main__":
    main()
