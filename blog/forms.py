from django import forms
from .models import Post

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter username'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Enter password'})
    )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Post Title'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Post Content', 'rows': 6}),
            'image': forms.FileInput(attrs={'class': 'form-input'})
        }