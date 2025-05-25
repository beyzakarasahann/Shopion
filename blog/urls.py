from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:pk>/', views.article_detail, name='article_detail'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
]
