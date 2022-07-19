from django.forms import ModelForm

from .models import Comment, Post


class PostForm(ModelForm):
    """Форма создания Post."""
    class Meta:
        model = Post
        fields = ('text', 'group', 'image',)


class CommentForm(ModelForm):
    """Форма создания Comment."""
    class Meta:
        model = Comment
        fields = ('text',)
