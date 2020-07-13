import datetime
import json

from django.shortcuts import render
from .models import *
from django.http import JsonResponse

# Create your views here.
from .utils import cookie_cart, cart_data, get_order


def store(request):
    data = cart_data(request)

    products = Product.objects.all()
    context = {
        'products': products,
        'cart_items': data['cart_items']
    }
    return render(request, 'store/store.html', context)


def cart(request):
    context = cart_data(request)

    return render(request, 'store/cart.html', context)


def checkout(request):
    context = cart_data(request)
    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(product_id)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderitem.quantity += 1
    elif action == 'remove':
        orderitem.quantity -= 1

    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()
    return JsonResponse("Item was added", safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = get_order(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse("Payment complete!", safe=False)
