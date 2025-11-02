# task13.py
import re
import random
from tasks.task10 import QUESTIONS_ANSWERS
from tasks.task12 import debug_log

def handle_task13(user_input):
    """
    Handles Task 13: Processes compound questions and returns answers.
    Verarbeitet zusammengesetzte Fragen und liefert Antworten zurück.
    سوالات مرکب را پردازش کرده و پاسخ‌ها را بازمی‌گرداند.
    """
    debug_log(f"Debug: Received compound question: {user_input}")

    # Define delimiters for splitting compound questions
    delimiters = r"\? and | and | or |, |; |\. |! "
    questions = re.split(delimiters, user_input.strip())
    debug_log(f"Debug: Split into individual questions: {questions}")

    responses = []
    for question in questions:
        # Clean up the question text
        question_cleaned = question.strip(" ?.").lower()

        if question_cleaned in QUESTIONS_ANSWERS:
            # Fetch a random answer if the question exists in the knowledge base
            answer = random.choice(QUESTIONS_ANSWERS[question_cleaned])
            responses.append(f"Q: {question.strip()}? A: {answer}")
        else:
            # Default response for unknown questions
            responses.append(f"Q: {question.strip()}? A: Sorry, I don't have an answer for that.")

    # Combine responses into a single string
    combined_response = "\n".join(responses)
    debug_log(f"Debug: Combined response: {combined_response}")

    return combined_response
