from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from apps.customer.forms import CustomUserCreationForm
from apps.dashboard.forms import CustomAuthenticationForm, ProductForm
from .decorators import not_logged_user
from ..product.models import Product, Category


# Create your views here.


@method_decorator(not_logged_user, name='dispatch')
class UserSignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'dashboard/auth/register.html'

    def form_valid(self, form):
        # Save the form to create the user
        response = super().form_valid(form)
        # Authenticate and login the user
        user = form.save()
        login(self.request, user)
        return response


@method_decorator(not_logged_user, name='dispatch')
class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'dashboard/auth/login.html'


def create_product(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products_list')
    else:
        form = ProductForm()
    return render(request, 'dashboard/products/add_product.html', {'form': form,'categories': categories})


def list_product(request):
    products = Product.objects.all()
    return render(request, 'dashboard/products/product_view.html', {'products': products})


def home(request):
    return render(request,"dashboard/analytics.html")
