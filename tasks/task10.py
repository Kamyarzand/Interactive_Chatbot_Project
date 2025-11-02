# task10.py
import json
import os

# Debug Mode Variable
DEBUG_MODE = False  # Change to True to enable debug logging

def debug_log(message):
    """
    Prints a debug message if DEBUG_MODE is enabled.
    """
    if DEBUG_MODE:
        print(message)

def load_questions_answers():
    """
    Load questions and answers from an external JSON file.
    Fragen und Antworten aus einer externen JSON-Datei laden.
    بارگذاری سوالات و پاسخ‌ها از یک فایل JSON خارجی.
    """
    file_path = os.path.join(os.path.dirname(__file__), '../data/questions_answers.json')
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                debug_log("Debug: JSON loaded successfully.")
                return json.load(file)
        except json.JSONDecodeError as e:
            debug_log(f"Debug: Error loading JSON file: {e}")
    else:
        debug_log("Debug: JSON file not found.")
    return {}

# Load the questions and answers
QUESTIONS_ANSWERS = load_questions_answers()

def handle_task10(user_input, previous_questions=None):
    """
    Handles Task 10: Answering predefined questions, supporting random responses for similar questions.
    """
    import random  # Add random module

    # Initialize previous_questions if not provided
    if previous_questions is None:
        previous_questions = set()

    # Add the current question to the set of previous questions
    previous_questions.add(user_input)

    # Find responses for the given user input
    responses = QUESTIONS_ANSWERS.get(user_input.lower(), [])
    if responses:
        return random.choice(responses)  # Pick a random response for the question
    else:
        return "I'm not sure about that. Could you try asking something else?"

