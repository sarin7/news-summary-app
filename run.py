import os
from flask import Flask, request, render_template, redirect, url_for, session

from news_tools import extract_keywords, fetch_news_data
from apply_inference import generate_summary

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route('/')
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_submit():
    username = request.form.get('username')
    password = request.form.get('password')

    # TODO: Replace with proper authentication logic
    if username == 'admin' and password == 'password':
        session['username'] = username
        return redirect(url_for('home'))
    return render_template('login.html', error='Invalid credentials')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/process_prompt', methods=['POST'])
def process_prompt():
    if 'username' not in session:
        return redirect(url_for('login'))

    prompt = request.form.get('prompt', '')

    if not prompt:
        return render_template('home.html', error='Prompt is required')

    # Step 1: Extract keywords from the prompt
    keywords = extract_keywords(prompt)

    # Step 2: Fetch news data, create prompt
    input_news_data = fetch_news_data(keywords)

    # Step 3: Get summary from LLM
    out_news_data = generate_summary(input_news_data)

    return render_template('home.html', original_prompt=prompt, news_sources=input_news_data['sources'], topic_summaries=out_news_data)

if __name__ == '__main__':
    app.run(debug=True)
