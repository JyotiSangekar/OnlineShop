import logging
from onlineshop.celery import app
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail, EmailMessage
from orders.models import Order, OrderItem
from paypal.standard.ipn.models import  PayPalIPN
from onlineshop.settings import PAYPAL_RECEIVER_EMAIL, THEME_CONTACT_EMAIL
from django.template.loader import render_to_string, get_template
from django.template import Context


@app.task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    order = Order.objects.get(id=order_id)
    order = get_object_or_404(Order, id=order_id)
    ordereditem = get_object_or_404(OrderItem, order=order.id)    
    subject = "Order has been created successfully"
    to = [order.email]
    from_email = "admin@myshop.com"

    ctx = {
        'first_name' : order.first_name,
        'last_name' : order.last_name,
        'email' : order.email,
        'address' : order.address,
        'postal_code' : order.postal_code,
        'city' : order.city,
        'created' : order.created,
        'updated' : order.updated,
        'Order_Number': ordereditem.order,
        'product' : ordereditem.product,
        'price' : ordereditem.price,
        'quantity' : ordereditem.quantity,                   
    }
    message = get_template('payment/email.html').render(ctx)
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()

    return msg.send()

@app.task
def order_paymentfail(order_id):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = 'Error Purchasing Order nr. {}'.format(order.id)
    message = 'Dear {},\n\nPayment Not Confirmed, Kindly contact your support or payment institution. Your order id is {}.'.format(order.first_name, order.id)
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email], fail_silently=False)
    return mail_sent

@app.task
def order_paymentsuccesstopaid(order_id):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    order = Order.objects.get(id=order_id)
    order = get_object_or_404(Order, id=order_id)
    ordereditem = get_object_or_404(OrderItem, order=order.id)    
    subject = "Order was SuccessFull"
    to = [order.email]
    from_email = "admin@myshop.com"

    ctx = {
        'first_name' : order.first_name,
        'last_name' : order.last_name,
        'email' : order.email,
        'address' : order.address,
        'postal_code' : order.postal_code,
        'city' : order.city,
        'created' : order.created,
        'updated' : order.updated,
        'Order_Number': ordereditem.order,
        'product' : ordereditem.product,
        'price' : ordereditem.price,
        'quantity' : ordereditem.quantity,                   
    }
    message = get_template('payment/email.html').render(ctx)
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()

    return msg.send()
