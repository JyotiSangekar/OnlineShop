from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart
from django.core.urlresolvers import reverse
from decimal import Decimal

#import Requests
# from django.contrib.auth.decorators import login_required

# @login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()

            for item in cart:
                #client = taxjar.Client(api_key='cc16b8b2f3fba39495891baf6a85e51c')
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=Decimal(cart.get_total_price_after_discount()),
                                         quantity=item['quantity'],
                                        )
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)  # set the order in the session
            request.session['order_id'] = order.id  # redirect to the payment
            return redirect(reverse('payment:process'))
            # return render(request,
            #               'orders/order/created.html',
            #               {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart,'form': form})