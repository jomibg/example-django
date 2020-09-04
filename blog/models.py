from django.db import models  
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
 
def MinLen(value):
	if len(value) < 50:
		raise ValidationError(
			('Description must contain more than 100 characters!'),
			params={'value': value},)
   
marks=[('one','*'),('two','**'),('three','***'),('four','****'),('five','*****')]
class Review(models.Model):
	user=models.OneToOneField('auth.User',on_delete=models.SET_NULL,null=True)
	content=models.TextField()
	mark=models.CharField(max_length=5,choices=marks,default=marks[0][0])
	def __str__(self):
		return self.content[:30]
	def get_absolute_url(self):
		return reverse("blog:review_detail",kwargs={'pk':self.pk})
class ActivityInfo(models.Model):
	user=models.OneToOneField('auth.User',on_delete=models.CASCADE,related_name='activity')
	orders_num=models.IntegerField(default=0)
	last_order_date=models.DateField(blank=True,null=True)
	def __str__(self):
		return str(self.user)

class Order(models.Model):
	customer_activity=models.ForeignKey(ActivityInfo,on_delete=models.SET_NULL,related_name='orders',null=True)
	subject=models.CharField(max_length=200)
	description=models.TextField(validators=[MinLen])
	created_date = models.DateField(default=date.today())
	additional_files=models.FileField(upload_to='orders_files/%Y/%m.%d/',blank=True,null=True,
		validators=[FileExtensionValidator(allowed_extensions=['docx','pdf'])])
	def __str__(self):
		return self.subject
	def delete(self,*args,**kwargs):
		self.additional_files.delete()
		super().delete(*args,**kwargs)



		