# task22.py

def print_help():
    """
    Print the help message with syntax, usage, and description of all command line arguments.
    """
    help_text = """
Chatbot Application - Help

Usage: python mainchatbot.py [OPTIONS]

Options:
  --help             Show this help message and exit
  --debug            Enable debug mode
  --test             Run unit tests
  --log              Enable logging mode
  --log-level LEVEL  Set logging level (INFO or WARNING)
  --question TEXT    Direct question to the chatbot
  --import           Import questions from a CSV file
  --filetype TYPE    Specify the type of file to import
  --filepath PATH    Specify the path to the file to import
  --list            List all questions in the knowledge base
  --add             Add a new question or answer
  --remove          Remove a question or answer
  --edit-question TEXT  The question text to add or remove
  --answer TEXT     The answer text
  --import-file     Import questions from a CSV file
  --file-path PATH  Specify the path to the file to import

Examples:
  python mainchatbot.py --question "What is your name?"
  python mainchatbot.py --import --filepath data/questions.csv
  python mainchatbot.py --list
"""
    print(help_text)

def handle_unknown_argument(unknown_args):
    """
    Handle unknown command line arguments by printing an error message and the help text.
    Args:
        unknown_args (list): List of unknown arguments
    """
    print(f"\n❌ Error: Unknown argument(s) provided: {' '.join(unknown_args)}")
    print("\nValid arguments are:")
    print_help()