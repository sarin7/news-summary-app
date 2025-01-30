import os
from flask import Flask, request, render_template, redirect, url_for, session
import requests
import re
from datetime import datetime, timedelta
from newspaper import Article

# Config params
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Extract keywords from the prompt
def extract_keywords(prompt):
    # Find and filter for significant words
    # return re.findall(r'\b\w{4,}\b', prompt)
    return prompt

# Extract article text from url
def extract_article_text_from_url(article_url):

    article_data = Article(url="%s" % (article_url), language='en')
    article_data.download()
    article_data.parse()
    
    out_text = f'{article_data.title}:\n {article_data.text} \n\n'
    # out_text = f'{article_data.title}:\n {article_data.summary} \n'

    return out_text

# Create instruction prompt
def create_prompt():
    # prompt = (
    #     "Please provide a clear and concise summary of the following "
    #     "news articles. "
    #     "Ensure the summary highlights the most important information, "
    #     "is coherent, and flows naturally. "
    #     "The output should be structured in a professional manner, "
    #     "with attention to readability and clarity, "
    #     "making it suitable for inclusion in reports or articles. "
    #     "Focus on delivering an insightful overview "
    #     "that avoids unnecessary repetition, while maintaining "
    #     "a smooth narrative throughout. "
    #     "Ensure that no special characters (such as '\\n', '\\t', or other symbols) "
    #     "are included in the output. \n\n"
    # )
    # prompt = (
    #     "Please provide a clear and concise summary of the following "
    #     "news articles: \n\n"
    # )

    prompt = ""

    return prompt

# Fetch top 5 headlines based on keywords
def fetch_news_data(keywords):

    # Define time window
    date_obj_start = datetime.now() - timedelta(days=7)
    date_str_start = date_obj_start.strftime("%Y-%m-%d")
    date_obj_end = datetime.now()
    date_str_end = date_obj_end.strftime("%Y-%m-%d")

    # Create instruction prompt
    input_prompt = create_prompt()

    # Define query based on extracted keywords
    # query = ' '.join(keywords)
    query = keywords

    # URL for NewsAPI
    url = f'https://newsapi.org/v2/everything'

    # Config params for NewsAPI
    params = {
        "q": f"{query}",  # Query topic
        "sources": "google-news,cnn,bloomberg,cbs-news,espn,fox-news,politico,reuters,the-verge,wired,vice-news",   # Restrict sources
        "from":{date_str_start},
        "to": {date_str_end},
        "pageSize": 100,      # Limit articles
        "sortBy": "relevancy",  # Sort by relevancy
        "apiKey": {NEWS_API_KEY}   # Your API key
    }

    # Get response
    response = requests.get(url, params=params)

    # Parse reponse, generate input prompt
    out = {}
    out['sources'] = {}
    out['input_prompts'] = {}
    if response.status_code == 200:
        result_articles = response.json().get('articles', [])

        for article in result_articles:

            # Ensure there are at least 3 different sources
            if len(out['sources'].keys()) == 3:
                break

            # Get source name
            source_name = article['source']['name']
            
            try:

                # Get article content that needs to be summarized
                article_text_str = extract_article_text_from_url(article['url'])

                # Add source
                out['sources'][f'{source_name} -- {article['url']}'] = article['url']

                # Add input prompt
                out['input_prompts'][article['title']] = f"Summarize the following in three sentences:\n{article_text_str}"

            except:
                continue

    return out