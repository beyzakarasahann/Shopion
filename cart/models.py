from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth.models import User
from products.models import Product


# Kullanıcının Sepeti
class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)  # NULL ve blank=True ekledik

    def __str__(self):
        if self.user:
            return f"{self.user.username}'s Cart"
        else:
            return "Anonymous Cart"  # Anonim kullanıcı için farklı bir ifade

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
    # Kullanıcının sepetini al veya oluştur
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Bu sepetteki ürünleri al
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.get_total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart/cart.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )
    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart')


