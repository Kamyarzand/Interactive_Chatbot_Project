import time

# List of goodbye keywords
GOODBYE_KEYWORDS = ["bye", "goodbye", "see you", "take care", "byebye", "farewell", "later", "adieu"]

def get_timestamp():
    return time.strftime("%H:%M:%S")

def is_goodbye(user_input):
    """
    Check if the input is a goodbye phrase.
    Returns True if the input is a goodbye phrase, False otherwise.
    """
    return any(keyword in user_input.lower() for keyword in GOODBYE_KEYWORDS)

def handle_task7(user_input):
    """
    Handles task 7 logic: checking for goodbye phrases.
    Returns True if the program should exit (goodbye detected), False otherwise.
    """
    if is_goodbye(user_input):
        print(f"{get_timestamp()} 🤖 It was such a pleasure chatting with you! Have a fantastic day! 👋")
        return True
    return False
