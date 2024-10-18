from django.urls import path
from .views import stock_suggestions,login_view,register,logout_view

urlpatterns = [
    # path('api/stocks/india/random/', RandomStockCreateAPIView.as_view(), name='random-india-stock-create'),
    path('stock-suggestions/',stock_suggestions, name='stock_suggestions'),
    # path('', check_user_status, name='check_user_status'),  
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

]
