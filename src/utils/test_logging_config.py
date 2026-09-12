import logging

from src.utils.logging_config import (
    LOG_FILE,
    configure_logging,
)


def main():
    configure_logging()

    logger = logging.getLogger(__name__)

    logger.info("Logging test started.")
    logger.warning("This is a test warning.")
    logger.error("This is a test error.")

    print()
    print(f"Log file created at: {LOG_FILE}")


if __name__ == "__main__":
    main()