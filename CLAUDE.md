# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Flask-based web application for Canadian G1 driving exam preparation, supporting bilingual (Chinese/English) question banks, practice mode, wrong answer tracking, and manual question management.

## Commands

### Setup
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Run
```bash
python app.py  # Access at http://localhost:5000
# Or on Windows: run.bat
```

### Initialize/Reset Database
```bash
python init_db.py
```

### Run Tests
```bash
python test_app.py
```

## Architecture

### Core Modules

- **app.py** - Flask application with all routes and API endpoints
- **models.py** - SQLAlchemy models: `Question`, `WrongAnswer`, `PracticeSession`
- **init_db.py** - Database initialization script
- **test_app.py** - unittest-based test suite

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/questions` | GET | Get questions with pagination/filters |
| `/api/practice/questions` | GET | Get random questions for practice |
| `/api/questions` | POST | Add new question |
| `/api/questions/<id>/correct-answer` | PUT | Update correct answer |
| `/api/questions/<id>` | DELETE | Delete question |
| `/api/practice` | POST | Start practice session |
| `/api/practice/answer` | POST | Submit answer |
| `/api/practice/finish` | POST | Finish practice session |
| `/api/wrong-answers` | GET | Get wrong answer list |
| `/api/practice-history` | GET | Get practice history |
| `/api/stats` | GET | Get statistics |
| `/api/question-sources` | GET | Get question source list |

### Database Schema

- **questions** - Question bank with fields: id, question_text, options (JSON), correct_id, correct_answer, explanation, language (zh/en), category, source, image_path
- **wrong_answers** - Wrong answer records linked to questions
- **practice_sessions** - Practice session history with scores

### Key Patterns

- Options stored as JSON string in database, parsed with `json.loads()`
- Language filtering uses `language='zh'` or `language='en'`
- Random question selection uses `db.func.random()`
- Test mode uses in-memory SQLite: `sqlite:///:memory:`
