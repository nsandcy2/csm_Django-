from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'owner']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'owner': forms.Select(attrs={'class': 'border rounded px-3 py-2 w-full'}),
        }
