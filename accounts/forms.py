from django.forms import ModelForm, widgets
from .models import(
    Order,
    Customer,
    Product,
)

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class OrderForm(ModelForm) :
    class Meta :
        model = Order
        fields = '__all__'      # create a form with all the fields in the Order Model,
    
class CustomerForm(ModelForm) :
    class Meta :
        model = Customer
        fields = '__all__'

class ProductForm(ModelForm) :
    class Meta :
        model = Product
        fields = '__all__'


class RegisterForm(UserCreationForm) :
    class Meta :
        model = User
        fields = ['email', 'username', 'password1', 'password2',]
        widgets = {
            'email': widgets.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'username': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
            'password1': widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password1'}),
            'password2': widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password2'}),
        }

class LoginForm(UserCreationForm) :
    class Meta :
        model = User
        fields = ['email', 'password']
        widgets = {
            'email': widgets.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}),
        }