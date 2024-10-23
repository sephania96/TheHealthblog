from django.shortcuts import render, redirect
from .models import Post
from .models import Post, Comment
# Create your views here.
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
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
    }

    return render(request, "blog/detail.html", context)