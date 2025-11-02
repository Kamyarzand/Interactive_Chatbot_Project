import argparse  # Library to handle command-line arguments / کتابخانه برای مدیریت آرگومان‌های خط فرمان
import json
import os

def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Chatbot Command-Line Argument Handler")

    # Argument for Task 9
    parser.add_argument(
        "--question",
        type=str,
        help="Direct question to the chatbot / سوال مستقیم به چت‌بات"
    )

    # Arguments for Task 15
    parser.add_argument(
        "--import",
        dest="import_flag",
        action="store_true",
        help="Enable import mode / حالت ایمپورت را فعال کنید"
    )
    parser.add_argument(
        "--filetype",
        type=str,
        help="Specify the file type (e.g., CSV) / نوع فایل را مشخص کنید (مانند CSV)"
    )
    parser.add_argument(
        "--filepath",
        type=str,
        help="Path to the file to import / مسیر فایل برای ایمپورت"
    )

    # Argument for Task 16: --list
    parser.add_argument(
        "--list",
        dest="list_flag",  # تنظیم نام صفت در شیء args
        action="store_true",
        help="List all questions in the knowledge base / نمایش همه سوالات"
    )

    return parser.parse_args()

def load_qa_database():
    """
    Load questions and answers from JSON file
    """
    try:
        filepath = os.path.join('data', 'questions_answers.json')
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON: {str(e)}")
        return {}

def handle_task9(question, handler):
    """
    Handle direct question from CLI
    """
    try:
        # First try predefined answers from task8
        response = handler(question)
        if response:
            return response
        
        # If no predefined answer, check JSON database
        qa_database = load_qa_database()
        normalized_question = question.lower().strip()
        
        if normalized_question in qa_database:
            answers = qa_database[normalized_question]
            # If answers is a list, return first answer, otherwise return the answer directly
            return answers[0] if isinstance(answers, list) else answers
            
        return "I'm not sure about that. Could you try asking something else?"
    except Exception as e:
        return f"Error processing question: {str(e)}"