from django_filters import (
    FilterSet,
    DateFilter,
    CharFilter,
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
    start_date = DateFilter(field_name='date_created', lookup_expr='gte')
    end_date = DateFilter(field_name='date_created', lookup_expr='lte')
    description = CharFilter(field_name='description', lookup_expr='icontains')
    class Meta :
        model = Product
        fields = '__all__'
        exclude = ['date_created',]