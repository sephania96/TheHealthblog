from django.shortcuts import render, redirect,get_object_or_404
from .models import Post, Comment, Doctor
from django.contrib.auth.forms import AuthenticationForm
from .models import Category
from django.http import HttpResponseRedirect
from blog.forms import CommentForm,CustomLoginForm, CustomUserCreationForm, PostForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .serializers import DoctorSerializer, CategorySerializer, PostSerializer, CommentSerializer
from rest_framework import viewsets
# Create your views here.




#im creating my serializer views here
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer





def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated:
                post.doctor = Doctor.objects.get(user=request.user)  # Assign the doctor if logged in
            post.save()
            form.save_m2m()  # Save the many-to-many relationships
            return redirect('blog_index')  # Redirect to the index page after creating the post
    else:
        form = PostForm()

    return render(request, 'blog/create_post.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')  # Redirect to login page after registration
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('blog_index')  # Redirect to home page after login
    else:
        form = CustomLoginForm()
    
    return render(request, 'blog/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_view')


def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {
        "posts": posts,
    }
    return render(request, "blog/index.html", context)

def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)

def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)  # Using get_object_or_404 for better error handling
    comments = Comment.objects.filter(post=post)
    form = CommentForm()  # Initialize the comment form

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            anonymous_name = form.cleaned_data.get('anonymous_name')
            comment = form.save(commit=False)  # Don't save yet, we need to set the user
            if request.user.is_authenticated:
                comment.user = request.user  # Associate the comment with the user
            else:
                comment.user = None  # Keep it as anonymous
                comment.anonymous_name = anonymous_name  # Optionally save the anonymous name
            comment.post = post  # Associate comment with the post
            comment.save()  # Save the comment
            return redirect('blog_detail', pk=post.pk)  # Redirect to the same post after saving

    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }

    return render(request, "blog/detail.html", context)






