from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('db-connection/', views.db_connection_view, name='db_connection'),
    path('remove-db-connection/', views.remove_db_connection, name='remove_db_connection'),
    path('chat/', views.chat_view, name='chat'),
    path('schema-test/', views.schema_test_view, name='schema_test'),
] 