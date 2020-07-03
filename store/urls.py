from django.contrib import admin
from django.urls import path

from store import views

urlpatterns = [
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('', views   .store, name="store")
]
