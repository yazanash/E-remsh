from django import forms
from django.contrib.auth.forms import AuthenticationForm

from apps.product.models import Product


class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    # colors = forms.CharField(widget=forms.HiddenInput(), required=False)

