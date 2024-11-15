# utils.py (or another utility file)
from django.core.mail import send_mail
from django.conf import settings


def send_order_confirmation_email(order):
    subject = 'Your Order is Confirmed!'
    message = f'Hello,\n\nYour order with ID {order.id} has been confirmed! We are preparing it for shipment.\n\nThank you for shopping with us!'
    recipient_list = [order.delivery.user.email]

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )
