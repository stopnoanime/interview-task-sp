# Phonebook Assistant

A web application made in Django that functions as a digital phone book.
It allows users to manage contacts using natural language prompts.

### Installation

You need to have Python version 3.10 or higher installed to use this project.
You'll also need an OpenAI account with a valid API key.

1. Clone and navigate to this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your OpenAI API key: `export OPENAI_API_KEY="your_api_key_here"`
4. Apply database migrations: `python manage.py migrate`
5. Launch the application: `python manage.py runserver`
6. Access the interface at `http://localhost:8000` in your browser

## Usage

The phonebook assistant understands various natural language commands. 
Examples include:

- Adding contacts: "Please add a record for Joanna with the number 222333444."
- Searching contacts: "What is the phone number for Joanna?"
- Updating contacts: "Update the phone number for Joanna to 555666777."
- Deleting contacts: "Delete Joanna's contact information."
- Listing contacts: "List all contacts."

## Technical Details

The backend is made using Django and uses the SQLite database via Django ORM.
The frontend is made in HTML, CSS with Django templates.

The application integrates with OpenAI's GPT-4o-mini model via the OpenAI API.
When a user enters a natural language prompt, it is processed as follows:

1. The prompt is sent to the LLM service
2. The LLM interprets the prompt and selects the appropriate function to call
3. The selected function is executed, performing the requested operation on the database
4. The user is redirected to the relevant page with a status message

## Project Structure

- `phonebook/` - Main application directory
  - `models.py` - Contact model definition
  - `views.py` - Django views for the application
  - `forms.py` - Form definition for prompt input
  - `services/` - Service classes including LLM integration
  - `templates/` - HTML templates for the interface
  - `static/` - CSS styling
- `phonebook_project/` - Django project settings and configuration