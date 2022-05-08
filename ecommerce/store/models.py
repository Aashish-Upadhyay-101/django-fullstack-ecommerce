from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(blank=True, unique=True, error_messages={
        'unique': 'An account with this email alread exist.'
    })

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    isDigital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(upload_to='product_image/', null=True, blank=True)

    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.name

    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    isCompleted = models.BooleanField(default=False, blank=True, null=True)
    transaction_id = models.CharField(max_length=10, null=True);


    @property
    def get_grand_total(self):
        orderItem = self.orderitem_set.all()
        grand_total = sum([(item.quantity * item.product.price) for item in orderItem])
        return grand_total 
    
    @property
    def get_total_item(self):
        orderItem = self.orderitem_set.all()
        total_quantity = sum([item.quantity for item in orderItem])
        return total_quantity


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_item_total(self):
        total = self.quantity * self.product.price 
        return total



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=50, null=False)
    state = models.CharField(max_length=50, null=False)
    zipcode = models.CharField(max_length=20, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address



        