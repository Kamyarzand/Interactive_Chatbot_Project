# task12.py
import json
import os
import random

# Debug Mode Variable
DEBUG_MODE = False  # Change to True to enable debug logging

def debug_log(message):
    """
    Prints a debug message if DEBUG_MODE is enabled.
    Gibt eine Debug-Nachricht aus, wenn DEBUG_MODE aktiviert ist.
    اگر حالت اشکال‌زدایی فعال باشد، پیام دیباگ را چاپ می‌کند.
    """
    if DEBUG_MODE:
        print(message)

def load_keywords_and_questions():
    """
    Load keywords and related questions from an external JSON file.
    Schlagwörter und zugehörige Fragen aus einer externen JSON-Datei laden.
    بارگذاری کلیدواژه‌ها و سوالات مرتبط از یک فایل JSON خارجی.
    """
    file_path = os.path.join(os.path.dirname(__file__), '../data/keywords_questions.json')
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                debug_log("Debug: Keywords and questions loaded successfully.")
                return json.load(file)
        except json.JSONDecodeError as e:
            debug_log(f"Debug: Error loading JSON file: {e}")
    else:
        debug_log("Debug: JSON file not found.")
    return {}

# Load the keywords and related questions
KEYWORDS_QUESTIONS = load_keywords_and_questions()

def handle_task12(user_input):
    """
    Handles Task 12: Suggesting related questions for a keyword.
    Schlägt verwandte Fragen zu einem Schlüsselwort vor.
    پیشنهاد سوالات مرتبط با یک کلیدواژه.
    """
    debug_log(f"Debug: Received user input: {user_input}")

    # Check if the input matches any keyword
    related_questions = KEYWORDS_QUESTIONS.get(user_input.lower(), None)
    
    if related_questions:
        debug_log("Debug: Keyword found, suggesting related questions.")

        # Display related questions as a numbered list
        print("Here are some related questions you might ask:")
        for idx, question in enumerate(related_questions, start=1):
            print(f"{idx}. {question}")

        # Ask the user to select a question by number
        while True:
            selection = input("Please type the number of the question you want to ask: ").strip()
            if selection.isdigit():
                selection = int(selection)
                if 1 <= selection <= len(related_questions):
                    selected_question = related_questions[selection - 1]
                    debug_log(f"Debug: User selected question: {selected_question}")

                    # Fetch the answer from QUESTIONS_ANSWERS in task10
                    from tasks.task10 import QUESTIONS_ANSWERS
                    return QUESTIONS_ANSWERS.get(selected_question.lower(), "I'm not sure about that.")
            print("Invalid selection. Please enter a valid number.")
    
    debug_log("Debug: No related questions found for the keyword.")
    return None
