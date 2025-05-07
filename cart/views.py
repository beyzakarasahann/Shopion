from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem

# Sepet Görüntüleme
def view_cart(request):
    # Giriş yapmış kullanıcı için sepet kaydedilecek
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)  # Giriş yapan kullanıcı için sepet
    else:
        cart, created = Cart.objects.get_or_create(user=None)  # Giriş yapmamış kullanıcı için anonim sepet

    # Sepetteki ürünleri al
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.get_total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart/cart.html', context)  # Bu satır doğru şekilde tamamlandı



# Sepete ürün ekle
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Eğer kullanıcı giriş yapmamışsa, anonim sepet oluştur
    if not request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=None)  # Anonim kullanıcı için sepet
    else:
        cart, created = Cart.objects.get_or_create(user=request.user)  # Giriş yapmış kullanıcı için normal sepet

    # Sepete ürün ekle
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1  # Eğer ürün zaten varsa miktarı artır
        cart_item.save()

    return redirect('view_cart')  # Sepeti tekrar görüntüle


# Sepetten ürün çıkar
def remove_from_cart(request, product_id):
    # Eğer kullanıcı giriş yapmamışsa, anonim sepet oluştur
    if not request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=None)  # Anonim kullanıcı için sepet
    else:
        cart = Cart.objects.get(user=request.user)  # Giriş yapmış kullanıcı için normal sepet

    cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
    cart_item.delete()

    return redirect('view_cart')  # Sepeti tekrar görüntüle
