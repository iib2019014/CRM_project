from django.shortcuts import render, redirect

from django.http import HttpResponse

from .models import(
    Product,
    Customer,
    Order,
)

from .forms import(
    OrderForm,
    CustomerForm,
    ProductForm,
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

def createProductView(request) :
    context = {}
    createProductForm = ProductForm()

    if request.method == 'POST' :
        createProductForm = ProductForm(request.POST)
        if createProductForm.is_valid() :
            createProductForm.save()
            return redirect('products')
        else :
            print("not valid")

    context['createProductForm'] = createProductForm
    return render(request, 'accounts/form_templates/create_product.html', context)

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

def updateCustomerView(request, pk_cust_id) :
    customer = Customer.objects.get(id=pk_cust_id)
    context = {}
    updateCustomerForm = CustomerForm(instance=customer)

    if request.method == 'POST' :
        updateCustomerForm = CustomerForm(request.POST, instance=customer)
        if updateCustomerForm.is_valid() :
            updateCustomerForm.save()
            return redirect('customer/pk_cust_id')

    context['updateCustomerForm'] = updateCustomerForm
    return render(request, 'accounts/form_templates/update_customer.html', context)

def statusView(request) :
    context = {}
    return render(request, 'accounts/status.html', context)

def createOrderView(request, pk_cust_id) :
    customer = Customer.objects.get(id=pk_cust_id)
    context = {}
    createOrderForm = OrderForm(
        initial={
            'customer': customer,
        }
    )

    if request.method == 'POST' :
        createOrderForm = OrderForm(request.POST)
        createOrderForm.save()
        return redirect('dashboard')
    context['createOrderForm'] = createOrderForm
    return render(request, 'accounts/form_templates/createOrder_form.html', context)

def createCustomerView(request) :
    context = {}
    createCustomerForm = CustomerForm()
    print("into view")

    if request.method == 'POST' :
        createCustomerForm = CustomerForm(request.POST)
        print("into post")
        if createCustomerForm.is_valid() :
            print("valid")
            # createCustomerForm.save()
            Customer.objects.create(
                name = request.POST.get('name'),
                phone = request.POST.get('phone'),
                email = request.POST.get('email'),
            )
            return redirect('dashboard')
        else :
            print("not valid")
            # print(createCustomerForm.errors)
    print("into get")
    context['createCustomerForm'] = createCustomerForm
    return render(request, 'accounts/form_templates/create_customer.html', context)

def removeCustomerView(request, pk_cust_id) :
    customer = Customer.objects.get(id=pk_cust_id)
    context = {}

    if request.method == 'POST' :
        customer.delete()
        return redirect('dashboard')
    context['customer'] = customer
    return render(request, 'accounts/form_templates/remove_customer.html', context)