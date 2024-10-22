# blog/admin.py
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post
from django.apps import apps

# Register your models here.

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)  # Specify the fields to use the summernote editor

app = apps.get_app_config('blog')  # Replace 'blog' with your app name

for model in app.get_models():
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass