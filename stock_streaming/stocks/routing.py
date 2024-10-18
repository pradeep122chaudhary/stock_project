# stock_streaming/stocks/routing.py

from django.urls import re_path
from .consumer import StockConsumer

websocket_urlpatterns = [
    re_path(r'ws/stocks/(?P<tickers>[^/]+)/$', StockConsumer.as_asgi()),
]
