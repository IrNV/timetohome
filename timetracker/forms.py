from django import forms

from .models import Post

class PostForm(forms.ModelForm):
    direction = forms.ChoiceField(choices=[("From home to university", "From home to university"),
    	("From University to home", "From University to home")])
    time = forms.TimeField()
    class Meta:
        model = Post
        fields = ('direction', 'time')