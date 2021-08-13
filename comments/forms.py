from django import forms
from .models import Comment, Note


class CommentForm(forms.ModelForm):
    body = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'input is-medium', 'placeholder': 'کامنت', 'dir': 'auto', 'style': 'resize:none;', }))

    class Meta:
        model = Comment
        fields = ('body',)


class NoteForm(forms.ModelForm):
    portion = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'class': 'input is-medium', 'placeholder': 'متن', 'dir': 'auto', 'id': 'input', 'readonly': 'readonly', 'style': 'resize:none;height:170px;', }))

    body = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'input is-medium', 'placeholder': 'توضیح', 'dir': 'auto'}))

    class Meta:
        model = Note
        fields = ('body',)
