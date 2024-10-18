from celery import shared_task
import requests
from .models import Stock
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import re  

@shared_task
def fetch_stock_data():
    url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500'

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("run")
        data = response.json()
        stocks = data.get('data', [])  

        # Get the channel layer 
        channel_layer = get_channel_layer()

        for stock_data in stocks:
            stock, created = Stock.objects.update_or_create(
                ticker=stock_data['symbol'],  
                defaults={
                    "name": stock_data.get("symbol", ""),  
                    "current_price": stock_data.get("lastPrice", 0),
                    "opening_price": stock_data.get("open", 0),
                    "daily_high": stock_data.get("dayHigh", 0),
                    "daily_low": stock_data.get("dayLow", 0),
                    "previous_close": stock_data.get("previousClose", 0),
                    "percentage_change": stock_data.get("pChange", 0),
                    "volume": stock_data.get("totalTradedVolume", 0),
                    "market_cap": stock_data.get("ffmc", 0),
                    "pe_ratio": None,  
                    "dividend_yield": None,  
                    "sector": stock_data.get("meta", {}).get("industry", ""),
                    "exchange": 'NSE',  
                }
            )

            sanitized_ticker = re.sub(r'[^a-zA-Z0-9_.-]', '_', stock_data.get('symbol', ''))

            async_to_sync(channel_layer.group_send)(
                f"stock_{sanitized_ticker}",  
                {
                    'type': 'stock_update',
                    'ticker':stock_data.get("symbol", ""),
                    'price': stock_data.get("lastPrice", 0)  #
                }
            )
    else:
        print(f"Failed to fetch stock data from {url}. Status Code: {response.status_code}")
