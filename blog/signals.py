from django.db.models.signals import post_save,pre_save,pre_delete
from django.dispatch import receiver
from .models import *
from django.contrib.auth.models import User,Group
from datetime import date
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail

 
@receiver(post_save,sender=User)
def create_info(sender,instance,created,**kwargs):
	if created:
		ActivityInfo.objects.create(user=instance)
		print("Info created!")
		if not instance.is_staff or not instance.is_superuser:
			group=Group.objects.get(name='customers')
			instance.groups.add(group)
	else:
		instance.activity.save()
		print("acitivty updated")
		


@receiver(pre_save,sender=Order)
def order_pre(sender,instance,**kwargs):
	if instance.customer_activity.last_order_date !=  date.today():
		instance.customer_activity.orders_num=0
		instance.customer_activity.save()
	if instance.customer_activity.orders_num >= 3:
		raise PermissionDenied('Have passed orders-per-day limit!')
		

@receiver(post_save,sender=Order)
def order_create(sender,instance,created,**kwargs):
	if created:
		instance.customer_activity.orders_num+=1
		instance.customer_activity.last_order_date=instance.created_date
		instance.customer_activity.save()
@receiver(pre_delete,sender=Order)
def order_delete(sender,instance,**kwargs):
	if instance.created_date == date.today():
		instance.customer_activity.orders_num-=1
		instance.customer_activity.save()
