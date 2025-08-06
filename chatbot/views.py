from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, DatabaseConnectionForm
from .models import DatabaseConnection, ChatHistory
import os
import sqlite3
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .agents import SchemaReaderAgent, SQLGeneratorAgent, AnsweringAgent
from django.utils.html import format_html, escape

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def profile_view(request):
    if request.method == 'POST':
        # Handle profile updates here if needed
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'profile.html', {'user': request.user})

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

    # Get chat history from database instead of session
    chat_histories = ChatHistory.objects.filter(user=request.user).order_by('timestamp')[:50]  # Last 50 messages
    chat_history = []
    for hist in chat_histories:
        chat_history.append({
            'sender': 'user', 
            'text': hist.user_query,
            'timestamp': hist.timestamp
        })
        chat_history.append({
            'sender': 'bot', 
            'text': hist.bot_response,
            'timestamp': hist.timestamp
        })

    if request.method == 'POST' and has_valid_connection:
        user_message = request.POST.get('message', '').strip()
        if user_message:
            generated_sql = None
            if user_message.lower() == '/schema':
                agent = SchemaReaderAgent()
                schema = agent.read_schema(db_conn)
                if 'error' in schema:
                    bot_response = f"Schema error: {escape(schema['error'])}"
                else:
                    html = '<b>Database Schema:</b><br>'
                    for table in schema['tables']:
                        html += f"<b>{escape(table['name'])}</b>: "
                        html += ', '.join(f"{escape(col['name'])} ({escape(col['type'])})" for col in table['columns'])
                        html += '<br>'
                    bot_response = mark_safe(html)
            elif user_message.lower().startswith('/sql '):
                question = user_message[5:].strip()
                schema_agent = SchemaReaderAgent()
                schema = schema_agent.read_schema(db_conn)
                sql_agent = SQLGeneratorAgent()
                generated_sql = sql_agent.generate_sql(question, schema)
                bot_response = f"<b>Generated SQL:</b><br><pre>{escape(generated_sql)}</pre>"
            elif user_message.lower().startswith('/run '):
                question = user_message[5:].strip()
                schema_agent = SchemaReaderAgent()
                schema = schema_agent.read_schema(db_conn)
                sql_agent = SQLGeneratorAgent()
                generated_sql = sql_agent.generate_sql(question, schema)
                answer_agent = AnsweringAgent()
                result = answer_agent.execute_sql(db_conn, generated_sql)
                bot_response = f"<b>Generated SQL:</b><br><pre>{escape(generated_sql)}</pre><br><b>Result:</b><br>{result}"
            else:
                # Echo bot
                bot_response = f"Echo: {user_message}"
            
            # Ensure bot_response is not empty
            if not bot_response or not str(bot_response).strip():
                bot_response = "(No response from AI)"
            print(f"[DEBUG] Bot response: {bot_response}")  # Debug log
            
            # Save to database
            ChatHistory.objects.create(
                user=request.user,
                user_query=user_message,
                generated_sql=generated_sql,
                bot_response=bot_response,
                db_connection=db_conn
            )
            
        return redirect('chat')

    return render(request, 'chat.html', {
        'db_conn': db_conn,
        'has_valid_connection': has_valid_connection,
        'chat_history': chat_history,
    })

@login_required
def chat_history_view(request):
    if request.user.role == 'admin':
        # Admin can see all chat histories
        histories = ChatHistory.objects.all().order_by('-timestamp')
    else:
        # Regular users can only see their own
        histories = ChatHistory.objects.filter(user=request.user).order_by('-timestamp')
    
    return render(request, 'chat_history.html', {
        'histories': histories,
        'is_admin': request.user.role == 'admin'
    })

@login_required
def schema_test_view(request):
    try:
        db_conn = request.user.db_connection
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    agent = SchemaReaderAgent()
    schema = agent.read_schema(db_conn)
    return JsonResponse(schema)

@login_required
def sqlgen_test_view(request):
    try:
        db_conn = request.user.db_connection
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    question = request.GET.get('question', '')
    if not question:
        return JsonResponse({'error': 'Missing question parameter.'}, status=400)
    schema_agent = SchemaReaderAgent()
    schema = schema_agent.read_schema(db_conn)
    sql_agent = SQLGeneratorAgent()
    sql = sql_agent.generate_sql(question, schema)
    return JsonResponse({'sql': sql})

@login_required
def schema_visualization_view(request):
    try:
        db_conn = request.user.db_connection
        if not db_conn or not db_conn.is_active:
            return JsonResponse({'error': 'No active database connection'}, status=400)
        
        schema_agent = SchemaReaderAgent()
        schema = schema_agent.read_schema(db_conn)
        
        if 'error' in schema:
            return JsonResponse({'error': schema['error']}, status=400)
        
        return JsonResponse(schema)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
