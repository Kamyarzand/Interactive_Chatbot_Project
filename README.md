# Interactive Python Chatbot: Advanced Modular System (Tasks 7-27)

This repository hosts a comprehensive interactive console chatbot developed in Python as a core project for Term 1. The system follows a **modular, task-based approach** and demonstrates proficiency in CLI management, robust error handling, unit testing, logging, and integration with external data from a Raspberry Pi sensor network.

## Core Features and Technical Implementation

The chatbot's features are categorized into four main sections, detailing the implementation of all 27 defined tasks.

### I. Console Application and Q&A Foundation (Tasks 7-15)

* **Task 7 (Base Console App):** Implemented the core Command-Line Interface (CLI) loop. All output adheres to a strict `HH:MM:SS [Message]` format. Includes a welcoming message, opening question, and a graceful exit mechanism (`bye`).
* **Task 8 & 10 (Q&A Expansion):** Developed basic matching logic and expanded the knowledge base to answer at least **10 distinct questions** in the interactive session.
* **Task 9 (Command Line Input):** Integrated support for running Q&A queries directly via command-line arguments (e.g., `--question "QuestionX?"`), bypassing the standard interactive loop.
* **Task 11 (Random Answer Variants):** Improved user experience by implementing a mechanism to store and **randomly select one of 2 to 4 answer variants** for the same question.
* **Task 12 (Keyword Suggestions):** Added a feature to recognize specific keywords and provide a **numbered list of related questions** for user selection, guiding knowledge discovery.
* **Task 13 (Compound Questions):** Developed parsing logic to identify and answer **multiple, distinct questions** (including greetings) within a single user input.
* **Task 14 (Question Variants):** Implemented logic to map **multiple phrasings** for a single core question to the same canonical answer key, increasing matching robustness.
* **Task 15 (CSV Import Support):** Added support for dynamic knowledge base expansion via a dedicated CLI argument (e.g., `--import --filetype CSV --filepath ...`), allowing the app to parse and load new Q&A pairs from a specified CSV file.

### II. Service Provider Tools and Management (Tasks 16-18)

These features provide command-line utilities for maintaining and inspecting the knowledge base.

* **Task 16 (List Questions):** Implemented a CLI argument to print all currently supported internal questions, facilitating knowledge base inspection.
* **Task 17 (Add/Remove Questions):** Developed CLI arguments (`--add` and `--remove`) to manage entire question-answer pairs within the internal list.
* **Task 18 (Modify Answers):** Added granular control via CLI arguments to specifically **add or remove individual answer variants** for an already supported question.

### III. Reliability, Testing, and Logging (Tasks 19-22)

The project includes core engineering practices for stability and maintenance.

* **Task 19 (Graceful Crash Handling):** Implemented robust **Try-Except blocks** to catch critical errors during operations (e.g., invalid file path, corrupted CSV, access rights).
    * Upon detecting an application crash, the system saves both the **chat log** and the **traceback** to separate files with timestamps.
* **Task 20 (Built-in Self-Test):** Integrated a unit testing framework to run tests covering the application's main functionalities (e.g., answer look-up), triggered explicitly via a dedicated debug CLI argument.
* **Task 21 (File-Based Logging):** Added a configurable file-based logging feature, disabled by default. It can be enabled and set to a specific level (`INFO` or `WARNING` default) using CLI arguments to inspect application behavior.
* **Task 22 (Help Message/Argument):** Provided a standard `--help` CLI argument to print a comprehensive help message, including command syntax and usage. This message is also displayed upon detecting an unknown or mistyped argument.

### IV. University Services, Trivia, and Sensor Integration (Tasks 23-27)

These advanced features integrate an entertainment module and real-time data processing.

* **Task 23 (Base Built-in Trivia):** Implemented an interactive, multiple-choice trivia game initiated by a keyword (e.g., `trivia`). The game displays the correct answer after each attempt and returns the user's score upon exit, resuming the main chat thread.
* **Task 24 (Progress Indicator):** Displays the user's progress and score in real-time during the trivia session (e.g., "Question 5 of 10; Score 3/10").
* **Task 25 (Data Storage):** *This task number appears to be implicit or missing from the user stories provided, but likely related to structured data handling.* **(Note: Please clarify if Task 25 had a specific function)**
* **Task 26 (Sensor Accuracy Assessment):** Implemented a CLI tool to calculate and provide the daily temperature range (max-min) for the **most recent 3 days**, comparing local sensor readings (recorded every ~30 minutes by **Raspberry Pi**) against weather forecast data.
* **Task 27 (Average Local Temperature):** Enhanced location-based answers by including the **average sensor temperature** for the most recent 3 days, calculated specifically for the event/lecture time window, in the chatbot's response.

## Setup and Execution

1.  **Dependencies:**
    *(If you have a `requirements.txt` file, list main packages here or include the install command.)*
    ```bash
    # Example: pip install -r requirements.txt
    ```
2.  **Run Application:**
    ```bash
    python mainchatbot.py
    ```
    Refer to the built-in help message (`python mainchatbot.py --help`) for a list of all available management and debug commands.
---
