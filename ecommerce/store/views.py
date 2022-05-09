from ctypes import addressof
import json
from math import prod
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import datetime
from .models import *
from .utils import cartData, cookieCart


# Create your views here.
def store(request):
    data = cartData(request)
    total_item = data['total_item']
    order = data['order']
    items = data['items']
        
    products = Product.objects.all()
    context = {'products': products, 'total_item': total_item}
    return render(request,'store/store.html', context=context)

def cart(request):
    data = cartData(request)
    total_item = data['total_item']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'total_item': total_item}
    return render(request,'store/cart.html', context=context)

def checkout(request):
    data = cartData(request)
    total_item = data['total_item']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'total_item': total_item}

    return render(request,'store/checkout.html', context=context)


def updateItem(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']

    print('Action:', action)
    print('Product Id:', product_id)

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    print(product)
    order, created = Order.objects.get_or_create(customer=customer, isCompleted=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    print(orderItem.quantity)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def process_order(request):
    data = json.loads(request.body)
    print(data)

    transaction_id = datetime.datetime.now().timestamp();

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, isCompleted=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

    else:
        print("COOKIES", request.COOKIES)
        name = data['form']['name']
        email = data['form']['email']

        cookieData = cookieCart(request)
        items = cookieData['items']

        customer, created = Customer.objects.get_or_create(email=email)
        customer.name = name
        customer.save()

        order = Order.objects.create(customer=customer, isCompleted=False)

        for item in items:
            product = Product.objects.get(id=item['product']['id'])
            orderItem = OrderItem.objects.create(product=product, order=order, quantity=item['quantity'])

    if total == order.get_grand_total:
        order.isCompleted = True 
    
    order.save() 

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order, 
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )
    return JsonResponse("Payment success...", safe=False)  