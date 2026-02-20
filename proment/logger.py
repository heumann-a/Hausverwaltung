import logging
import sys
from datetime import datetime
from typing import Optional


class UniversalLogger:
    _instance: Optional['UniversalLogger'] = None

    def __init__(self, name: str = "Hausverwaltung", level: int = logging.INFO):
        if UniversalLogger._instance is not None:
            return
        
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(level)
            
            formatter = logging.Formatter(
                fmt='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        UniversalLogger._instance = self

    @classmethod
    def get_logger(cls, caller_class: Optional[str] = None) -> logging.Logger:
        if cls._instance is None:
            cls()
        
        if caller_class:
            return logging.getLogger(f"Hausverwaltung.{caller_class}")
        return cls._instance.logger

    @staticmethod
    def debug(message: str, caller_class: Optional[str] = None):
        logger = UniversalLogger.get_logger(caller_class)
        logger.debug(message)

    @staticmethod
    def info(message: str, caller_class: Optional[str] = None):
        logger = UniversalLogger.get_logger(caller_class)
        logger.info(message)

    @staticmethod
    def warning(message: str, caller_class: Optional[str] = None):
        logger = UniversalLogger.get_logger(caller_class)
        logger.warning(message)

    @staticmethod
    def error(message: str, caller_class: Optional[str] = None):
        logger = UniversalLogger.get_logger(caller_class)
        logger.error(message)

    @staticmethod
    def critical(message: str, caller_class: Optional[str] = None):
        logger = UniversalLogger.get_logger(caller_class)
        logger.critical(message)
