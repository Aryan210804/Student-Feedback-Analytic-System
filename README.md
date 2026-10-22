# Student Feedback Analytics System

A beginner-friendly student feedback dashboard built with Python, Flask, and pandas. It cleans feedback data, summarizes ratings and comments, and displays results in a responsive dashboard.

## Features

- Overview page with response, rating, sentiment, and course highlights
- Dashboard with category averages, rating distribution, sentiment, monthly trends, and department averages
- Top and bottom course rankings, frequent keywords, and recent comments
- Feedback form with server-side validation for ratings from 1 to 5
- JSON summary endpoint for dashboard charts
- Synthetic dataset generator for creating 500 sample responses

## Requirements

- Python 3.9 or later
- pip

## Setup and run

Open a terminal in the project folder (`student-feedback-system/`) and install the dependencies:

```bash
pip install -r requirements.txt
```

Start the Flask development server:

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. The development server is intended for local use, not production deployment.

### Optional: regenerate sample data

To create a fresh 500-row synthetic dataset, run:

```bash
python generate_dataset.py
```

This replaces `feedback.csv`. Back up any feedback you want to keep before running the generator.

## Pages and API

| Path | Description |
| --- | --- |
| `/` | Overview and key performance indicators |
| `/dashboard` | Charts, course rankings, keywords, and latest comments |
| `/feedback` | Feedback form (GET) and submission endpoint (POST) |
| `/api/summary` | Analytics summary as JSON |

## Project structure

```text
student-feedback-system/
├── app.py
├── data_analysis.py
├── data_cleaning.py
├── generate_dataset.py
├── requirements.txt
├── feedback.csv
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   └── feedback.html
└── static/
    ├── css/style.css
    └── js/dashboard.js
```

## Dataset

`feedback.csv` stores feedback IDs, dates, student and course details, five 1–5 ratings, and a comment. The application reads the CSV beside `app.py`, so it can be launched from another working directory.

The sample data is synthetic. Sentiment is estimated with a small word list and falls back to the overall rating when a comment contains no recognized sentiment words; it is not a full natural-language sentiment model.