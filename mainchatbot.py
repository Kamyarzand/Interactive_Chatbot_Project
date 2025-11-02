# mainchatbot.py
import argparse
from tasks import task7  # Import Task 7 from the tasks folder
from tasks import task8  # Import Task 8 from the tasks folder
from tasks import task9  # Import Task 9 from the tasks folder
from tasks import task10 # Import Task 10 from the tasks folder
from tasks import task12  # Import Task 12
from tasks.task13 import handle_task13 # Import Task 13
from tasks.task14 import process_task14  # Import Task 14
from tasks import task15  # Import Task 15
from tasks import task16  # Import Task 16
from tasks import task17  # Import Task 17 for adding/removing questions
from tasks import task18  # Import Task 18
from tasks import task19  # Import Task 19 for error handling and logging
from tasks import task20  # Import Task 20 for unit testing
from tasks import task21  # Import Task 21 for enhanced logging
from tasks import task22  # Import Task 22 for help text and error handling
from tasks import task23  # Import Task 23 and 24 for trivia game
from tasks import task25  # Import Task 25 for weather information
from tasks import task26  # Import Task 26 for weather forcast
import os
from tabulate import tabulate  # اضافه کردن کتابخانه برای نمایش بهتر
import sys  # For fixing Unicode encoding issues
import traceback

# Unicode configuration
sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')
os.environ["PYTHONUTF8"] = "1"

# Set Debug Mode for Task 10
task10.DEBUG_MODE = False  # Change to True to enable debug logging

def parse_arguments():
    """
    Parse command-line arguments and return known arguments along with unknown ones.
    """
    parser = argparse.ArgumentParser(description="Chatbot Application", add_help=False)
    
    # Task 20 arguments (debug and test)
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--test", action="store_true", help="Run unit tests")
    
    # Task 21 arguments (logging)
    parser.add_argument("--log", action="store_true", help="Enable logging mode")
    parser.add_argument("--log-level", choices=['INFO', 'WARNING'], 
                       default='WARNING', help="Set logging level")
    parser.add_argument("--help", action="store_true", help="Show help message and exit")
    
    # Task 9 arguments
    parser.add_argument("--question", type=str, help="The question text")
    
    # General arguments
    parser.add_argument("--import", action="store_true", help="Import questions from a CSV file")
    parser.add_argument("--filetype", type=str, help="Specify the type of file to import")
    parser.add_argument("--filepath", type=str, help="Specify the path to the file to import")
    parser.add_argument("--list", action="store_true", help="List all questions in the knowledge base")
    
    # Task 17 arguments
    parser.add_argument("--add", action="store_true", help="Add a new question or answer")
    parser.add_argument("--remove", action="store_true", help="Remove a question or answer")
    parser.add_argument("--edit-question", type=str, help="The question text to add or remove")
    parser.add_argument("--answer", type=str, help="The answer text")
    parser.add_argument("--import-file", action="store_true", help="Import questions from a CSV file")
    parser.add_argument("--file-path", type=str, help="Specify the path to the file to import")

    # Task 26 arguments
    parser.add_argument("--temp-changes", action="store_true", help="Show temperature changes for last 3 days")
    parser.add_argument("--forecast", type=str, help="Get temperature changes forecast for city")
    parser.add_argument("--temp-monitor", type=str, help="Monitor temperature for city")

    try:
        # Parse known arguments and get unknowns
        args, unknown = parser.parse_known_args()

        # If there are unknown arguments, handle them
        if unknown:
            task22.handle_unknown_argument(unknown)
            sys.exit(1)
            
        return args
    except Exception as e:
        print(f"Error parsing arguments: {str(e)}")
        task22.print_help()
        sys.exit(1)
    

