# stock_app/admin.py

from django.contrib import admin
from .models import Stock,Subscription

# Register the Stock model with the default admin interface
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'name', 'current_price', 'opening_price', 'daily_high', 'daily_low', 'previous_close', 'percentage_change', 'volume', 'market_cap', 'exchange', 'last_updated')
    list_filter = ('exchange', 'sector')  
    search_fields = ('ticker', 'name')  
    ordering = ('ticker',)  
    readonly_fields = ('last_updated',)  


admin.site.register(Subscription)