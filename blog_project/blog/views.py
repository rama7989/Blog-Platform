from django.shortcuts import render, get_object_or_404
from .models import BlogPost
from django.contrib.auth.decorators import login_required

from rest_framework import generics, permissions
from .models import BlogPost
from .serializers import BlogPostSerializer

from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


#login and Logout
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog-list')
        else:
            return render(request, 'blog/login.html', {'form': {'errors': True}})
    return render(request, 'blog/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

# Register
def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'blog/register.html', {'form': {'errors': "Passwords do not match"}})

        if User.objects.filter(username=username).exists():
            return render(request, 'blog/register.html', {'form': {'errors': "Username already exists"}})

        user = User.objects.create_user(username=username, password=password1)
        login(request, user)
        return redirect('blog-list')

    return render(request, 'blog/register.html')

@login_required
def blog_list(request):
    posts = BlogPost.objects.filter(is_private=False)
    return render(request, 'blog/blog_list.html', {'posts': posts})

@login_required
def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.is_private and post.author != request.user:
        return render(request, 'blog/403.html')  # Forbidden
    return render(request, 'blog/blog_detail.html', {'post': post})


class BlogPostListCreateAPIView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogPostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]