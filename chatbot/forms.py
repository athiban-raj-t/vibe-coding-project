from django import forms
from .models import DatabaseConnection

class DatabaseConnectionForm(forms.ModelForm):
    class Meta:
        model = DatabaseConnection
        fields = ['db_type', 'label', 'file_path']
        widgets = {
            'db_type': forms.Select(attrs={'class': 'form-control'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Connection Label'}),
            'file_path': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Path to SQLite3 file (e.g., db.sqlite3)'}),
        } 