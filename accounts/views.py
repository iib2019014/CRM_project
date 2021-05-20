from django.shortcuts import render

from django.http import HttpResponse

from .models import(
    Product,
    Customer,
    Order,
)

from .forms import(
    CreateOrderForm,
)

# Create your views here.
# def homePageView(request) :
#     return HttpResponse("<h1>This is the home page</h1>")

def homePageView(request) :
    context = {}
    return render(request, 'accounts\home_page.html', context)

def dashboardView(request) :
    context = {}
    # sorted_orders = Order.objects.all().order_by('customer')
    customers = Customer.objects.all()
    context['customers'] = customers

    orders = Order.objects.all()
    context['orders'] = orders

    total_orders = orders.count()
    context['total_orders'] = total_orders
    
    orders_delivered = orders.filter(status="delivered").count()
    context['orders_delivered'] = orders_delivered

    orders_pending = orders.filter(status="pending").count()
    context['orders_pending'] = orders_pending

    return render(request, 'accounts\dashboard.html', context)

def productsView(request) :
    context = {}
    products = Product.objects.all()
    context['products'] = products
    return render(request, 'accounts\products.html', context)

def customerView(request, pk_cust_id) :
    context = {}
    the_customer = Customer.objects.get(id=pk_cust_id)
    context['the_customer'] = the_customer

    # their_orders = Order.objects.filter(customer=the_customer)
    their_orders = the_customer.order_set.all()
    context['their_orders'] = their_orders
    
    total_orders = their_orders.count()
    context['total_orders'] = total_orders

    return render(request, 'accounts\customer.html', context)

def statusView(request) :
    context = {}
    return render(request, 'accounts\status.html', context)

def createOrderView(request) :
    context = {}
    createOrderForm = CreateOrderForm()
    context['createOrderForm'] = createOrderForm
    return render(request, 'accounts/form_templates/createOrder_form.html', context)