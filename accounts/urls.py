from django.urls import path
from .views import(
    homePageView,
    dashboardView,
    logoutView,
    productsView,
    statusView,
    customerView,
    createOrderView,
    updateCustomerView,
    createCustomerView,
    removeCustomerView,
    createProductView,
    removeProductView,
    registerView,
    loginView,
    userHomePageView,
    accountSettingsView,
)

urlpatterns = [
    # path('admin/', admin,site.urls),

    path('', homePageView, name='home'),
    path('userHome/', userHomePageView, name='userHome'),

    path('register/', registerView, name='register'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),

    path('dashboard/', dashboardView, name='dashboard'),
    path('products/', productsView, name='products'),
    path('status/', statusView, name='status'),
    path('customer/<str:pk_cust_id>/', customerView, name='customer'),

    # path('createOrder/', createOrderView, name='createOrder'),
    path('createOrder/<str:pk_cust_id>/', createOrderView, name='createOrder'),
    path('createCustomer/', createCustomerView, name='createCustomer'),
    path('createProduct/', createProductView, name='createProduct'),

    path('updateCustomer/<str:pk_cust_id>/', updateCustomerView, name='updateCustomer'),

    path('removeCustomer/<str:pk_cust_id>/', removeCustomerView, name='removeCustomer'),
    path('removeProduct/<str:pk_product_id>/', removeProductView, name='removeProduct'),

    path('accountSettings/', accountSettingsView, name='accountSettings'),
]