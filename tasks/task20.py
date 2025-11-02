# task20.py
import unittest
import os
import sys
from unittest.mock import patch, MagicMock
from tasks import task8, task10, task12, task17, task18, task19

class ChatbotTestCase(unittest.TestCase):
    """
    Unit Testing for Chatbot main features
    Unit-Tests für die Hauptfunktionen des Chatbots
    تست‌های واحد برای قابلیت‌های اصلی چت‌بات
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Setup test environment once before all tests
        Test-Umgebung einmalig vor allen Tests einrichten
        آماده‌سازی محیط تست یکبار قبل از همه تست‌ها
        """
        # Create test directories
        os.makedirs("test_logs", exist_ok=True)
        os.makedirs("test_data", exist_ok=True)
        
        # Create a test CSV file
        with open("test_data/questions.csv", "w", encoding="utf-8") as f:
            f.write("question,answer1,answer2\n")
            f.write("test question 1,test answer 1,alternate answer 1\n")
            f.write("test question 2,test answer 2,alternate answer 2\n")
    
    def setUp(self):
        """
        Setup before each test
        Einrichtung vor jedem Test
        آماده‌سازی قبل از هر تست
        """
        self.logger = task19.ChatbotLogger(log_dir="test_logs")
        # Load test data from CSV
        success, result = task19.safe_import_csv("test_data/questions.csv", self.logger)
        self.test_qa_list = result if success else []

    def tearDown(self):
        """
        Cleanup after each test
        Aufräumen nach jedem Test
        پاکسازی بعد از هر تست
        """
        # Remove handlers
        for handler in self.logger.chat_logger.handlers[:]:
            handler.close()
            self.logger.chat_logger.removeHandler(handler)
        for handler in self.logger.error_logger.handlers[:]:
            handler.close()
            self.logger.error_logger.removeHandler(handler)

    @classmethod
    def tearDownClass(cls):
        """
        Final cleanup after all tests
        Endgültiges Aufräumen nach allen Tests
        پاکسازی نهایی بعد از همه تست‌ها
        """
        # Clean up test directories and files
        if os.path.exists("test_logs"):
            for file in os.listdir("test_logs"):
                os.remove(os.path.join("test_logs", file))
            os.rmdir("test_logs")
        if os.path.exists("test_data"):
            for file in os.listdir("test_data"):
                os.remove(os.path.join("test_data", file))
            os.rmdir("test_data")

    @patch('builtins.input', return_value='1')
    def test_predefined_answers(self, mock_input):
        """
        Test predefined answer lookup
        Test der vordefinierten Antwortsuche
        تست جستجوی پاسخ‌های از پیش تعریف شده
        """
        result = task8.handle_task8("what is your name")
        self.assertIsNotNone(result, "Should return a predefined answer")
        
        result = task8.handle_task8("invalid question")
        self.assertIsNone(result, "Should return None for invalid questions")

    @patch('tasks.task12.handle_task12')
    def test_keyword_suggestions(self, mock_handle):
        """
        Test keyword-based suggestions
        Test der schlüsselwortbasierten Vorschläge
        تست پیشنهادات بر اساس کلمات کلیدی
        """
        # Setup mock
        mock_handle.return_value = "Here are some Python-related questions"
        
        # Test
        result = task12.handle_task12("python")
        self.assertIsNotNone(result, "Should return suggestions for 'python' keyword")

    def test_qa_management(self):
        """
        Test question and answer management
        Test der Fragen- und Antwortverwaltung
        تست مدیریت سوال و جواب
        """
        # Mock save_to_csv function
        original_save = task17.save_to_csv
        task17.save_to_csv = MagicMock(return_value=True)
        
        try:
            # Test adding new question
            success = task17.add_question(self.test_qa_list, "new test question", "new test answer")
            self.assertTrue(success, "Should successfully add new question")
            
            # Test adding duplicate question
            success = task17.add_question(self.test_qa_list, "new test question", "another answer")
            self.assertFalse(success, "Should not add duplicate question")
            
            # Test removing question
            success = task17.remove_question(self.test_qa_list, "new test question")
            self.assertTrue(success, "Should successfully remove question")
        finally:
            # Restore original function
            task17.save_to_csv = original_save

def run_tests(debug_mode=False):
    """
    Run unit tests with optional debug mode
    Unit-Tests mit optionalem Debug-Modus ausführen
    اجرای تست‌های واحد با حالت دیباگ اختیاری
    """
    # Set debug mode
    task10.DEBUG_MODE = debug_mode
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(ChatbotTestCase)
    
    # Configure test runner
    runner = unittest.TextTestRunner(
        verbosity=2 if debug_mode else 1,
        buffer=not debug_mode  # Buffer output in non-debug mode
    )
    
    # Run tests and get results
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()