# services/auth-service/app/utils/logging.py
import logging
import sys
from pythonjsonlogger import jsonlogger
from app.core.config import settings

class JsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        log_record['logger'] = record.name
        log_record['timestamp'] = record.created

def setup_logging():
    """Setup JSON logging"""
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # JSON formatter
    formatter = JsonFormatter(
        '%(timestamp)s %(level)s %(logger)s %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger