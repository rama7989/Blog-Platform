from django.urls import path
from . import views
from .views import BlogPostListCreateAPIView, BlogPostDetailAPIView
from .views import user_login, user_logout, user_register

urlpatterns = [
    path('', views.blog_list, name='blog-list'),
    path('<int:pk>/', views.blog_detail, name='blog-detail'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('api/', BlogPostListCreateAPIView.as_view(), name='api-blog-list-create'),
    path('api/<int:pk>/', BlogPostDetailAPIView.as_view(), name='api-blog-detail'),
]
