from django.db import models
from django.db.models.deletion import SET_NULL

STATUS = (
    ('pending', 'pending'),
    ('out for delivery', 'out for delivery'),
    ('delivered', 'delivered'),
)

CATEGORY = (
    ('indoor', 'indoor'),
    ('outdoor', 'outdoor'),
)


# Create your models here.
class Customer(models.Model) :
    name = models.CharField(max_length=25, null=True)
    phone = models.CharField(max_length=10, null=True)
    eamil = models.CharField(max_length=25, null=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) :
        return self.name

class Tag(models.Model) :
    name = models.CharField(max_length=25, null=True)
    id = models.CharField(max_length=25, primary_key=True)

    def __str__(self) :
        return self.name

class Product(models.Model) :
    name = models.CharField(max_length=25, null=True)
    description = models.CharField(max_length=25, null=True)
    category = models.CharField(max_length=25, null=True, choices=CATEGORY)
    product_id = models.CharField(max_length=10, primary_key=True)
    price = models.FloatField(null=True)
    tags = models.ManyToManyField(Tag)

    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) :
        return self.name
    
class Order(models.Model) :
    order_id = models.CharField(max_length=25, primary_key=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=SET_NULL)   # when the customer is deleted we want this customer attribute to be null,
    product = models.ForeignKey(Product, null=True, on_delete=SET_NULL)
    # product = models.ManyToOneRel()
    status = models.CharField(max_length=25, null=True, choices=STATUS)

    def __str__(self) :
        return "order [" + self.order_id + "]"