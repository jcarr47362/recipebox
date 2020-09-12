from django import forms
from homepage.models import Recipe, Author


class AddRecipeForm(forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)
    #author = forms.ModelChoiceField(queryset=Author.objects.all())
    time_required = forms.CharField(max_length=50)
    instructions = forms.CharField(widget=forms.Textarea)


class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name", "bio"]
    # username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)
