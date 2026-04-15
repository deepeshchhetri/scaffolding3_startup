# CSE 510 Operational Assignment 3: Text Preprocessing Web Service

This was a scaffolding assignment for CSE 510 where I built a small web service that pulls books from Project Gutenberg, cleans them up, and shows some basic stats about the text.

## Assignment Overview

The web service does four main things:
- Fetches text from Project Gutenberg URLs
- Cleans and preprocesses the text
- Provides statistical analysis
- Returns results via a clean web interface

## Quick Start

### 1. Environment Setup

First, I tested the environment:
I used the command : python test_setup.py

A few tests didn't get carried along, so I install missing packages:
I used the command : pip install -r requirements.txt

### 2. Running the Application

Started the Flask development server:
I used the command : python app.py

### 3. Testing the Interface

The web interface includes example URLs we can click to test:
- Pride and Prejudice by Jane Austen
- Frankenstein by Mary Shelley
- Alice in Wonderland by Lewis Carroll
- Moby Dick by Herman Melville

---

## Outputs

### Part 1 — test_setup.py Output
This confirms the environment was set up correctly and all packages loaded without issues.

![alt text](<Screenshot 2026-04-13 at 5.07.23 PM.png>)

### Part 2 — Flask Server Running
The terminal output showing the app is live.

![alt text](<Screenshot 2026-04-13 at 5.16.15 PM.png>)

![alt text](<Screenshot 2026-04-13 at 5.18.23 PM.png>)

### Part 3 — Web Interface Home Page
The main page where you paste in a Gutenberg URL and hit the button to analyze it.

![alt text](<Screenshot 2026-04-14 at 3.57.23 PM.png>)

### Part 4 — Analysis Results
The results page showing stats, a 3-sentence summary, and the first 500 characters of cleaned text — tested here with all 4 Books.

![alt text](<Screenshot 2026-04-13 at 5.26.24 PM-1.png>)
![alt text](<Screenshot 2026-04-13 at 5.26.35 PM.png>)

![alt text](<Screenshot 2026-04-13 at 5.27.43 PM.png>)
![alt text](<Screenshot 2026-04-13 at 5.27.56 PM.png>)

![alt text](<Screenshot 2026-04-13 at 5.28.54 PM.png>)
![alt text](<Screenshot 2026-04-13 at 5.29.07 PM.png>)

![alt text](<Screenshot 2026-04-13 at 5.30.21 PM.png>)
![alt text](<Screenshot 2026-04-13 at 5.30.35 PM.png>)

---

## What Was Implemented

### Part 1: Environment Setup
Forked the starter repo, opened it in a GitHub Codespace, ran `python --version` to confirm Python 3.9+, installed all dependencies via `pip install -r requirements.txt`, and ran `test_setup.py` to verify everything was working before moving on.

### Part 2: TextPreprocessor Methods

Added three methods to the `TextPreprocessor` class in `starter_preprocess.py`:

#### `fetch_from_url(url: str) -> str`
To check that the URL ends in `.txt` before doing anything, then used the `requests` library to download the raw text. I added proper error handling for timeouts, connection failures, and bad HTTP responses so it fails with a clear message rather than an ugly traceback.

#### `get_text_statistics(text: str) -> Dict`
Goes through the cleaned text and calculates total characters, total words, total sentences, average word length, and average sentence length. It also finds the top 10 most used words — with common stop words like "the," "and," "a" filtered out so you actually get something interesting back.

#### `create_summary(text: str, num_sentences: int = 3) -> str`
Splits the text into sentences using a regex pattern and returns the first three joined together as one string. It is a simple extractive approach but works well as a quick preview of what the book is about.

### Part 3: Flask API Endpoints

Built two working endpoints in `app.py`:

#### `POST /api/clean`
Took a JSON body with a Gutenberg URL, ran it through the full pipeline — fetch, clean, normalize, get stats, generated summary — and returned everything as a single JSON response. Returns `success: true` on a good run and `success: false` with an error message if anything goes wrong.

Expected input:
```json
{"url": "https://www.gutenberg.org/files/1342/1342-0.txt"}
```

Expected output:
```json
{
    "success": true,
    "cleaned_text": "It is a truth universally acknowledged...",
    "statistics": {
        "total_characters": 717571,
        "total_words": 124588,
        "total_sentences": 6403,
        "avg_word_length": 4.3,
        "avg_sentence_length": 19.5,
        "most_common_words": ["mr", "elizabeth", "darcy", ...]
    },
    "summary": "It is a truth universally acknowledged..."
}
```

#### `POST /api/analyze`
Took raw text directly instead of a URL, skipped the fetching and cleaning steps, and returned the statistics.

Expected input:
```json
{"text": "Your raw text here..."}
```

Expected output:
```json
{
    "success": true,
    "statistics": {...}
}
```

### Part 4: Frontend Integration

Finished the JavaScript in `templates/index.html` to wire everything together. The form grabs the URL you type in, sends it to `/api/clean` using a `fetch()` POST call, and then hands the response off to `displayResults()` which fills in all the stat cards, the summary box, and the text preview. If something fails — bad URL, slow server, wrong format — it shows a readable error message at the top instead of silently breaking.

---

## Testing Implementation

### Manual Testing
1. Started the server: `python app.py`
2. Opened http://localhost:5000
3. Tried the example URLs
4. Verified statistics

### Code Testing

# Testing individual components
python starter_preprocess.py

# Testing specific methods
python -c "
from starter_preprocess imported TextPreprocessor
tp = TextPreprocessor()

---

## Project Structure

scaffolding3_startup/
├── README.md                    
├── requirements.txt             # Python dependencies
├── test_setup.py                # Environment validation
├── app.py                       # Flask application
├── starter_preprocess.py        # Text preprocessing class
├── screenshots/
│   ├── test_setup.png
│   ├── server_running.png
│   ├── home_page.png
│   └── results.png
└── templates/
└── index.html              

---

## Learning Objectives

- Understanding text preprocessing fundamentals
- Learning basic web API development with Flask
- Practicing working with external data sources
- Gained experience with JSON APIs and frontend integration

---

## Methodology

1. **Started with Part 2**: Implemented the TextPreprocessor methods first
2. **Tested incrementally**: Tested each method as I implement it
3. **Used the existing methods**: The starter code provided helper methods for tokenization
4. **Handled errors**: Project Gutenberg URLs was sometimes slow
5. **Read the comments**: The TODO comments provide helpful hints

---

## Common Issues

**"Module not found" errors**: Run `pip install -r requirements.txt`

**Network timeouts**: Project Gutenberg can be slow; add reasonable timeouts to your requests

**Text encoding issues**: Project Gutenberg uses UTF-8; specify encoding when needed

**Port already in use**: Kill existing Flask processes or use a different port

---

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Requests Library](https://requests.readthedocs.io/)
- [Project Gutenberg](https://www.gutenberg.org/)
- [Regular Expressions in Python](https://docs.python.org/3/library/re.html)

---
