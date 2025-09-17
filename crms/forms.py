from django import forms
from .models import ChangeRequest, ImpactAnalysis

class ChangeRequestForm(forms.ModelForm):
    class Meta:
        model = ChangeRequest
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'change_period_from': forms.DateInput(attrs={'type': 'date'}),
            'change_period_to': forms.DateInput(attrs={'type': 'date'}),
        }

class ImpactAnalysisForm(forms.ModelForm):
    class Meta:
        model = ImpactAnalysis
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }