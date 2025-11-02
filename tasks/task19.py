# task19.py
import os
import csv
import time
import traceback
import logging
from datetime import datetime
from pathlib import Path

class ChatbotLogger:
    """Handle logging for both chat messages and error tracebacks."""
    
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging directory and files."""
        # Create logs directory if it doesn't exist
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Setup chat log
        chat_log_file = os.path.join(self.log_dir, f"chat_log_{self.timestamp}.txt")
        self.chat_logger = logging.getLogger('chat')
        self.chat_logger.setLevel(logging.INFO)
        chat_handler = logging.FileHandler(chat_log_file, encoding='utf-8')
        chat_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        self.chat_logger.addHandler(chat_handler)
        
        # Setup error log
        error_log_file = os.path.join(self.log_dir, f"error_log_{self.timestamp}.txt")
        self.error_logger = logging.getLogger('error')
        self.error_logger.setLevel(logging.ERROR)
        error_handler = logging.FileHandler(error_log_file, encoding='utf-8')
        error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.error_logger.addHandler(error_handler)
    
    def log_chat(self, message, sender):
        """Log chat messages."""
        self.chat_logger.info(f"{sender}: {message}")
    
    def log_error(self, error, traceback_info=None):
        """Log errors and their tracebacks."""
        self.error_logger.error(f"Error: {str(error)}")
        if traceback_info:
            self.error_logger.error(f"Traceback: {traceback_info}")

class CSVValidator:
    """Validate CSV files and handle various CSV-related errors."""
    
    @staticmethod
    def validate_file_path(filepath):
        """Check if the file path is valid and accessible."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"The file {filepath} does not exist.")
        
        if not os.access(filepath, os.R_OK):
            raise PermissionError(f"Insufficient permissions to read {filepath}")
        
        if not filepath.lower().endswith('.csv'):
            raise ValueError(f"File {filepath} is not a CSV file")
    
    @staticmethod
    def validate_csv_format(filepath):
        """Validate CSV file format and content."""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader)  # Read header
                
                # Check for required columns (question and at least one answer)
                required_columns = {'question', 'answer1'}
                header_set = {col.lower().strip() for col in header}
                
                if not required_columns.issubset(header_set):
                    raise ValueError("CSV file must contain 'question' and 'answer1' columns")
                
                # Validate each row
                for row_num, row in enumerate(csv_reader, start=2):
                    if len(row) != len(header):
                        raise ValueError(f"Invalid number of columns in row {row_num}")
                        
                    # Check if question field is not empty
                    if not row[header.index('question')].strip():
                        raise ValueError(f"Empty question field in row {row_num}")
                    
                    # Check if at least one answer is provided
                    answers = [row[i] for i, col in enumerate(header) if col.startswith('answer')]
                    if not any(ans.strip() for ans in answers):
                        raise ValueError(f"No answer provided for question in row {row_num}")
                        
        except csv.Error as e:
            raise ValueError(f"CSV parsing error: {str(e)}")
        except UnicodeDecodeError:
            raise ValueError("CSV file has invalid encoding. Please use UTF-8 encoding.")

def safe_import_csv(filepath, logger):
    """
    Safely import a CSV file with full validation and error handling.
    Returns a tuple (success, result/error_message)
    """
    if not os.path.exists(filepath):
        error_msg = "The file does not exist."
        logger.log_error(error_msg)
        return False, error_msg

    if not filepath.lower().endswith('.csv'):
        error_msg = "Invalid file type. Please provide a CSV file."
        logger.log_error(error_msg)
        return False, error_msg

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            # Try to read first few lines to check if file is readable
            content = file.read()
            if not content.strip():
                error_msg = "The CSV file is empty."
                logger.log_error(error_msg)
                return False, error_msg

            # Check CSV structure
            reader = csv.DictReader(content.splitlines())
            if not reader.fieldnames or 'question' not in reader.fieldnames:
                error_msg = "Invalid CSV structure. File must contain a 'question' column."
                logger.log_error(error_msg)
                return False, error_msg

            qa_list = []
            for i, row in enumerate(reader, 1):
                try:
                    question = row.get('question', '').strip()
                    if not question:
                        error_msg = f"Row {i}: Missing question."
                        logger.log_error(error_msg)
                        return False, error_msg

                    answers = [row.get(f'answer{j}', '').strip() 
                             for j in range(1, 5) 
                             if row.get(f'answer{j}', '').strip()]
                    
                    if not answers:
                        error_msg = f"Row {i}: No answers provided for question '{question}'"
                        logger.log_error(error_msg)
                        return False, error_msg

                    qa_list.append({"question": question, "answers": answers})
                except Exception as e:
                    error_msg = f"Error processing row {i}: {str(e)}"
                    logger.log_error(error_msg)
                    return False, error_msg

            return True, qa_list

    except UnicodeDecodeError:
        error_msg = "Invalid file encoding. Please use UTF-8 encoding."
        logger.log_error(error_msg)
        return False, error_msg
    except csv.Error as e:
        error_msg = f"CSV parsing error: {str(e)}"
        logger.log_error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Unexpected error while reading CSV: {str(e)}"
        logger.log_error(error_msg)
        return False, error_msg
    # Error message templates
ERROR_MESSAGES = {
    'file_not_found': "❌ Error: The file was not found.",
    'permission_denied': "❌ Error: Permission denied while accessing the file.",
    'invalid_format': "❌ Error: The file format is invalid or corrupted.",
    'encoding_error': "❌ Error: The file has invalid encoding. Please use UTF-8.",
    'unexpected_error': "❌ An unexpected error occurred. Please check the error logs."
}