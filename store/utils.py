import json
from .models import *


def cookie_cart(request):
    if request.COOKIES['cart'] is not None:
        cart_cookie = json.loads(request.COOKIES['cart'])
    else:
        cart_cookie = {}
    items = []
    order = {"get_cart_total": 0, "get_cart_items": 0}
    cart_items = order['get_cart_items']

    for i in cart_cookie:
        try:

            cart_items += cart_cookie[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart_cookie[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart_cookie[i]['quantity']

            item = {
                'product': {
                    "id": product.id,
                    'name': product.name,
                    'price': product.price,
                    'image_url': product.image_url
                },
                'quantity': cart_cookie[i]['quantity'],
                'get_total': total
            }

            items.append(item)

            order['shipping'] = not product.digital
        except:
            pass
    return {'cart_items': cart_items, 'order': order, 'items': items}


def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        cookie_data = cookie_cart(request)
        items = cookie_data['items']
        cart_items = cookie_data['cart_items']
        order = cookie_data['order']

    return {'cart_items': cart_items, 'order': order, 'items': items}


def get_order(request, data):
    print("Not authenticate!")
    name = data['form']['name']
    email = data['form']['email']

    cookie_data = cookie_cart(request)
    items = cookie_data['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
        name=name
    )

    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        order_item = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )

    return customer, order
