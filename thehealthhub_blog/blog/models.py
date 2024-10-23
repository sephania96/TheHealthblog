from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django_summernote.fields import SummernoteTextField
# Create your models here.


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to="doctor_profiles/", null=True, blank=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    anonymous_user_name = models.CharField(max_length=100, null=True, blank=True)  # Field for the anonymous user's name
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)  # For doctor authorship
    categories = models.ManyToManyField(Category)  # Relationship to categories
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')  # Allow null for anonymous users
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username if self.user else "Anonymous"}: {self.post.title}'
    
# class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     content = models.TextField()
#     date = models.DateTimeField(auto_now_add=True)
#     user_name = models.CharField(max_length=100, null=True, blank=True)  # For anonymous users
#     doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)  # For doctor responses

#     def __str__(self):
#         return f"{self.user_name or 'Anonymous'} - {self.post.title}"