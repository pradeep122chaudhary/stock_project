# your_app_name/__init__.py

# Import the Celery app for task registration
from .celery import app as celery_app

# Import the task to ensure it is registered
# from stocks.tasks import fetch_stock_data

__all__ = ('celery_app',)
