from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse



def view_cart(request):
    # Kullanıcıya özel sepet al
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart, _ = Cart.objects.get_or_create(user=None)

    cart_items = CartItem.objects.filter(cart=cart)

    # Sadece checkbox işaretli ürünler toplam fiyata eklensin
    if request.method == "POST":
        selected_ids = request.POST.getlist("selected_items")
        selected_ids = [int(pid) for pid in selected_ids]
        selected_items = cart_items.filter(product__id__in=selected_ids)
    else:
        selected_items = cart_items  # ilk girişte hepsi dahil

    total_price = sum(item.get_total_price() for item in selected_items)

    return render(request, "cart/cart.html", {
        "cart_items": cart_items,
        "total_price": total_price,
    })


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


    return redirect('cart:view_cart')  # ✅ DOĞRU YÖNLENDİRME BU


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

@csrf_exempt  # Geçici olarak CSRF'siz test için, ileride güvenlik ekleriz
def add_to_cart_ajax(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        if not request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=None)
        else:
            cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        total_items = CartItem.objects.filter(cart=cart).count()

        return JsonResponse({
            'success': True,
            'message': f'"{product.name}" sepete eklendi!',
            'cart_count': total_items
        })

    return JsonResponse({'success': False, 'error': 'Geçersiz istek'}, status=400)



def get_user_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart, _ = Cart.objects.get_or_create(user=None)
    return cart

def increase_quantity(request, product_id):
    cart = get_user_cart(request)

    # 🔒 Ürünü kontrol et
    product = get_object_or_404(Product, id=product_id)

    # 🛠️ get_or_create ile güvenli işlem
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart:view_cart')


def decrease_quantity(request, product_id):
    cart = get_user_cart(request)
    try:
        item = CartItem.objects.get(cart=cart, product_id=product_id)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart:view_cart')


def start_checkout(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_items')
        cart = get_user_cart(request)
        selected_items = cart.cartitem_set.filter(product_id__in=selected_ids)

        total_price = sum(item.get_total_price() for item in selected_items)

        return render(request, 'cart/summary.html', {
            'selected_items': selected_items,
            'total_price': total_price,
        })
