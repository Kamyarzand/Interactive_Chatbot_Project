# task15.py
import csv

# Function to import questions and answers from a CSV file
def import_csv(filepath):
    """
    Imports questions and answers from a CSV file and returns a list of dictionaries.
    Each dictionary contains a question and its possible answers.
    
    :param filepath: Path to the CSV file
    :return: List of dictionaries with keys 'question' and 'answers'
    """
    qa_list = []
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                question = row['question']
                answers = [row[f'answer{i}'] for i in range(1, 5) if row[f'answer{i}'].strip()]
                qa_list.append({"question": question, "answers": answers})
    except Exception as e:
        print(f"Error importing CSV: {e}")
    return qa_list

# Example usage
def handle_task15(args):
    """Handle importing questions and answers from a CSV file."""
    try:
        # Open and read the CSV file
        with open(args.filepath, mode="r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            qa_list = []
            for row in reader:
                question = row.get("Question", "").strip()
                answers = [
                    row.get(f"Answer{i}", "").strip()
                    for i in range(1, 5)
                    if row.get(f"Answer{i}", "").strip()
                ]
                if question and answers:
                    qa_list.append({"question": question, "answers": answers})

        if not qa_list:  # بررسی اگر لیست خالی باشد
            raise ValueError("CSV file contains no valid questions and answers.")

        return qa_list

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {args.filepath}")
    except KeyError:
        raise ValueError("CSV file is missing required columns (e.g., 'Question', 'Answer1').")
    except Exception as e:
        raise Exception(f"An error occurred while importing CSV: {e}")

