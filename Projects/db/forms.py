from django import forms
from .models import Post
from .models import Studinfo

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class studform(forms.ModelForm):
    class Meta:
        model=Studinfo
        fields = ['name','email','mobile','address']

