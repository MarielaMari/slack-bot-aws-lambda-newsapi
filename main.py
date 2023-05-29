import urllib.request
import json
import os

def lambda_handler(event, context):
    # Get the API key from environment variables
    api_key = os.environ['NEWSAPI_API_KEY']

    # Get the webhook URL from environment variables
    webhook_url = os.environ['SLACK_WEBHOOK_URL']

    # Set the news source and API endpoint
    news_source = 'bbc-news' #or can use 'cnn', 'TechCrunch', 'Calgary Herald', etc.
    api_endpoint = f'https://newsapi.org/v2/top-headlines?sources={news_source}&apiKey={api_key}'

    try:
        # Send a GET request to NewsAPI
        response = urllib.request.urlopen(api_endpoint)
        data = json.loads(response.read())

        # Extract the news articles
        articles = data['articles']

        # Prepare Slack message payload
        slack_payload = {
            'text': 'Latest news from NewsAPI:',
            'attachments': []
        }

        for article in articles:
            # Create an attachment for each article
            attachment = {
                'title': article['title'],
                'title_link': article['url'],
                'text': article['description'],
                'color': '#36a64f'  # Set a color for the attachment (optional)
            }
            slack_payload['attachments'].append(attachment)

        # Send the payload to Slack
        req = urllib.request.Request(webhook_url, method='POST')
        req.add_header('Content-Type', 'application/json')
        response = urllib.request.urlopen(req, json.dumps(slack_payload).encode())

        if response.getcode() == 200:
            return {
                'statusCode': 200,
                'body': 'News sent to Slack successfully.'
            }
        else:
            return {
                'statusCode': response.getcode(),
                'body': 'Failed to send news to Slack.'
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'An error occurred: {str(e)}'
        }
