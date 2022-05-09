from ctypes import addressof
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import datetime
from .models import *



# Create your views here.
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, isCompleted=False)
        items = order.orderitem_set.all() # parent_model.lowercaseed_child_set.querySet()
        total_item = order.get_total_item;
    else:
        items = []
        order = {'get_grand_total':0, 'get_total_item': 0, 'shipping':False}
        total_item = order['get_total_item']
        
    products = Product.objects.all()
    context = {'products': products, 'total_item': total_item}
    return render(request,'store/store.html', context=context)

def cart(request):
    '''
    if the user is authenticated
    set customer to req.user.customer (the current logged in user)
    get_or_create() return a tuple i.e (object, created) 
    items: grabbing all the orderItem (backward relationship more on this : https://docs.djangoproject.com/en/4.0/topics/db/queries/#following-relationships-backward)
    '''
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, isCompleted=False)
        items = order.orderitem_set.all() # parent_model.lowercaseed_child_set.querySet()
        total_item = order.get_total_item;

    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        print(cart)
        items = []
        order = {'get_grand_total':0, 'get_total_item': 0, 'shipping':False}
        total_item = order['get_total_item']

        for i in cart:
            total_item += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_grand_total'] += total
            order['get_total_item'] += cart[i]['quantity']

    
    context = {'items': items, 'order': order, 'total_item': total_item}
    return render(request,'store/cart.html', context=context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, isCompleted=False)
        items = order.orderitem_set.all() # parent_model.lowercaseed_child_set.querySet()
        total_item = order.get_total_item;
    else:
        items = []
        order = {'get_grand_total':0, 'get_total_item': 0, 'shipping':False}
        total_item = len(items)

    
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
        # orderItem.quantity = (orderItem.quantity + 1)
        orderItem.quantity += 1
    elif action == 'remove':
        # orderItem.quantity = (orderItem.quantity - 1)
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