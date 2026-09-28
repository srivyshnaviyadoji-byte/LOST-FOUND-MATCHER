# Lost & Found Matcher

A Python-based Lost & Found Matcher that provides both a
command-line interface and a Flask web interface.

## Features

- Register lost items
- Register found items
- Search by category
- Search by location
- Keyword-based matching
- Confidence scoring
- Status management
- JSON data storage
- CLI interface
- Flask web interface
- Automated tests

## Project Structure

lost-found-matcher/

├── app.py
├── main.py
├── matcher.py
├── utils.py
├── data.json
├── requirements.txt
├── templates/
├── static/
└── tests/

## Installation

Clone the repository:

git clone YOUR_REPOSITORY_URL

Enter the project:

cd lost-found-matcher

Create virtual environment:

python -m venv venv

Activate it:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

## Run CLI

python main.py

## Run Web Application

python app.py

Then open:

http://127.0.0.1:5000

## Testing

pytest

## Matching Logic

Category Match: 30 points

Location Match: 30 points

Keyword Match: 40 points

Total: 100 points

The matching score is a suggestion and does not prove ownership.