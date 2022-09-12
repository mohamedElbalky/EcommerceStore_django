from operator import sub
from celery import Celery

from django.core.mail import send_mail
from django.conf import settings
from .models import Order


app = Celery()

@app.task
def order_created(order_id):
    """
        task to send an email 
        notification when an order os successfully created
    """
    order = Order.objects.get(id=order_id)
    subject = f"Order no.{order.id}"
    message = f"""
        Dear {order.first_name},
        you have successfully placed an order.
        your order ID is {order.id}.
    """
    mail_send = send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[order.email]
        
    )
    return mail_send
