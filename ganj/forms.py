from django import forms
from .models import Post


class NewPostForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'input is-medium', 'placeholder': 'حداکثر 100 کاراکتر', 'dir': 'auto'}))

    body = forms.CharField( required=True, widget=forms.Textarea(
        attrs={'class': 'input is-medium', 'placeholder': 'متن پست', 'dir': 'auto', 'style': 'resize:none; height: 300px;'}))

    tags = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'input is-medium', 'placeholder': 'توسط فاصله جدا شود', 'dir': 'auto'}))

    author = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'input is-medium', 'id': 'authorautocomplete', 'placeholder': 'نویسنده', 'dir': 'auto'}))
    class Meta:
        model = Post
        fields = ('title', 'body', 'tags', 'author')



class EditPostForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'input is-medium', 'placeholder': 'حداکثر 100 کاراکتر', 'dir': 'auto'}))

    tags = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'input is-medium', 'placeholder': 'توسط فاصله جدا شود', 'dir': 'auto'}))

    author = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'input is-medium', 'id': 'authorautocomplete', 'placeholder': 'نویسنده', 'dir': 'auto'}))
    class Meta:
        model = Post
        fields = ('title', 'tags', 'author')
