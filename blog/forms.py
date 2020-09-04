from django import forms
from .models import *
from django.core.validators import FileExtensionValidator
class ReviewForm(forms.ModelForm):
	class Meta:
		model=Review
		exclude=['user']
		widgets={
		'content':forms.Textarea(attrs={'rows': '10','maxlength':'1000','class':'form-control'}),
		'marks':forms.Select(attrs={}),
		}

class OrderForm(forms.ModelForm):
	class Meta:
		model=Order
		exclude=['customer_activity','created_date']
		widgets={
		'subject':forms.TextInput(attrs={'style':'width:500px;',}),
		'description':forms.Textarea(attrs={'rows': '20','style':'width:800px;'}),
		}
		validators={
		'additional_files':FileExtensionValidator(allowed_extensions=['docx','pdf'])
		}
