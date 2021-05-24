from django_filters import (
    FilterSet,
    DateFilter,
)

from .models import (
    Order,
    Product,
)

class OrderFilter(FilterSet) :
    # my custom attributes,
    start_date = DateFilter(field_name='date_ordered', lookup_expr='gte')
    end_date = DateFilter(field_name='date_ordered', lookup_expr='lte')
    class Meta :
        model = Order
        # fields = ('product', 'status', 'date_ordered')
        fields = '__all__'
        exclude = ['customer', 'date_ordered']




































    
class ProductFilter(FilterSet) :
    class Meta :
        model = Product
        fields = '__all__'