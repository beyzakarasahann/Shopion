from django.shortcuts import render
from products.models import Product  # Ürün modelin varsa bunu import et

def home(request):
    products = Product.objects.all()  # Tüm ürünleri al
    return render(request, 'main.html', {'products': products})  # Template'e gönder
