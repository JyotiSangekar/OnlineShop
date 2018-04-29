from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
import requests


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')
    response = requests.get('http://freegeoip.net/json/%s' % ip_address)
    geodata = response.json()
   # booklist = requests.get(
    #    'https://api.nytimes.com/svc/books/v3/lists.json?list-name=hardcover-fiction&api-key=94f521d72a6c406b87070b21d29435ae')
   # booklist_response = booklist.json()
   # print(booklist_response)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {'category': category,
                                                      'categories': categories,
                                                      'products': products,
                                                      'ip': geodata['ip'],
                                                      'country': geodata['country_name'],
                                                      'latitude': geodata['latitude'],
                                                      'longitude': geodata['longitude'],
                                                      'api_key': 'AIzaSyAUR-EM5qKZFSr-GzxH9XvmUgP_DYx22ko',
                                                     # 'books': booklist_response
                                                      })

    # if category_slug:
    #     category = get_object_or_404(Category, slug=category_slug)
    #     products = products.filter(category=category)
    # return render(request, 'shop/product/list.html', {'category': category,
    #                                                   'categories': categories,
    #                                                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})