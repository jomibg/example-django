from django.urls import path,reverse_lazy
from .views import *
app_name='blog'
urlpatterns=[
path('review/<int:pk>',ReViewDetail.as_view(),name='review_detail'),
path('reviews/',ReViewList.as_view(),name='review_list'),
path('review/new',CreateReView.as_view(),name='review_create'),
path('reviews/<int:pk>/update',UpdateReView.as_view(),name='review_update'),
path('reviews/<int:pk>/delete',DeleteReView.as_view(),name='review_delete'),
path('orders_admin/',AdminOrdersList.as_view(),name='admin_orders'),
path('orders/',UserOrdersList.as_view(),name='order_list'),
path('order/write',OrderCreate.as_view(success_url=reverse_lazy('home')),name='order_create'),
path('order/<int:pk>',OrderDetail.as_view(),name='order_detail'),
path('order/<int:pk>/delete',OrderDelete.as_view(),name='order_delete'),

]