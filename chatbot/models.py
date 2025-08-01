import base64
from cryptography.fernet import Fernet
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Utility for encryption/decryption
class EncryptionHelper:
    @staticmethod
    def get_fernet():
        key = getattr(settings, 'FIELD_ENCRYPTION_KEY', None)
        if not key:
            raise ValueError('FIELD_ENCRYPTION_KEY must be set in settings.py')
        return Fernet(key)

    @staticmethod
    def encrypt(value):
        if value is None:
            return value
        f = EncryptionHelper.get_fernet()
        return f.encrypt(value.encode()).decode()

    @staticmethod
    def decrypt(value):
        if value is None:
            return value
        f = EncryptionHelper.get_fernet()
        return f.decrypt(value.encode()).decode()

class EncryptedCharField(models.CharField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return EncryptionHelper.decrypt(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return EncryptionHelper.encrypt(value)

# Create your models here.

class User(AbstractUser):
    ANALYST = 'analyst'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (ANALYST, 'Analyst'),
        (ADMIN, 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ANALYST)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class DatabaseConnection(models.Model):
    DB_TYPE_CHOICES = [
        ('sqlite3', 'SQLite3'),
        # ('postgresql', 'PostgreSQL'),
        # ('mysql', 'MySQL'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='db_connection')
    db_type = models.CharField(max_length=20, choices=DB_TYPE_CHOICES, default='sqlite3')
    label = models.CharField(max_length=100, default='Default SQLite3')
    file_path = models.CharField(max_length=255, default='db.sqlite3')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.label} ({'Active' if self.is_active else 'Inactive'})"
