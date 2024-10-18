
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Stock, Subscription
from .forms import StockSearchForm, RegistrationForm, LoginForm
from django.http import JsonResponse

@login_required
def subscription_list(request):
    subscriptions = Subscription.objects.filter(user=request.user)

    search_form = StockSearchForm()

    search_results = []
    if request.method == "POST":
        search_form = StockSearchForm(request.POST)
        if search_form.is_valid():
            query = search_form.cleaned_data.get('query')
            search_results = Stock.objects.filter(ticker__icontains=query) | Stock.objects.filter(name__icontains=query)
    
    if 'add_subscription' in request.POST:
        stock_id = request.POST.get('stock_id')
        stock = Stock.objects.get(id=stock_id)
        Subscription.objects.create(user=request.user, stock=stock)
        return redirect('subscription_list')  

    context = {
        'subscriptions': subscriptions,
        'search_form': search_form,
        'search_results': search_results,
    }

    return render(request, 'subscription.html', context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('subscription_list')  
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  

def stock_suggestions(request):
    query = request.GET.get('q', '')
    if query:
        stocks = Stock.objects.filter(ticker__icontains=query)[:5]  
        suggestions = [{'ticker': stock.ticker, 'name': stock.name} for stock in stocks]
        return JsonResponse({'suggestions': suggestions})
    return JsonResponse({'suggestions': []})
