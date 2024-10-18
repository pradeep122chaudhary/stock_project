import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get tickers from URL
        self.tickers = self.scope['url_route']['kwargs']['tickers'].split(',')
        self.group_names = [f"stock_{ticker}" for ticker in self.tickers]

        # Get the user from the WebSocket scope
        self.user = self.scope['user']

        # Check if the user is authenticated
        if self.user.is_authenticated:
            # Validate subscriptions
            subscribed_tickers = await self.get_subscribed_stocks(self.user, self.tickers)

            # Join stock groups only for stocks the user is subscribed to
            for ticker in subscribed_tickers:
                group_name = f"stock_{ticker}"
                await self.channel_layer.group_add(group_name, self.channel_name)

            # Accept the WebSocket connection
            await self.accept()

            # Fetch the current stock prices for the subscribed tickers asynchronously
            if subscribed_tickers:
                stocks = await self.get_stocks(subscribed_tickers)
                if stocks:
                    stock_data = [
                        {
                            'ticker': stock.ticker,
                            'price': float(stock.current_price)  
                        }
                        for stock in stocks
                    ]
                    await self.send(text_data=json.dumps(stock_data))
        else:
            # Reject the connection if the user is not authenticated
            await self.close()

    async def disconnect(self, close_code):
        # Leave stock groups
        for group_name in self.group_names:
            await self.channel_layer.group_discard(group_name, self.channel_name)

    async def stock_update(self, event):
        # Send updated stock data to WebSocket
        await self.send(text_data=json.dumps({
            'ticker': event['ticker'],
            'price': float(event['price'])
        }))

    @database_sync_to_async
    def get_stocks(self, tickers):
        from .models import Stock  # Import here to ensure the app is loaded
        return list(Stock.objects.filter(ticker__in=tickers))

    @database_sync_to_async
    def get_subscribed_stocks(self, user, tickers):
        from .models import Subscription  # Import here to ensure the app is loaded
        subscriptions = Subscription.objects.filter(user=user, stock__ticker__in=tickers)
        return list(subscriptions.values_list('stock__ticker', flat=True))
