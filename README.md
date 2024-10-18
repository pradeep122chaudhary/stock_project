# Stock Subscription Project

This project is a web application that allows users to subscribe to stock updates. Users can search for stocks and view their current prices, along with historical data. The application utilizes Django for the backend and Channels for real-time updates.

## Features

- User registration and authentication (login/logout)
- Subscription management for stocks
- Real-time stock price updates using WebSockets
- Search functionality for stocks
- User-friendly interface built with Bootstrap

## Tech Stack

- **Backend:** Django
- **WebSockets:** Django Channels
- **Database:** PostgreSQL (or any preferred database)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Task Queue:** Celery for asynchronous tasks
- **API:** Requests to fetch stock data from external APIs

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pradeep122chaudhary/stock_project.git
   cd stock_project
   
##Create and activate a virtual environment
python -m venv myenv
source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`

pip install -r requirements.txt


Setup DB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'stock_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

##Run migrations
python manage.py migrate

##Run Celery worker and Celery Beat:
celery -A stock_streaming worker -l info

##Start Celery Beat for scheduled tasks:
celery -A stock_streaming beat -l info

