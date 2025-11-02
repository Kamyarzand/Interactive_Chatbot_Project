# task21.py
import logging
import os
from datetime import datetime
from pathlib import Path

class EnhancedLogger:
    """
    Enhanced logging system with multiple levels
    Erweitertes Logging-System mit mehreren Ebenen
    سیستم لاگینگ پیشرفته با سطوح مختلف
    """
    
    LEVELS = {
        'INFO': logging.INFO,
        'WARNING': logging.WARNING
    }
    
    def __init__(self, log_dir="logs", level="WARNING"):
        """
        Initialize the logger with specified level
        Logger mit angegebener Ebene initialisieren
        راه‌اندازی لاگر با سطح مشخص شده
        """
        self.log_dir = log_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.level = self.LEVELS.get(level.upper(), logging.WARNING)
        self.setup_logging()
    
    def setup_logging(self):
        """
        Setup logging configuration
        Logging-Konfiguration einrichten
        تنظیم پیکربندی لاگینگ
        """
        # Create logs directory
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Setup main logger
        self.logger = logging.getLogger('chatbot')
        self.logger.setLevel(self.level)
        
        # Create log file with timestamp
        log_file = os.path.join(self.log_dir, f"chatbot_{self.timestamp}.log")
        handler = logging.FileHandler(log_file, encoding='utf-8')
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(handler)
        
        # Initial log message
        self.logger.info(f"Logging started with level: {logging.getLevelName(self.level)}")
    
    def info(self, message):
        """
        Log info message
        Info-Nachricht protokollieren
        ثبت پیام اطلاعاتی
        """
        self.logger.info(message)
    
    def warning(self, message):
        """
        Log warning message
        Warnmeldung protokollieren
        ثبت پیام هشدار
        """
        self.logger.warning(message)
    
    def log_answer_lookup(self, question, answer=None):
        """
        Log answer lookup attempts
        Protokollierung von Antwortsuchen
        ثبت تلاش‌های جستجوی پاسخ
        """
        if answer:
            self.info(f"Answer found for question: '{question}' -> '{answer}'")
        else:
            self.warning(f"No answer found for question: '{question}'")
    
    def log_import(self, filepath, success, message):
        """
        Log import operations
        Import-Vorgänge protokollieren
        ثبت عملیات وارد کردن
        """
        if success:
            self.info(f"Successfully imported data from: {filepath}")
        else:
            self.warning(f"Failed to import data from: {filepath}. Reason: {message}")
    
    def log_command(self, command, args):
        """
        Log CLI commands
        CLI-Befehle protokollieren
        ثبت دستورات خط فرمان
        """
        self.info(f"Command executed: {command} with args: {args}")

def create_logger(level="WARNING"):
    """
    Create a new logger instance
    Neue Logger-Instanz erstellen
    ایجاد یک نمونه جدید از لاگر
    """
    return EnhancedLogger(level=level)