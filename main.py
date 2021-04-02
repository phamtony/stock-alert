import requests
from twilio.rest import Client
import os

STOCK_API = os.environ["STOCK_API"]
NEWS_API = os.environ["NEWS_API"]
account_sid = os.environ["account_sid"]
auth_token= os.environ["auth_token"]

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

stock_url = "https://www.alphavantage.co/query"
stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": STOCK_API,
}
stock_response = requests.get(stock_url, params=stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json()
daily_stock_data = stock_data["Time Series (Daily)"] #Convert to list comprehension
counter = 0
today_close = []
for key, value in daily_stock_data.items():
    today_close.append(float(value["4. close"]))
    counter += 1
    if counter > 1:
        break

percentage = round((1 - (today_close[0] / today_close[1])) * 100, 2)
gain_loss = "📈" if today_close[0] - today_close[1] > 0 else "📉"
if percentage > 4:
    print("Get news")

    news_url = "https://newsapi.org/v2/everything"
    news_params = {
        "apiKey": NEWS_API,
        "qInTitle": COMPANY_NAME,
        "pageSize": 3
    }
    news_response = requests.get(news_url, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()
    news_article_data = news_data["articles"] #Convert to list comprehension
    client = Client(account_sid, auth_token)

    for news in news_article_data:
        message_text = f"""
                    {STOCK}: {gain_loss}{percentage}%
                    Headline: {news['title']}
                    Brief: {news['description']}
                """
        message = client.messages \
            .create(
            body=f"{message_text}",
            from_='+18064524372',
            to='<ENTERNUMBER HERE>'
        )


