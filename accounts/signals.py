from django.db.models.signals import (
    # pre_save,
    post_save,
)
from .models import (
    Customer,
)
from django.contrib.auth.models import User, Group

def create_customer_profile(sender, instance, created, **kwargs) :
    print("create_customer_profile with created : %s" % created)
    if created :
        instance.groups.add(Group.objects.get(name='customers'))

        print("added " + str(instance) + " to " + str(instance.groups.all()))


        new_customer = Customer.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email,
        )

        print(str(new_customer) + " for " + str(instance))

post_save.connect(create_customer_profile, sender=User)