from django.shortcuts import render, get_object_or_404
from .models import Product


def home(request):
    products = Product.objects.all()
    return render(request, 'main.html', {'products': products})
# Ürün listeleme
def product_list(request):
    # Veritabanındaki tüm ürünleri alıyoruz
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

# Ürün detay sayfası
def product_detail(request, id):
    # Ürün ID'sine göre ürünü alıyoruz. Bulamazsa 404 hatası verir.
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/product_detail.html', {'product': product})
