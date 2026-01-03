"""Custom logger module with file and console output support."""
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class CustomLogger:
    """
    Custom logger with three log levels: minor, warning, and bug.

    This logger supports both console output and optional file logging.
    Log levels are mapped as follows:
    - MINOR (INFO): Minor issues that don't affect functionality
    - WARNING: Situations that could lead to problems
    - BUG (ERROR): Actual bugs and errors
    """

    def __init__(self, name: str, log_dir: Optional[Path] = None) -> None:
        """
        Initialize the custom logger.

        Args:
            name: Name for the logger instance
            log_dir: Optional directory path for log files
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Prevent duplicate handlers
        if not self.logger.handlers:
            # Console handler - shows INFO and above
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(
                logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            )
            self.logger.addHandler(console_handler)

            # File handler - logs everything (optional)
            if log_dir:
                log_dir.mkdir(parents=True, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_handler = logging.FileHandler(
                    log_dir / f"{name}_{timestamp}.log", encoding="utf-8"
                )
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(
                    logging.Formatter(
                        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                    )
                )
                self.logger.addHandler(file_handler)

    def minor(self, message: str) -> None:
        """
        Log minor issues that don't affect functionality.

        Args:
            message: The log message describing the minor issue
        """
        self.logger.info(f"MINOR: {message}")

    def warning(self, message: str) -> None:
        """
        Log warnings about situations that could lead to problems.

        Args:
            message: The warning message describing the potential issue
        """
        self.logger.warning(f"WARNING: {message}")

    def bug(self, message: str) -> None:
        """
        Log bugs and errors that need attention.

        Args:
            message: The error message describing the bug
        """
        self.logger.error(f"BUG: {message}")


# Global logger instance for the application
logger = CustomLogger("todo_app", Path("logs"))
