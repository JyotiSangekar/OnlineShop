from django.apps import AppConfig
from django.db.models.signals import pre_save, post_save
from django.apps import apps
from django.dispatch import receiver


class PaymentConfig(AppConfig):
    name = 'payment'

    def ready(self):
        from paypal.standard.ipn.models import PayPalIPN
        ST_PP_COMPLETED = apps.get_model('ipn', 'PayPalIPN')
        post_save.connect(receiver, sender="ipn.PayPalIPN")
