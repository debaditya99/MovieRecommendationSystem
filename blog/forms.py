from .models import comment
from django import forms
class CommentForm(forms.ModelForm):
    class Meta:
        model = comment
        fields = ('name','body')
        widgets = {
        'name': forms.TextInput(attrs={"placeholder": "E.g. John Bruh",'class':'form-control'}),
        'body': forms.Textarea(attrs={"placeholder": "Write your views about this post.",'class':'form-control'}),
        }

# class Subscribe(forms.Form):
#     Email = forms.EmailField()
#     def __str__(self):
#         return self.Email