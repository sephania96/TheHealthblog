from django.shortcuts import render, redirect
from .models import Post
from .forms import AnonymousPostForm
from autoslug import AutoSlugField
# Create your views here.
def create_post(request):
    if request.method == 'POST':
        form = AnonymousPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.doctor = None  # No doctor assigned initially
            post.save()
            form.save_m2m()  # Save the many-to-many relationships (categories)
            return redirect('post_detail', slug=post.slug)  # Redirect to the post detail view
    else:
        form = AnonymousPostForm()
    return render(request, 'create_post.html', {'form': form})