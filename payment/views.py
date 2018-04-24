from decimal import Decimal
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from orders.models import Order, OrderItem
from django.views.decorators.csrf import csrf_exempt
from django.db.models.signals import pre_save, post_save
from paypal.standard.models import  ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.apps import apps
from paypal.standard.ipn.models import  PayPalIPN
from onlineshop.settings import PAYPAL_RECEIVER_EMAIL, THEME_CONTACT_EMAIL
from django.core.mail import send_mail, EmailMessage
from django.template import Context
from django.template.loader import render_to_string, get_template
from orders.tasks import *


def payment_process(request):
        order_id = request.session.get('order_id')
        # print (order_id)
        order = get_object_or_404(Order, id=order_id)
        host = request.get_host()
        
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': '%.2f' % order.get_total_cost().quantize(Decimal('.01')),
            'item_name': 'Order {}'.format(order.id),
            'invoice': str(order.id),
            'currency_code': 'USD',
            'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host, reverse('payment:success')),
            'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),
            'custom': order_id
        }
        # request.session.get['order_id'] = order_id
        form = PayPalPaymentsForm(initial=paypal_dict)
        return render(request, 'payment/process.html', {'form':form})

@csrf_exempt
def successView(request, sender=PayPalIPN, **kwargs):
    order_id = request.session.get('order_id')
    print("Get oredr from session")
    print (order_id)
    order = get_object_or_404(Order, id=order_id)
    print("print order query")
    print (order)
    ordereditem = get_object_or_404(OrderItem, order=order.id)
    print("orderitems")
    print(ordereditem)
    # ipn_obj = sender
    print("order processing ........"*400)
    # order_createdsendmail.delay(order_id)
    ipn_obj_confirm = PayPalIPN.objects.filter(custom=order_id)
    print (ipn_obj_confirm)
    # ipn_obj_confirm = ipn_obj.objects.filter(invoice=str(order_id))
    print ("Query set for paypal response from database")
    print (ipn_obj_confirm)
    for i in ipn_obj_confirm:
        if i.payment_status == "Completed":
            if i.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
                order_paymentfail.delay(order_id)
                print("Failed messgae sent")
                return render(request, 'payment/canceled.html')
            else:
                values_to_update = {'paid':True}
                obj_order, created = Order.objects.update_or_create(id=order_id, defaults=values_to_update )
                order_paymentsuccesstopaid(order_id)
                print ("Print success purchase message")  
                return render(request, 'payment/done.html')
        else:
            order_paymentfail.delay(order_id)
            print("Error sending messages")
            return render(request,'payment/canceled.html')
    return render(request, template_name="payment/done.html") 
valid_ipn_received.connect(successView, sender=PayPalIPN)

@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')

@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')

