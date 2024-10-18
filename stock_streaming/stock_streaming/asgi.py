# stock_streaming/asgi.py

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from stocks import routing  # Import your routing

# Set the default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_streaming.settings')

# Ensure that Django apps are fully loaded before starting the ASGI application
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns  # Use the websocket URL patterns defined in routing.py
            # pass
        )
    ),
})
