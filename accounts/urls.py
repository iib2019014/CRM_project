from django.urls import path
from .views import(
    homePageView,
    dashboardView,
    productsView,
    statusView,
    customerView,
)

urlpatterns = [
    # path('admin/', admin,site.urls),
    path('', homePageView, name='home'),
    path('dashboard/', dashboardView, name='dashboard'),
    path('products/', productsView, name='products'),
    path('status/', statusView, name='status'),
    path('customer/<str:pk_cust_id>/', customerView, name='customer'),
]