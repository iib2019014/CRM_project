from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.
# def homePageView(request) :
#     return HttpResponse("<h1>This is the home page</h1>")

def homePageView(request) :
    context = {}
    return render(request, 'accounts\home_page.html', context)

def dashboardView(request) :
    context = {}
    return render(request, 'accounts\dashboard.html', context)

def productsView(request) :
    context = {}
    return render(request, 'accounts\products.html', context)

def customerView(request) :
    context = {}
    return render(request, 'accounts\customer.html', context)

def statusView(request) :
    context = {}
    return render(request, 'accounts\status.html', context)