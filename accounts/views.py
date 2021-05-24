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

from django.forms import inlineformset_factory

from .filters import (
    OrderFilter,
    ProductFilter,
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
    last_5_orders = orders.order_by('-date_ordered')[:5]
    context['last_5_orders'] = last_5_orders

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
    productFilter = ProductFilter(request.GET, queryset=products)
    products = productFilter.qs
    context['products'] = products
    context['productFilter'] = productFilter
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

    # their_orders_or_filtered = Order.objects.filter(customer=the_customer)
    their_orders_or_filtered = the_customer.order_set.all()
    context['their_orders_or_filtered'] = their_orders_or_filtered
    
    total_orders = their_orders_or_filtered.count()
    context['total_orders'] = total_orders

    customerOrderFilter = OrderFilter(request.GET, queryset=their_orders_or_filtered)
    context['customerOrderFilter'] = customerOrderFilter
    their_orders_or_filtered = customerOrderFilter.qs
    context['their_orders_or_filtered'] = their_orders_or_filtered

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
    Customer_Order_FormSet = inlineformset_factory(
        Customer,   # the parent model
        Order,   # the child model
        fields=(
            'product',
            'status'
        ),   # the child fields need to be in form
        extra=5    # no. of additional empty forms to be displayed,
    )
    customer = Customer.objects.get(id=pk_cust_id)
    context = {}
    # createOrderForm = OrderForm(
    #     initial={
    #         'customer': customer,
    #     }
    # )
    createOrderFormSet = Customer_Order_FormSet(instance=customer, queryset=Order.objects.none())
    print(createOrderFormSet.instance)

    if request.method == 'POST' :
        print("into post")
        createOrderFormSet = Customer_Order_FormSet(request.POST, instance=customer)
        if createOrderFormSet.is_valid() :
            print("valid")
            createOrderFormSet.save()
            print(createOrderFormSet)
            return redirect('dashboard')
        else :
            print("not valid")
            createOrderFormSet = Customer_Order_FormSet(instance=customer)
    context['createOrderFormSet'] = createOrderFormSet
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

def removeProductView(request, pk_product_id) :
    product = Product.objects.get(id=pk_product_id)
    context = {}
    context['product'] = product

    if request.method == 'POST' :
        product.delete()
        return redirect('products')
    return render(request, 'accounts/form_templates/remove_product.html', context)