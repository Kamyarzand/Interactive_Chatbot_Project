# tasks/task18.py
import csv
import os

def save_to_csv(qa_list, filepath="data/questions.csv"):
    """
    Save the updated QA list to CSV file
    CSV-Datei mit aktualisierten Fragen und Antworten speichern
    ذخیره لیست سوال و جواب‌های به‌روز شده در فایل CSV
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            max_answers = max(len(qa['answers']) for qa in qa_list)
            fieldnames = ['question'] + [f'answer{i+1}' for i in range(max_answers)]
            
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for qa in qa_list:
                row = {'question': qa['question']}
                for i, answer in enumerate(qa['answers']):
                    row[f'answer{i+1}'] = answer
                writer.writerow(row)
        return True
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return False

def add_answer(qa_list, question, new_answer):
    """
    Add a new answer to an existing question
    Neue Antwort zu einer bestehenden Frage hinzufügen
    اضافه کردن پاسخ جدید به یک سوال موجود
    """
    try:
        # Find the question
        for qa in qa_list:
            if qa['question'].lower() == question.lower():
                # Check if answer already exists
                if new_answer in qa['answers']:
                    print(f"❌ Answer already exists for question: {question}")
                    return False
                    
                # Add new answer
                qa['answers'].append(new_answer)
                
                # Save changes
                if save_to_csv(qa_list):
                    print(f"✅ Successfully added new answer to question: {question}")
                    return True
                else:
                    print("❌ Failed to save changes")
                    return False
                    
        print(f"❌ Question not found: {question}")
        return False
        
    except Exception as e:
        print(f"❌ Error adding answer: {e}")
        return False

def remove_answer(qa_list, question, answer_to_remove):
    """
    Remove an answer from an existing question
    Antwort von einer bestehenden Frage entfernen
    حذف یک پاسخ از سوال موجود
    """
    try:
        # Find the question
        for qa in qa_list:
            if qa['question'].lower() == question.lower():
                # Check if it's the only answer
                if len(qa['answers']) <= 1:
                    print(f"❌ Cannot remove the only answer for question: {question}")
                    return False
                    
                # Try to remove the answer
                if answer_to_remove in qa['answers']:
                    qa['answers'].remove(answer_to_remove)
                    
                    # Save changes
                    if save_to_csv(qa_list):
                        print(f"✅ Successfully removed answer from question: {question}")
                        return True
                    else:
                        print("❌ Failed to save changes")
                        return False
                        
                print(f"❌ Answer not found for question: {question}")
                return False
                
        print(f"❌ Question not found: {question}")
        return False
        
    except Exception as e:
        print(f"❌ Error removing answer: {e}")
        return False