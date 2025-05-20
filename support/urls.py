from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.support_detail, name='support_detail'),
    path('', views.support_list, name='support_list'),
    path('new/', views.support_new, name='support_new'),
]
