from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post

class PostForm(forms.ModelForm):
    direction = forms.ChoiceField(choices=[("From home to university", "From home to university"),
    	("From University to home", "From University to home")])
    time = forms.TimeField(widget=forms.TimeInput(format=('hh-mm-ss')))
    class Meta:
        model = Post
        fields = ('direction', 'time')

# Customized user creation form
class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None