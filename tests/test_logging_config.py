import logging

import src.utils.logging_config as logging_config


def test_configure_logging_creates_file_and_console_handlers(
    monkeypatch,
    tmp_path,
):
    log_dir = tmp_path / "logs"
    log_file = log_dir / "pipeline.log"

    monkeypatch.setattr(
        logging_config,
        "LOG_DIR",
        log_dir,
    )

    monkeypatch.setattr(
        logging_config,
        "LOG_FILE",
        log_file,
    )

    root_logger = logging.getLogger()

    original_handlers = root_logger.handlers.copy()
    original_level = root_logger.level

    try:
        logging_config.configure_logging()

        assert log_dir.exists()
        assert log_file.exists()

        assert root_logger.level == logging.INFO
        assert len(root_logger.handlers) == 2

        handler_types = {
            type(handler)
            for handler in root_logger.handlers
        }

        assert logging.FileHandler in handler_types
        assert logging.StreamHandler in handler_types

        test_logger = logging.getLogger("test_logging")

        test_logger.info("logging configuration test message")

        for handler in root_logger.handlers:
            handler.flush()

        log_contents = log_file.read_text()

        assert "logging configuration test message" in log_contents

    finally:
        for handler in root_logger.handlers:
            handler.close()

        root_logger.handlers.clear()

        for handler in original_handlers:
            root_logger.addHandler(handler)

        root_logger.setLevel(original_level)