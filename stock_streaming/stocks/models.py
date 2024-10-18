from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)  
    name = models.CharField(max_length=255)  
    current_price = models.DecimalField(max_digits=10, decimal_places=2)  
    opening_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  
    daily_high = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  
    daily_low = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  
    previous_close = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  
    percentage_change = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  
    volume = models.BigIntegerField(null=True, blank=True)  
    market_cap = models.BigIntegerField(null=True, blank=True)  
    pe_ratio = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  
    dividend_yield = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  
    sector = models.CharField(max_length=255, null=True, blank=True)  
    exchange = models.CharField(max_length=255, null=True, blank=True)  
    last_updated = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.ticker} - {self.name}"
    




class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'stock')

    # def __str__(self):
    #     return f"{self.user.username} subscribed to {self.stock.ticker}"


