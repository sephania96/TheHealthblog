from django import forms
from .models import Comment, Post
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Email Address', required=True)
    first_name = forms.CharField(label='First Name', required=True)
    last_name = forms.CharField(label='Last Name', required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
class CommentForm(forms.ModelForm):
    anonymous_name = forms.CharField(required=False, max_length=100, label="Your Name (Optional)")

    class Meta:
        model = Comment
        fields = ['content', 'anonymous_name']  # Include anonymous name field

    def save(self, commit=True, user=None):
        comment = super().save(commit=False)
        if user:
            comment.user = user  # Associate the comment with the user
        else:
            # If user is not authenticated, you can set a default name or leave it blank
            comment.user = None  # This allows for anonymous comments
        if commit:
            comment.save()
        return comment

class DoctorCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content'] 


class AnonymousPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'anonymous_user_name', 'categories']  # Include categories