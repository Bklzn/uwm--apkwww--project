from django import forms
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        is_authenticated = kwargs.pop('is_authenticated', False)
        super(CommentForm, self).__init__(*args, **kwargs)
        if is_authenticated:
            self.fields['nickname'] = forms.CharField(required=False)
        else:
            self.fields['nickname'] = forms.CharField(required=True)

    class Meta:
        model = Comment
        fields = ('text', 'nickname')


class PostForm(forms.ModelForm):
    published_date = forms.DateTimeField(required=True, widget=forms.TextInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Post
        fields = ('title', 'text', 'published_date')
