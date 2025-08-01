from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, DatabaseConnection

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('role',)

class DatabaseConnectionForm(forms.ModelForm):
    class Meta:
        model = DatabaseConnection
        fields = ['db_type', 'label', 'file_path']
        widgets = {
            'db_type': forms.Select(attrs={'class': 'form-control'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Connection Label'}),
            'file_path': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Path to SQLite3 file (e.g., db.sqlite3)'}),
        } 