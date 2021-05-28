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
        try :
            user_group = Group.objects.get(name='customers')
            instance.groups.add(user_group)
            print("added " + str(instance) + " to " + str(instance.groups.all()))
        except Group.DoesNotExist :
              pass  


        new_customer = Customer.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email,
        )

        print(str(new_customer) + " for " + str(instance))

post_save.connect(create_customer_profile, sender=User)