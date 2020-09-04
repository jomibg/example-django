"""VCDev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from blog.views import IndexView,donate_index,charge,successMSG
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',IndexView.as_view(),name='home'),
    path('accounts/',include('accounts.urls',namespace='accounts')),
    path('',include('django_registration.backends.activation.urls')),
    path('blog/',include('blog.urls',namespace='blog')),
    path('donate/',donate_index,name='donate'),
    path('charge/',charge,name='charge'),
    path('donate/<str:amount>/success',successMSG,name='donate_success'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''django_registration_register is the account-registration view.
django_registration_complete is the post-registration success message.
django_registration_activate is the account-activation view.
django_registration_activation_complete is the post-activation success message.
django_registration_disallowed is a message indicating registration is not currently permitted'''