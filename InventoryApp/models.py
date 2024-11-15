import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class ProductDetails(models.Model):
    ProductID = models.BigIntegerField(unique=True)
    ProductCode = models.CharField(max_length=255, unique=True)
    ProductName = models.CharField(max_length=255)
    ProductImage = models.ImageField(upload_to="uploads/", blank=True, null=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdatedDate = models.DateTimeField(blank=True, null=True)
    IsFavourite = models.BooleanField(default=False)
    Active = models.BooleanField(default=True)
    TotalStock = models.DecimalField(default=0.00, max_digits=20, decimal_places=8, blank=True, null=True)

    class Meta:
        db_table = "products_product"
        verbose_name = ("product")
        verbose_name_plural = ("products")
        unique_together = (("ProductCode", "ProductID"),)
        ordering = ("-CreatedDate", "ProductID")



class Customer(AbstractUser):
  is_customer=models.BooleanField(default=False)
  name = models.CharField(max_length=100)
  contact_no = models.CharField(max_length=100)
  email = models.EmailField()
  address = models.TextField()

  def __str__(self):
    return self.name


class Cart(models.Model):
  user = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
  item = models.ForeignKey(ProductDetails, on_delete=models.DO_NOTHING)
  quantity0=models.CharField(max_length=15,default=1)
  status = models.CharField(default=0)


class Delivery(models.Model):
    user=models.ForeignKey(Customer,on_delete=models.DO_NOTHING)
    name=models.CharField(max_length=100,default=None,null=True)
    address=models.TextField(default=None,null=True)
    state=models.CharField(max_length=100,default=None,null=True)
    district=models.CharField(max_length=100,default=None,null=True)
    place = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)
    pincode = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)
    status=models.CharField(max_length=10)

class PaymentMethod(models.Model):

        PAYMENT_METHOD_CHOICES = [
            ('card', 'Card'),
            ('upi', 'UPI'),
            ('cod', 'Cash on Delivery'),
        ]
        method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES,default="cod")
        status = models.CharField(max_length=50, default="Pending")  # e.g., Pending, Completed, Failed

        def __str__(self):
            return f"{self.method} - {self.status}"


class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    delivery = models.ForeignKey(Delivery, on_delete=models.DO_NOTHING, default=1)
    payment = models.ForeignKey(PaymentMethod, on_delete=models.DO_NOTHING, default=1)
    product = models.ManyToManyField(Cart)
    amount = models.CharField(max_length=10, default=0)
    date = models.DateField(auto_now=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    customer_email = models.EmailField()
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    cancel_order = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.order_status}"
