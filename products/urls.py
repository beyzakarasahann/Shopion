# products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Ürün listeleme
    path('', views.product_list, name='product_list'),

    # Ürün detay sayfası
    path('detail/<int:id>/', views.product_detail, name='product_detail'),

    # Ürünü sepete ekleme
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # Sepet görüntüleme
    path('cart/', views.view_cart, name='view_cart'),

    # Sepetten ürün çıkarma
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
]
