# CricketGPT - A Cricket Information Chatbot powered by OpenAI's GPT-4
CricketGPT, a Cricket Information Chatbot using OpenAI's GPT-3.5 model. CricketBot is designed to respond to a wide range of cricket-related queries. This application is built using Python and Flask, with a user interface for interacting with the bot.

# Application Design
The chatbot, CricketBot, is designed as a Flask application. The Flask framework allows the creation of modular, reusable components which are organized as Blueprints. The chatbot uses Flask-Login for user authentication and dotenv for environment variable management.

The application makes use of OpenAI's GPT-3.5 model, which has been trained on a diverse range of internet text to respond to the user's cricket-related queries.

# Development
CricketBot was developed using Python. The following libraries and dependencies are used:

- Flask: A micro web framework written in Python.
- Flask-Login: Provides user session management for Flask.
- Python-dotenv: Reads key-value pair from .env file and adds them to environment variable.
- OpenAI's GPT-4: AI model for generating human-like text.

# Installation
To set up and run CricketBot, you'll need to follow these steps:
# Requirements
Python 3.6 or later
Pip: A package installer for Python.
# Steps
1. Clone the repository to your local machine.
```
git clone https://github.com/trandrewan/cits3403project
```
2. Navigate to the project directory.
```
cd cits3403project
```
3. Create a virtual environment and activate it:
```
python3 -m venv venv
source venv/bin/activate
```
4. Install the necessary dependencies using pip:
```
pip install -r requirements.txt
```
5. Edit the .env file in the **/website** directory of the project and add your OpenAI key:
- to get an API Key go to https://platform.openai.com/
- accounts --> view api keys --> create new secret key
```
OPENAI_API_KEY="ENTER_YOUR_API_KEY"
```

# Running the Application Locally
To run the CricketBot application locally, follow these steps:

Ensure you're in the project directory and your virtual environment is active.

Run the application with the Flask command:
```
export FLASK_APP=main
flask run
```
Open your browser and visit http://localhost:5000.
