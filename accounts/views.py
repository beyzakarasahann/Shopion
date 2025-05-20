from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.shortcuts import get_object_or_404
from support.models import SupportTicket
from support.forms import SupportTicketForm


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # home view'in yoksa burayı değiştirebilirsin
        else:
            messages.error(request, "Kullanıcı adı veya şifre hatalı.")
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')



def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Hesabınız oluşturuldu.")
            return redirect('home')  # veya redirect('/')
        else:
            messages.error(request, "Kayıt işlemi tamamlanamadı. Lütfen bilgilerinizi kontrol edin.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})



@login_required
def account_view(request):
    return render(request, 'accounts/account.html')  # 👈 bu html'i birazdan yaparız

@login_required
def favorites_view(request):
    # Şu anlık dummy içerik, daha sonra favori ürünler modelinden çekilecek
    return render(request, 'accounts/favorites.html')


@login_required
def toggle_favorite_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product in request.user.favorites.all():
        request.user.favorites.remove(product)
    else:
        request.user.favorites.add(product)

    return redirect(request.META.get('HTTP_REFERER', 'home'))



@login_required
def favorites_view(request):
    favorites = request.user.favorites.all()
    return render(request, 'accounts/favorites.html', {'favorites': favorites})


@login_required
def account_dashboard(request):
    return render(request, 'accounts/account.html', {
        "account_section": "accounts/welcome_inner.html"  # default boş içerik
    })

