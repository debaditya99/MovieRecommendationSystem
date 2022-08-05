from django import forms

class UserInput(forms.Form):
    movie=forms.CharField()