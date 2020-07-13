from django.contrib import admin
from django.urls import path

from store import views

urlpatterns = [
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('', views   .store, name="store"),
    path('update_item/', views.update_item, name="Update"),
    path('process_order/', views.process_order, name="Process Order"),
]
