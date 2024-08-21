from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('myorders/', views.my_orders, name='my_orders'),

    path('dashboard/admin/orders/', views.orders_admin, name='orders_admin'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),

    path('dashboard/admin/foods/add_food/', views.add_food, name='add_food'),
    re_path(r'^dashboard/admin/orders/confirm_delivery/(?P<orderID>\d+)/$', views.confirm_delivery, name='confirm_delivery'),
    
    re_path(r'^delete_item/(?P<ID>\d+)/$', views.delete_item, name='delete_item'),
    path('placeOrder/', views.placeOrder, name='placeOrder'),
    re_path(r'^addTocart/(?P<foodID>\d+)/$', views.addTocart, name='addTocart'),
]
