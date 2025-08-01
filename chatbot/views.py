from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import DatabaseConnectionForm
from .models import DatabaseConnection
import os
import sqlite3
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_POST

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def db_connection_view(request):
    try:
        db_conn = request.user.db_connection
    except DatabaseConnection.DoesNotExist:
        db_conn = None

    if request.method == 'POST':
        form = DatabaseConnectionForm(request.POST, instance=db_conn)
        if form.is_valid():
            db_type = form.cleaned_data['db_type']
            file_path = form.cleaned_data['file_path']
            # Only support SQLite3
            if db_type == 'sqlite3':
                abs_path = os.path.abspath(file_path)
                if not os.path.isfile(abs_path):
                    messages.error(request, f"File '{file_path}' does not exist.")
                else:
                    try:
                        conn = sqlite3.connect(abs_path)
                        conn.execute('SELECT name FROM sqlite_master LIMIT 1')
                        conn.close()
                        db_conn = form.save(commit=False)
                        db_conn.user = request.user
                        db_conn.is_active = True
                        db_conn.save()
                        messages.success(request, 'Database connection validated and saved successfully!')
                        return redirect('db_connection')
                    except Exception as e:
                        messages.error(request, f"Invalid SQLite3 database: {e}")
            else:
                messages.error(request, "Only SQLite3 is supported.")
    else:
        form = DatabaseConnectionForm(instance=db_conn)

    return render(request, 'db_connection.html', {'form': form, 'db_conn': db_conn})

@login_required
@require_POST
def remove_db_connection(request):
    try:
        db_conn = request.user.db_connection
        db_conn.delete()
        messages.success(request, 'Database connection removed.')
    except DatabaseConnection.DoesNotExist:
        messages.error(request, 'No database connection to remove.')
    return redirect('db_connection')

@login_required
def chat_view(request):
    # Check for valid/active DB connection
    try:
        db_conn = request.user.db_connection
        has_valid_connection = db_conn and db_conn.is_active
    except DatabaseConnection.DoesNotExist:
        db_conn = None
        has_valid_connection = False

    # Simple in-memory chat history for demo (replace with DB later)
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []

    chat_history = request.session['chat_history']

    if request.method == 'POST' and has_valid_connection:
        user_message = request.POST.get('message', '').strip()
        if user_message:
            chat_history.append({'sender': 'user', 'text': user_message})
            # Echo bot
            bot_response = f"Echo: {user_message}"
            chat_history.append({'sender': 'bot', 'text': bot_response})
            request.session['chat_history'] = chat_history
        return redirect('chat')

    return render(request, 'chat.html', {
        'db_conn': db_conn,
        'has_valid_connection': has_valid_connection,
        'chat_history': chat_history,
    })
