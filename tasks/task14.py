import json
import os
from tasks import task25

def load_variants():
    """Load question variants from JSON file"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        file_path = os.path.join(project_root, 'Gitlabrepository_chatbot', 'data', 'question_variants.json')
        
        
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        print(f"File not found: {file_path}")
        return {}
    except Exception as e:
        return {}

def extract_location(text):
    """Extract location from the question text"""
    try:
        words = text.lower().split()
        if "hall" in words:
            hall_index = words.index("hall")
            if hall_index + 1 < len(words):
                return words[hall_index + 1]
        return None
    except Exception as e:
        print(f"Error extracting location: {str(e)}")
        return None

def find_original_question(user_input):
    """Find the original question from variants"""
    variants_data = load_variants()
    user_input = user_input.lower().strip().rstrip('?')
    
    for original_q, data in variants_data.items():
        if user_input == original_q.lower() or user_input in [v.lower() for v in data['variants']]:
            return original_q, data
    return None, None

def process_task14(user_input):
    """Process questions about lecture halls"""
    try:
        original_q, data = find_original_question(user_input)
        if original_q and data:
            answer = data['answer']
            if 'lecturing hall' in original_q.lower():
                location = extract_location(original_q)
                if location:
                    weather_service = task25.WeatherService()
                    weather_info = weather_service.get_location_weather(location)
                    if weather_info:
                        return f"{answer}{weather_info}"
            return answer
        return "I'm sorry, I couldn't find information about that location."
    except Exception as e:
        print(f"Error in process_task14: {str(e)}")
        return "I encountered an error while processing your question."