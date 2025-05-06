from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import CartItem

# Sepeti göster
def cart_view(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_items = CartItem.objects.filter(session_key=session_key)
    total_price = sum(item.get_total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart/cart.html', context)

# Ürünü sepete ekle
def add_to_cart(request, product_id):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    product = get_object_or_404(Product, id=product_id)

    item, created = CartItem.objects.get_or_create(
        session_key=session_key,
        product=product
    )
    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart')
