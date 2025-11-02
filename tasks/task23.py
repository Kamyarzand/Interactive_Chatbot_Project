# task23.py - Trivia Game Module
import random
import json
import os

class TriviaGame:
    """Class to manage the trivia game functionality"""
    
    def __init__(self, num_questions=10):
        """Initialize trivia game with specified number of questions"""
        self.num_questions = num_questions
        self.current_question = 0
        self.score = 0
        self.questions = []
        self.is_active = False
        self.game_questions = []
        self.load_questions()

    def load_questions(self):
        """Load questions from JSON file"""
        try:
            file_path = 'data/trivia_questions.json'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if 'questions' in data:
                        # Convert questions to include correct_answer index
                        self.questions = []
                        for q in data['questions']:
                            # Find index of correct answer
                            correct_index = q['options'].index(q['answer'])
                            question = {
                                'question': q['question'],
                                'options': q['options'],
                                'correct_answer': correct_index
                            }
                            self.questions.append(question)
        except Exception as e:
            print(f"Error loading questions: {e}")
            self.questions = []

    def start_game(self):
        """Start a new game"""
        if not self.questions:
            return "Error: No questions available. Please check trivia_questions.json file."
        
        self.is_active = True
        self.current_question = 0
        self.score = 0
        
        # Select random questions
        num_questions = min(self.num_questions, len(self.questions))
        self.game_questions = random.sample(self.questions, num_questions)
        
        return self.get_current_question()

    def get_current_question(self):
        """Get the current question text with progress indicator"""
        if not self.is_active or self.current_question >= len(self.game_questions):
            return self.end_game()

        question = self.game_questions[self.current_question]
        options = question['options']
        
        # Format question text with progress and score
        question_text = f"Question {self.current_question + 1}/{len(self.game_questions)}; Score {self.score}/{self.current_question}\n"
        question_text += question['question'] + "\n"
        for idx, option in enumerate(options):
            question_text += f"{chr(65 + idx)}) {option}\n"
        
        return question_text

    def check_answer(self, user_answer):
        """Check if the answer is correct and return feedback"""
        if not self.is_active:
            return "No active game. Type 'trivia' to start a new game."

        try:
            current = self.game_questions[self.current_question]
            
            # Convert answer to uppercase and validate
            user_answer = user_answer.strip().upper()
            if len(user_answer) != 1 or user_answer < 'A' or user_answer > 'D':
                return "Please enter a valid letter (A, B, C, or D)"

            # Convert letter to index
            answer_idx = ord(user_answer) - ord('A')
            if answer_idx >= len(current['options']):
                return "Invalid option. Please choose from the available answers."

            # Get user's choice and correct answer
            user_choice = current['options'][answer_idx]
            correct_index = current['correct_answer']
            correct_choice = current['options'][correct_index]

            # Prepare feedback
            feedback = []
            feedback.append(f"You answered: {user_choice}")
            feedback.append(f"Correct answer: {correct_choice}")
            
            if answer_idx == correct_index:
                self.score += 1
                feedback.append("✅ Correct!")
            else:
                feedback.append("❌ Wrong!")

            self.current_question += 1
            
            # Add next question or end game
            if self.current_question < len(self.game_questions):
                feedback.append("\n" + self.get_current_question())
            else:
                feedback.append(self.end_game())

            return "\n".join(feedback)

        except Exception as e:
            print(f"Error in check_answer: {e}")
            return "Error processing answer. Please try again."

    def end_game(self):
        """End the game and return final score"""
        self.is_active = False
        return f"Game Over! 🎮\nFinal Score: {self.score}/{len(self.game_questions)}"

    def get_score(self):
        """Get current score"""
        score = f"Current Score: {self.score}/{self.current_question}"
        self.is_active = False
        return score