from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import UpdateView
from django.contrib.auth.models import User
# Create your views here.

class ProfileUpdate(UserPassesTestMixin,UpdateView):
	model=User
	fields=['username','email']
	template_name='registration/profile_form.html'
	def test_func(self):
		userobj=User.objects.get(pk=self.kwargs['pk'])
		return userobj == self.request.user
