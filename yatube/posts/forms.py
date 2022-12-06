from django.forms import ModelForm

from .models import Comment, Group, Post, Profile


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


class ProfileForm(ModelForm):
    """Форма настроек Profile."""

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('user',)


class GroupForm(ModelForm):
    """Форма создания Group."""

    class Meta:
        model = Group
        fields = '__all__'
        exclude = ('group_author',)
