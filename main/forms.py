from django import forms
from .models import Section, Block

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['title', 'slug', 'position']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BlockForm(forms.ModelForm):
    class Meta:
        model = Block
        fields = ['section', 'title', 'content', 'image', 'position']
        widgets = {
            'section': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'position': forms.NumberInput(attrs={'class': 'form-control'}),
        }