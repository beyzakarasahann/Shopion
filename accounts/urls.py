from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account_view, name='account'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('toggle-favorite/<int:product_id>/', views.toggle_favorite_view, name='toggle_favorite'),
]
