from django.shortcuts import render, redirect,get_object_or_404
from .models import Post, Comment
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from blog.forms import CommentForm,CustomLoginForm, CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog_index')  # Redirect to your index page after registration
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('blog_index')  # Redirect to your index page after login
    else:
        form = CustomLoginForm()
    
    return render(request, 'blog/login.html', {'form': form})


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







# def create_post(request):
#     if request.method == 'POST':
#         form = AnonymousPostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.doctor = None  # No doctor assigned initially
#             post.save()
#             form.save_m2m()  # Save the many-to-many relationships (categories)
#             return redirect('post_detail', slug=post.slug)  # Redirect to the post detail view
#     else:
#         form = AnonymousPostForm()
#     return render(request, 'create_post.html', {'form': form})

# def post_detail(request, post_id):
#     post = Post.objects.get(id=post_id)
#     comments = post.comments.all()

#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             anonymous_name = form.cleaned_data.get('anonymous_name')
#             comment = form.save(user=request.user)  # Pass the current user
#             if not request.user.is_authenticated and anonymous_name:
#                 comment.user = None  # Keep as anonymous
#                 comment.save()  # Save the comment
#             return redirect('post_detail', post_id=post.id)
#     else:
#         form = CommentForm()

#     return render(request, 'post_detail.html', {
#         'post': post,
#         'comments': comments,
#         'form': form,
#     })