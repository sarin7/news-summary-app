# News Topic Summary Flask App

## Overview
The **News Topic Summary Generator** is a Flask-based web application that allows users to enter a news topic and retrieve summarized news along with their sources. The app fetches the more relevant articles from multiple news sources and provides a structured summary for the user.

## Features
- User authentication with login and logout functionality
- Fetch news summaries from sources
- Displays clickable news sources with URLs
- Summarizes the 3 most relevant articles from the past 7 days
- Responsive UI with a dark-themed design

## Installation
### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/sarin7/news-summary-app.git
   cd news-summary-app
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```sh
   export FLASK_APP=run.py
   export FLASK_ENV=development
   ```
4. Run the Flask app:
   ```sh
   flask run
   ```
5. Open the app in your browser:
   ```sh
   http://127.0.0.1:5000
   ```

## API Usage
This app integrates with **NewsAPI** to fetch and summarize news articles.
- **NEWS_API_KEY** fetches the latest articles from sources like CNN and Google News.

## File Structure
```
/news-summary-app
│── templates/          # HTML templates
│── run.py             # Main Flask application
│── requirements.txt    # Dependencies
│── README.md          # Project documentation
```

## Usage
1. Navigate to the homepage.
2. Enter a news topic in the text area.
3. Click "Submit" to fetch news sources and summaries.
4. Click on source links to read full articles.
