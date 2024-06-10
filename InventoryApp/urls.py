
from django.urls import path

from InventoryApp import views

urlpatterns = [
   path('product', views.Product.as_view(), name='product'),
   path('LoginView',views.LoginView.as_view(),name='LoginView'),
   path('Product1',views.Product1.as_view(),name='Product1'),
   path('size',views.size.as_view(),name='size'),
   path('color',views.color.as_view(),name='color')
]
