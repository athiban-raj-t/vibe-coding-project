import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from chatbot.models import DatabaseConnection

@pytest.mark.django_db
def test_registration_and_login(client):
    # Register a new user
    response = client.post(reverse('register'), {
        'username': 'testuser',
        'password1': 'Testpass123!',
        'password2': 'Testpass123!',
    })
    assert response.status_code == 302  # Redirect to login
    # Login
    response = client.post(reverse('login'), {
        'username': 'testuser',
        'password': 'Testpass123!',
    })
    assert response.status_code == 302  # Redirect after login

@pytest.mark.django_db
def test_db_connection_flow(client):
    User = get_user_model()
    user = User.objects.create_user(username='dbuser', password='Testpass123!')
    client.login(username='dbuser', password='Testpass123!')
    # Add a valid connection (default db.sqlite3)
    response = client.post(reverse('db_connection'), {
        'db_type': 'sqlite3',
        'label': 'My DB',
        'file_path': 'db.sqlite3',
    }, follow=True)
    assert b'Database connection validated and saved successfully!' in response.content
    db_conn = DatabaseConnection.objects.get(user=user)
    assert db_conn.label == 'My DB'
    # Remove connection
    response = client.post(reverse('remove_db_connection'), follow=True)
    assert b'Database connection removed.' in response.content
    assert not DatabaseConnection.objects.filter(user=user).exists()

@pytest.mark.django_db
def test_chat_access_requires_connection(client):
    User = get_user_model()
    user = User.objects.create_user(username='chatuser', password='Testpass123!')
    client.login(username='chatuser', password='Testpass123!')
    # No connection: chat input should be disabled
    response = client.get(reverse('chat'))
    assert b'Connect to a valid SQLite3 database to start chatting.' in response.content
    # Add connection
    client.post(reverse('db_connection'), {
        'db_type': 'sqlite3',
        'label': 'Chat DB',
        'file_path': 'db.sqlite3',
    })
    # Now chat input should be enabled
    response = client.get(reverse('chat'))
    assert b'<input type="text" name="message" placeholder="Type your message..."' in response.content
    # Send a message
    response = client.post(reverse('chat'), {'message': 'Hello, bot!'}, follow=True)
    assert b'Echo: Hello, bot!' in response.content
