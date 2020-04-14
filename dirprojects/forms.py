from django import forms

class DirProjForm(forms.Form):
    name = forms.CharField(label="Project Name",required=True, widget=forms.TextInput(attrs={'size': '122', 'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':124, 'class': 'form-control'}),label="Description",required=False)