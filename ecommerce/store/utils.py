import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print(cart)
    items = []
    order = {'get_grand_total':0, 'get_total_item': 0, 'shipping':False}
    total_item = order['get_total_item']

    for i in cart:
        try:
            total_item += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_grand_total'] += total 
            order['get_total_item'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageUrl': product.imageUrl,
                },
                'quantity': cart[i]['quantity'],
                'get_item_total': total
            }

            items.append(item) 

            if product.isDigital == False:
                order['shipping'] = True 
        except:
            pass

    return {'items': items, 'order': order, 'total_item': total_item}


def cartData(request):
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
        cookieData = cookieCart(request)
        total_item = cookieData['total_item']
        order = cookieData['order']
        items = cookieData['items']

    return {'items': items, 'order': order, 'total_item': total_item}