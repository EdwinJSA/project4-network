from django import forms

class newPostform(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "What's on your mind?"}), required=True, label="")
    
