from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='view_cart'),  # Sepeti görüntüleme
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Ürün ekleme
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),  # Ürün çıkarma
]
