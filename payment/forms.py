from django.forms import ModelForm
from .models import ShippingAdress

class ShippingAdressForm(ModelForm):
    class Meta:
        model = ShippingAdress
        fields = ['full_name','email','street_address','apartment_address','country','city','zip_code']
        exclude = ('user',)