def main():
    try:
        weather_service = task25.WeatherService()

        # Parse arguments first
        args = parse_arguments()
        
        # Handle --help argument immediately
        if args.help:
            task22.print_help()
            return

        # Initialize logger
        logger = task19.ChatbotLogger()
        logger.log_chat("Chatbot started", "SYSTEM")

        # Initialize enhanced logger if enabled
        enhanced_logger = None
        if args.log:
            enhanced_logger = task21.create_logger(level=args.log_level)
            
        # Handle Task 20: Unit Testing
        if args.test:
            print("Running unit tests...")
            success = task20.run_tests(debug_mode=args.debug)
            if success:
                print("✅ All tests passed successfully!")
            else:
                print("❌ Some tests failed. Check the output above for details.")
            return

        # Set debug mode for other tasks
        if args.debug:
            print("Debug mode enabled")
            task10.DEBUG_MODE = True        
        # Initialize qa_list to avoid uninitialized access
        qa_list = []
        
        # Always attempt to import the default CSV at startup
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        default_csv_path = os.path.join(project_root, 'Gitlabrepository_chatbot', 'data', 'questions.csv')

        print(f"Looking for CSV file at: {default_csv_path}")
        if os.path.exists(default_csv_path):
            print("File found!")
        else:
            print("File not found!")
        if os.path.exists(default_csv_path):
            try:
                success, result = task19.safe_import_csv(default_csv_path, logger)
                if success:
                    qa_list = result
                    logger.log_chat(f"Default CSV imported successfully: {len(qa_list)} questions loaded.", "SYSTEM")
                    table_data = [
                        [i + 1, item["question"], ", ".join(item["answers"])]
                        for i, item in enumerate(qa_list[:3])
                    ]
                    print(tabulate(table_data, headers=["#", "Question", "Answers"], tablefmt="grid"))
                else:
                    print(f"⚠️ Error loading default CSV: {result}")
                    logger.log_error(f"Error loading default CSV: {result}")
            except Exception as e:
                logger.log_error(f"Error importing default CSV: {e}", traceback.format_exc())
                print(task19.ERROR_MESSAGES['unexpected_error'])

        # Handle Task 15: Import mode (if --import is specified)
        if args.import_file:
            try:
                if not args.filepath:
                    print("\n❌ Error: No filepath specified. Please provide a filepath using --filepath argument.")
                    logger.log_error("Import attempted without filepath")
                    if enhanced_logger:
                        enhanced_logger.warning("Import attempted without filepath")
                    return

                success, result = task19.safe_import_csv(args.filepath, logger)
                if success:
                    qa_list = result
                    logger.log_chat(f"Successfully imported {len(qa_list)} questions from {args.filepath}", "SYSTEM")
                    if enhanced_logger:
                        enhanced_logger.log_import(args.filepath, True, f"Imported {len(qa_list)} questions")
                    print(f"\n✅ Successfully imported {len(qa_list)} questions from {args.filepath}")
                    if qa_list:
                        table_data = [
                            [i + 1, item["question"], ", ".join(item["answers"])]
                            for i, item in enumerate(qa_list[:3])
                        ]
                        print("\nPreview of imported questions:")
                        print(tabulate(table_data, headers=["#", "Question", "Answers"], tablefmt="grid"))
                else:
                    print(f"\n❌ CSV Import Error: {result}")
                    logger.log_error(f"CSV Import Error: {result}")
            except FileNotFoundError as e:
                error_msg = f"File not found: {args.filepath}"
                print(f"\n❌ Error: {error_msg}")
                logger.log_error(error_msg, traceback.format_exc())
            except PermissionError as e:
                error_msg = f"Permission denied accessing file: {args.filepath}"
                print(f"\n❌ Error: {error_msg}")
                logger.log_error(error_msg, traceback.format_exc())
            except UnicodeDecodeError as e:
                error_msg = "File encoding error. Please ensure the file is UTF-8 encoded."
                print(f"\n❌ Error: {error_msg}")
                logger.log_error(error_msg, traceback.format_exc())
            except Exception as e:
                error_msg = f"Unexpected error during import: {str(e)}"
                print(f"\n❌ Error: {error_msg}")
                logger.log_error(error_msg, traceback.format_exc())
            finally:
                return

        # Handle Task 16: List all questions
        if args.list:
            try:
                if not qa_list:
                    message = "Knowledge base not loaded. Please import a CSV file first."
                    print(message)
                    logger.log_chat(message, "SYSTEM")
                else:
                    print("\nListing questions:")
                    task16.list_questions(qa_list)
                    logger.log_chat("Listed all questions", "SYSTEM")
            except Exception as e:
                logger.log_error(f"Error listing questions: {e}", traceback.format_exc())
                print(task19.ERROR_MESSAGES['unexpected_error'])
            return

        # Handle Task 17: Adding/Removing questions
        if args.add:
            try:
                if args.edit_question and args.answer:
                    success = task17.add_question(qa_list, args.edit_question, args.answer)
                    if success:
                        logger.log_chat(f"Added question: {args.edit_question}", "SYSTEM")
                        if enhanced_logger:
                            enhanced_logger.info(f"Added question: {args.edit_question}")
                        if args.list:
                            task16.list_questions(qa_list)
                    return
                elif args.question and args.answer:
                    success = task18.add_answer(qa_list, args.question, args.answer)
                    if success:
                        logger.log_chat(f"Added answer to question: {args.question}", "SYSTEM")
                        if enhanced_logger:
                            enhanced_logger.info(f"Added answer to question: {args.question}")
                        if args.list:
                            task16.list_questions(qa_list)
                    return
                else:
                    print("For adding a new question use: --edit-question and --answer")
                    print("For adding a new answer use: --question and --answer")
                    return
            except Exception as e:
                logger.log_error(f"Error adding question/answer: {e}", traceback.format_exc())
                print(task19.ERROR_MESSAGES['unexpected_error'])
                return

        # Handle removing questions/answers
        if args.remove:
            try:
                if args.edit_question:
                    success = task17.remove_question(qa_list, args.edit_question)
                    if success:
                        logger.log_chat(f"Removed question: {args.edit_question}", "SYSTEM")
                        if args.list:
                            task16.list_questions(qa_list)
                    return
                elif args.question and args.answer:
                    success = task18.remove_answer(qa_list, args.question, args.answer)
                    if success:
                        logger.log_chat(f"Removed answer from question: {args.question}", "SYSTEM")
                        if args.list:
                            task16.list_questions(qa_list)
                    return
                else:
                    print("For removing an entire question use: --edit-question")
                    print("For removing a specific answer use: --question and --answer")
                    return
            except Exception as e:
                logger.log_error(f"Error removing question/answer: {e}", traceback.format_exc())
                print(task19.ERROR_MESSAGES['unexpected_error'])
                return

        # Handle Task 26: weather forecast
        if args.temp_changes:
            monitor = task26.TemperatureMonitor()
            changes = monitor.get_daily_changes()
            for change in changes:
                print(f"Date: {change['date']}")
                print(f"Local temp change: {change['local_change']}°C")
                print(f"Forecast temp change: {change['forecast_change']}°C")
                print(f"Accuracy difference: {abs(change['local_change'] - change['forecast_change'])}°C")
            return
        if args.forecast:
            forecast = task26.WeatherForecast()
            changes = forecast.get_forecast(args.forecast)
            if changes:
                for change in changes:
                    print(f"Date: {change['date']}, Temperature change: {change['change']}°C")
            return
         
        # Handle Task 9: Direct question
        if args.question:
            try:
                response = task9.handle_task9(args.question, task8.handle_task8)
                print(f"Chatbot: {response}")
                logger.log_chat(args.question, "USER")
                logger.log_chat(response, "BOT")
                if enhanced_logger:
                    enhanced_logger.log_answer_lookup(args.question, response)
                return
            except Exception as e:
                logger.log_error(f"Error handling direct question: {e}", traceback.format_exc())
                if enhanced_logger:
                    enhanced_logger.warning(f"Error handling question: {str(e)}")
                print(task19.ERROR_MESSAGES['unexpected_error'])
                return

        # Default chatbot behavior
        print("Welcome to the Chatbot! Let's begin.")
        logger.log_chat("Session started", "SYSTEM")
        previous_questions = set()
        # task23 Initialize trivia game
        trivia_game = task23.TriviaGame()

        while True:
            try:
                user_input = input(f"{task7.get_timestamp()} You: ").strip()
                logger.log_chat(user_input, "USER")
                
                # Handle Task 7: Check for goodbyes
                if task7.handle_task7(user_input):
                    logger.log_chat("User said goodbye", "SYSTEM")
                    break
                # Handle Task 23: Trivia Game
                if user_input.lower() == "trivia":
                    if not trivia_game.is_active:
                        # Start new game
                        response = trivia_game.start_game()
                        print(f"{task7.get_timestamp()} Bot: Let's play a trivia game! 🎮")
                    else:
                        # End current game and show score
                        response = trivia_game.get_score()
                        trivia_game = task23.TriviaGame()  # Reset game
                        print(f"{task7.get_timestamp()} Bot: Game ended. Returning to chat mode. 🎮")
                    print(f"{task7.get_timestamp()} Bot: {response}")
                    logger.log_chat(response, "BOT")
                    continue
                
                # Handle trivia game answers when game is active
                if trivia_game.is_active:
                    response = trivia_game.check_answer(user_input)
                    print(f"{task7.get_timestamp()} Bot: {response}")
                    logger.log_chat(response, "BOT")
                    continue # Skip other tasks when trivia game is active    
                # Handle Task 12: Keyword-based suggestions
                keyword_response = task12.handle_task12(user_input)
                if keyword_response:
                    print(f"{task7.get_timestamp()} Bot: {keyword_response}")
                    logger.log_chat(keyword_response, "BOT")
                    continue

                # Handle Task 13: Compound questions
                if "and" in user_input or "or" in user_input:
                    response = handle_task13(user_input)
                else:
                    # Handle Task 10: Multiple questions and random answers
                    response = task10.handle_task10(user_input, previous_questions)
                
                # Handle Task 14: Lecturing Hall questions first
                if "lecturing hall" in user_input.lower():
                    response = process_task14(user_input)
                    if response:
                        print(f"{task7.get_timestamp()} Bot: {response}")
                        logger.log_chat(response, "BOT")
                        continue

                if "weather" in user_input.lower():
                    city = weather_service.extract_city(user_input)
                    if city:
                        response = weather_service.get_location_weather(city)
                    else:
                        response = "Please specify a city name. Example: 'weather in London'"
                    print(f"{task7.get_timestamp()} Bot: {response}")
                    logger.log_chat(response, "BOT")
                    continue

                # Print the response
                print(f"{task7.get_timestamp()} Bot: {response}")
                logger.log_chat(response, "BOT")

            except KeyboardInterrupt:
                logger.log_chat("Session terminated by user (KeyboardInterrupt)", "SYSTEM")
                print("\nGoodbye! Thanks for chatting!")
                break
            except Exception as e:
                logger.log_error(f"Error in chat loop: {e}", traceback.format_exc())
                print("I encountered an error. Please try again.")

    except Exception as e:
        logger.log_error(f"Error parsing arguments: {e}", traceback.format_exc())
        print(task19.ERROR_MESSAGES['unexpected_error'])
        return

if __name__ == "__main__":
    main()