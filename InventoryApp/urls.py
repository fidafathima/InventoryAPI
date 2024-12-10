
from django.urls import path

from InventoryApp import views

urlpatterns = [

   path('product', views.Product.as_view(), name='product'),
   path('LoginView',views.LoginView.as_view(),name='LoginView'),
   path('Product1',views.Product1.as_view(),name='Product1'),
   path('PDetail/<int:id>/',views.PDetail.as_view(),name="PDetail"),
   path('customer', views.customer.as_view(), name='customer'),
   path('AddToCart/<int:id>/',views.AddToCart.as_view(),name='AddToCart'),
   path('CartView',views.CartView.as_view(),name='CartView'),
   path('ChangeQuantity/<int:id>/',views.ChangeQuantity.as_view(),name='ChangeQuantity'),
   path('Remove/<int:id>/',views.Remove.as_view(),name='Remove'),
   path('RemoveItem/<int:id>/',views.RemoveItem.as_view(),name='RemoveItem'),
   path('address',views.address.as_view(),name='address'),
   path('ChangeAddress/<int:id>/',views.ChangeAddress.as_view(),name='ChangeAddress'),
   path('CheckOut',views.CheckOut.as_view(),name='CheckOut'),
   path('payment/<int:id>/',views.payment.as_view(),name='payment'),
   path('orders',views.orders.as_view(),name='orders')


]
