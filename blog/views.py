from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import *
from .forms import *
from django.http import HttpResponse,JsonResponse
from .decorators import customers_only
from django.utils.decorators import method_decorator
from django.core.mail import send_mail,mail_admins
from datetime import date
# Create your views here. 
class IndexView(TemplateView):
	template_name='index.html'


 
#############Reviews###########################
class ReViewDetail(DetailView):
	model=Review
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['user']=self.request.user
		return context
		
class ReViewList(ListView):
	model=Review
	context_object_name='reviews'
	def get_queryset(self):
		return Review.objects.all().order_by('mark')

#@method_decorator(login_required, name='dispatch')
class CreateReView(LoginRequiredMixin,CreateView):
	model=Review
	form_class =ReviewForm
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class UpdateReView(UserPassesTestMixin,UpdateView):
	model=Review
	form_class=ReviewForm
	raise_exception=True
#msms da po defaultu podiže grešku ako je user ulogovan,a ne prolazi test
#ovako još izbacuje grešku kad neulogovan user proba da pristupi
	def test_func(self):
		obj=Review.objects.get(pk=self.kwargs['pk'])
		return obj.user==self.request.user

class DeleteReView(UserPassesTestMixin,DeleteView):
	model = Review
	success_url = reverse_lazy('blog:review_list')
	def test_func(self):
		obj=Review.objects.get(pk=self.kwargs['pk'])
		return obj.user==self.request.user
#############Orders###########################
@method_decorator(customers_only, name='dispatch')
class UserOrdersList(LoginRequiredMixin,ListView):
	model=Order
	context_object_name='orders'
	def get_queryset(self):
		return Order.objects.filter(customer_activity__user=self.request.user).order_by('created_date')

class AdminOrdersList(UserPassesTestMixin,ListView):
	model=Order
	context_object_name='orders'
	template_name='blog/admin_orders_list.html'
	raise_exception=True
	def test_func(self):
		isss=self.request.user.is_staff or self.request.user.is_superuser
		return isss
	def get_queryset(self):
		return Order.objects.all().order_by('created_date')

class OrderDetail(UserPassesTestMixin,DetailView):
	model=Order
	def test_func(self):
		customer_activity=ActivityInfo.objects.get(user=self.request.user)
		obj=Order.objects.get(pk=self.kwargs['pk'])
		metching=customer_activity == obj.customer_activity
		isss=self.request.user.is_staff or self.request.user.is_superuser
		return metching or isss

class OrderCreate(LoginRequiredMixin,CreateView):
	model=Order
	form_class=OrderForm
	def form_valid(self, form):
		customer_activity=ActivityInfo.objects.get(user=self.request.user)
		form.instance.customer_activity =customer_activity
		subject='\"'+form.instance.subject+'\"' +' from: ' +str(customer_activity)
		body=form.instance.description
		try:
			mail_admins(subject,body,fail_silently=False,)
			return super().form_valid(form)
		except:
			subject='SPAM REPORT user: ' + str(customer_activity)
			body='This user has passed orders-per-day limit!' + str(date.today())
			mail_admins(subject,body,fail_silently=False)
			return HttpResponse('<h1>You have passed orders-per-day limit!</h1>')
			
class OrderDelete(UserPassesTestMixin,DeleteView):
	model=Order
	success_url=reverse_lazy('blog:order_list')
	def get_success_url(self):
		if self.request.user.is_staff or self.request.user.is_superuser:
			self.success_url=reverse_lazy('blog:admin_orders')
			return self.success_url
		return self.success_url
	def test_func(self):
		customer_activity=ActivityInfo.objects.get(user=self.request.user)
		obj=Order.objects.get(pk=self.kwargs['pk'])
		metching=customer_activity == obj.customer_activity
		isss=self.request.user.is_staff or self.request.user.is_superuser
		return metching or isss
###############Donations####################################
import stripe
stripe.api_key = "sk_test_2PTkgznHaLBPLSX2KxjosvmP00HCdioOU0"


def donate_index(request):
	user=request.user
	context={'user':user }
	return render(request,'donate.html',context)

def charge(request):
	if request.method=='POST':
		print('Data:',request.POST)
	amount=int(request.POST['amount'])
	customer=stripe.Customer.create(name=request.user,email=request.user.email,
		source=request.POST['stripeToken'])

	charge=stripe.Charge.create(
  customer=customer,
  amount=amount*100,
  currency="usd",
)
	return redirect(reverse_lazy('donate_success',args=[amount]))
def successMSG(request,amount):
	return render(request,'donate-success.html',{'amount':amount})





