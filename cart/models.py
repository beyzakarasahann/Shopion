from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.conf import settings



class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"{self.user.username}'s Cart"
        elif self.session_key:
            return f"Session Cart ({self.session_key})"
        else:
            return "Orphan Cart"
# Sepet öğesi (Sepetteki her bir ürün)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.product.price * self.quantity
# Sepeti göster
def cart_view(request):
    # Session key yoksa oluştur
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    # Kullanıcı giriş yaptıysa ona ait cart al, yapmadıysa session key'e ait
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = Cart.objects.filter(session_key=session_key).first()

    cart_items = CartItem.objects.filter(cart=cart) if cart else []
    total_price = sum(item.get_total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart/cart.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Oturum anahtarı yoksa oluştur
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    # Giriş yapmışsa user ile, değilse session_key ile cart bul
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    # Ürün zaten sepette varsa miktar artır, yoksa ekle
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )
    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart')  # Sepet sayfası URL name

