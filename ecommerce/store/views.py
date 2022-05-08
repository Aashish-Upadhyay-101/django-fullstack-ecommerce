from django.shortcuts import render
from django.http import HttpResponse
from .models import *


# Create your views here.
def store(request):
    products = Product.objects.all()
    context = {'products': products}
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
    else:
        items = []
        order = {'get_grand_total':0, 'get_total_item': 0}
    
    context = {'items': items, 'order': order}
    return render(request,'store/cart.html', context=context)

def checkout(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, isCompleted=False)
        items = order.orderitem_set.all() # parent_model.lowercaseed_child_set.querySet()
    else:
        items = []
    
    context = {'items': items, 'order': order}

    return render(request,'store/checkout.html', context=context)

