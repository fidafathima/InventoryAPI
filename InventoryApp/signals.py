# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .utils import send_order_confirmation_email

@receiver(post_save, sender=Order)
def send_confirmation_on_order_confirmed(sender, instance, **kwargs):
    if instance.order_status == 'confirmed':  # Check if the status is confirmed
        send_order_confirmation_email(instance)
