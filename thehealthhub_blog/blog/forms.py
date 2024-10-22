from django import forms
from models import Comment, Post, User

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'user_name'] 

class DoctorCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content'] 


class AnonymousPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'anonymous_user_name', 'categories']  # Include categories