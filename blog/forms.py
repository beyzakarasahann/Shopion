from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="Yorumunuz",
        widget=forms.Textarea(attrs={
            'class': 'w-full p-2 border rounded dark:bg-gray-800 dark:text-white',
            'rows': 4,
            'placeholder': 'Yorumunuzu buraya yazın...'
        })
    )

    class Meta:
        model = Comment
        fields = ['content']
