from django.urls import path,include 
app_name='accounts' 
from django.contrib.auth import views as av
from django.urls import reverse_lazy 
from .decorators import *
from .views import *
urlpatterns = [
path('login/',redirect_authenticated(av.LoginView.as_view())
	,name='login'),
path('logout/',av.LogoutView.as_view(next_page='/'),name='logout'),
path('password_reset/',av.PasswordResetView.as_view(
	success_url=reverse_lazy('accounts:reset_done')),
name='password_reset'),
path('reset/done/',av.PasswordResetDoneView.as_view(),name='reset_done'),
path('reset/<uidb64>/<token>/',av.PasswordResetConfirmView.as_view(
	success_url=reverse_lazy('accounts:reset_complete')),name='reset_confirm'),
path('reset/complete/',av.PasswordResetCompleteView.as_view(),name='reset_complete'),
path('change_info/<int:pk>/',ProfileUpdate.as_view(success_url=reverse_lazy('home')),name='ch_info'),
path('change_password/',av.PasswordChangeView.as_view(success_url=reverse_lazy('home')),name='password_change'),
] 