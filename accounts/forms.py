from django.forms import ModelForm
from .models import(
    Order,
)

class CreateOrderForm(ModelForm) :
    class Meta :
        model = Order
        fields = '__all__'      # create a form with all the fields in the Order Model,