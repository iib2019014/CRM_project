from django.shortcuts import render, redirect

from .models import(
    Product,
    Customer,
    Order,
)

from .forms import(
    OrderForm,
    CustomerForm,
    ProductForm,
    UserCreationForm,
    RegisterForm,
    LoginForm,
)

from django.forms import inlineformset_factory

from .filters import (
    OrderFilter,
    ProductFilter,
)

from django.contrib import messages

from django.contrib.auth import (
    authenticate,
    login,
    logout,
)

from django.contrib.auth.decorators import login_required

from .decorators import (
    authentication_required,
    user_allowed,
    admin_only,
)

from django.contrib.auth.models import Group

# Create your views here.

@login_required(login_url='login')
@admin_only
def homePageView(request) :
    context = {}
    if request.user.groups.exists() :
        user_groups = request.user.groups.all()
        context['user_groups'] = user_groups
        # print(user_groups)
    print(context)
    return render(request, 'accounts\home_page.html', context)

@login_required(login_url='login')
@user_allowed(allowed_users=['customers'])
def userHomePageView(request) :
    context = {}
    user_customer = request.user.customer
    context['user_customer'] = user_customer

    customer_orders = user_customer.order_set.all()
    context['customer_orders'] = customer_orders
    context['total_orders'] = customer_orders.count()
    context['delivered_orders'] = customer_orders.filter(status="delivered").count()
    context['pending_orders'] = customer_orders.filter(status="pending").count()
    
    if request.user.groups.exists() :
        user_group = request.user.groups.all()[0].name
        context['user_group'] = user_group
    return render(request, 'accounts\\user_page.html', context)

@authentication_required
def registerView(request) :
    # register_form = UserCreationForm()
    register_form = RegisterForm()
    context = {}

    if request.method == 'POST' :
        print("into post")
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid() :
            print("valid")
            user = register_form.save()

            user.groups.add(Group.objects.get(name='customers'))    # add the registered customer to the 'customers' group,
            Customer.objects.create(
                user=user,      # whenever a user is registered assign that user a customer profile,
            )
            
            messages.success(request, "an account was successfully registered for " + register_form.cleaned_data.get('username'))
            return redirect('home')
        else :
            print("not valid")
    else :
        print("into get")
    context['register_form'] = register_form
    return render(request, 'accounts/registration/register.html', context)

@authentication_required
def loginView(request) :
    login_form = LoginForm()
    context = {}

    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')

        logged_in_user = authenticate(request, username=username, password=password)

        print(logged_in_user)

        if logged_in_user is not None :
            login(request, logged_in_user)
            return redirect('home')
        else :
            messages.error(request, "invalid credentials")

    context['login_form'] = login_form
    return render(request, 'accounts/registration/login.html', context)

def logoutView(request) :
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@user_allowed(allowed_users=['admins'])
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
    context['delivered_orders'] = orders_delivered

    orders_pending = orders.filter(status="pending").count()
    context['pending_orders'] = orders_pending

    return render(request, 'accounts\dashboard.html', context)

@login_required(login_url='login')
@user_allowed(allowed_users=['admins'])
def productsView(request) :
    context = {}
    products = Product.objects.all()
    productFilter = ProductFilter(request.GET, queryset=products)
    products = productFilter.qs
    context['products'] = products
    context['productFilter'] = productFilter
    return render(request, 'accounts\products.html', context)

@login_required(login_url='login')
@user_allowed(allowed_users=['admins'])
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

@login_required(login_url='login')
@user_allowed(allowed_users=['admins', 'customers'])
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

@login_required(login_url='login')
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

@login_required(login_url='login')
def statusView(request) :
    context = {}
    return render(request, 'accounts/status.html', context)

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
def removeCustomerView(request, pk_cust_id) :
    customer = Customer.objects.get(id=pk_cust_id)
    context = {}

    if request.method == 'POST' :
        customer.delete()
        return redirect('dashboard')
    context['customer'] = customer
    return render(request, 'accounts/form_templates/remove_customer.html', context)

@login_required(login_url='login')
def removeProductView(request, pk_product_id) :
    product = Product.objects.get(id=pk_product_id)
    context = {}
    context['product'] = product

    if request.method == 'POST' :
        product.delete()
        return redirect('products')
    return render(request, 'accounts/form_templates/remove_product.html', context)