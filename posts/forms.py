from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image')
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Заголовок поста"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Текст поста"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control", "placeholder": "Изображение (необязательно)"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Ваш комментарий..."}),
        }
