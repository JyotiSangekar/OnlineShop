from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^create/$', views.order_create, name='order_create'),
    # url(r'^created/$', views.order_created1, name='order_created1'),
]
