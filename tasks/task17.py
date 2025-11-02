# tasks/task17.py
import csv
import os

def save_to_csv(qa_list, filepath="data/questions.csv"):
    """
    Save changes to CSV file
    
    :param qa_list: List of QA pairs to save
    :param filepath: Path to the CSV file
    :return: True if successful, False otherwise
    """
    try:
        # Ensure data directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            # Determine maximum number of answers
            max_answers = max(len(qa['answers']) for qa in qa_list)
            
            # Create column headers
            fieldnames = ['question'] + [f'answer{i+1}' for i in range(max_answers)]
            
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            # Write each QA pair
            for qa in qa_list:
                row = {'question': qa['question']}
                for i, answer in enumerate(qa['answers']):
                    row[f'answer{i+1}'] = answer
                writer.writerow(row)
        return True
    except Exception as e:
        print(f"Error saving to CSV file: {e}")
        return False

def add_question(qa_list, question, answer):
    """
    Add a new question and answer to the knowledge base
    
    :param qa_list: List of QA pairs
    :param question: Question to add
    :param answer: Answer to add
    :return: True if successful, False otherwise
    """
    try:
        # Check for duplicate questions
        if any(qa['question'].lower() == question.lower() for qa in qa_list):
            print(f"❌ Question already exists: {question}")
            return False
        
        # Add new question
        qa_list.append({
            'question': question,
            'answers': [answer]
        })
        
        # Save changes to CSV
        if save_to_csv(qa_list):
            print(f"✅ Successfully added question: {question}")
            return True
        else:
            print("❌ Failed to save changes")
            return False
            
    except Exception as e:
        print(f"❌ Error adding question: {e}")
        return False

def remove_question(qa_list, question):
    """
    Remove a question from the knowledge base
    
    :param qa_list: List of QA pairs
    :param question: Question to remove
    :return: True if successful, False otherwise
    """
    try:
        # Find and remove question
        original_length = len(qa_list)
        qa_list[:] = [qa for qa in qa_list if qa['question'].lower() != question.lower()]
        
        if len(qa_list) == original_length:
            print(f"❌ Question not found: {question}")
            return False
        
        # Save changes to CSV
        if save_to_csv(qa_list):
            print(f"✅ Successfully removed question: {question}")
            return True
        else:
            print("❌ Failed to save changes")
            return False
            
    except Exception as e:
        print(f"❌ Error removing question: {e}")
        return False