from django import forms
from .models import Comment, Post

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