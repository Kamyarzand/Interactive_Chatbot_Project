import time

# Predefined questions and answers
PREDEFINED_ANSWERS = {
    "what is your name": "I'm ChatGPT, your friendly chatbot! 😊",
    "how are you": "I'm just a bunch of code, but I'm feeling great! How about you? 😄",
    "what can you do": "I can chat with you, answer your questions, and make your day brighter! 🌞",
    "tell me a joke": "Why did the scarecrow win an award? Because he was outstanding in his field! 😂"
}

def get_timestamp():
    """
    Get current timestamp
    Aktuellen Zeitstempel abrufen
    دریافت برچسب زمانی فعلی
    """
    return time.strftime("%H:%M:%S")

def process_question(user_input):
    """
    Process user question and return appropriate response
    Benutzerfrage verarbeiten und passende Antwort zurückgeben
    پردازش سوال کاربر و برگرداندن پاسخ مناسب
    """
    if not user_input:
        return None
        
    normalized_input = user_input.lower().strip()
    return PREDEFINED_ANSWERS.get(normalized_input)

def handle_task8(user_input):
    """
    Handles task 8 logic: responding to predefined questions.
    Returns True if a valid response is given, False otherwise.
    """
    try:
        response = process_question(user_input)
        if response:
            print(f"{get_timestamp()} 🤖 {response}")
            return response
        return None       
    except Exception as e:
            print(f"{get_timestamp()} 🤖 Hmm, I’m not sure about that. Could you try asking something else? 🤔")
            return None



