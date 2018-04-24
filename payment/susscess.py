@csrf_exempt
def successView(request, sender=PayPalIPN, **kwargs):
    ipn_obj = sender
    print(ipn_obj)
    order_id = request.session.get('order_id')
    print (order_id)
    order = get_object_or_404(Order, id=order_id)
    print (order)
    ordereditem = get_object_or_404(OrderItem, order=order.id)
    ipn_obj_confirm = PayPalIPN.objects.filter(custom=order_id)
    print (ipn_obj_confirm)
    # ipn_obj_confirm = ipn_obj.objects.filter(invoice=str(order_id))
    # print (ipn_obj_confirm)
    for i in ipn_obj_confirm:
        if i.payment_status == "Completed":
            if i.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
                send_mail(
                    'Error Purchasing',
                    'Payment Not Confirmed, Kindly contact your support or payment institution',
                    settings.THEME_CONTACT_EMAIL,
                    [order.email],
                    fail_silently=False,
                )
                return reverse('payment:canceled')
            else:
                values_to_update = {'paid':True}
                obj_order, created = Order.objects.update_or_create(order_id=order_id, defaults=values_to_update )
                subject = "Order was SuccessFull"
                to = [order.email]
                from_email = settings.THEME_CONTACT_EMAIL

                ctx = {
                    'first_name' : order.first_name,
                    'last_name' : order.last_name,
                    'email' : order.email,
                    'address' : order.address,
                    'postal_code' : order.postal_code,
                    'city' : order.city,
                    'created' : order.created,
                    'updated' : order.updated,
                    'paid' : order.paid,
                    'Order Number': ordereditem.order,
                    'product' : ordereditem.product,
                    'price' : ordereditem.price,
                    'quantity' : ordereditem.quantity,                   
                }
                message = get_template('payment/email.html').render(Context(ctx))
                msg = EmailMessage(subject, message, to=to, from_email=from_email)
                msg.content_subtype = 'html'
                msg.send()       
                return reverse('payment:done')
        else:
            send_mail(
                'Error Purchasing',
                'Payment Not Confirmed, Kindly contact your support or payment institution',
                settings.THEME_CONTACT_EMAIL,
                [order.email],
                fail_silently=False,
            )            
            return reverse('payment:canceled')
    # return render(request, template_name="payment/done.html") 
valid_ipn_received.connect(successView, sender=PayPalIPN)