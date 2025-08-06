# DataChat Companion Web Application

An AI-powered chatbot for natural language database queries and insights. Built with Django, LangChain, and LangGraph, this application allows business users to interact with their SQLite databases using conversational language.

## 🚀 Features

- **🔐 Secure Authentication**: Role-based access (Analyst/Admin) with Django's built-in auth system
- **🗄️ Database Connectivity**: User-specific SQLite3 database connections with file browser
- **�� AI-Powered Chat**: Natural language to SQL conversion using Azure OpenAI
- **📊 Schema Visualization**: Interactive tree view of database structure
- **💬 Chat History**: Persistent conversation history with export capabilities
- **📱 Modern UI**: Responsive design with Microsoft Copilot-style interface
- **🔒 Security**: Encrypted credential storage and SQL injection protection

## 🛠️ Tech Stack

- **Backend**: Django 5.0, Python 3.8+
- **Database**: SQLite3 (user-specific connections)
- **AI/ML**: LangChain, LangGraph, Azure OpenAI (GPT models)
- **Frontend**: Bootstrap 5, Font Awesome, Marked.js
- **Security**: Django Cryptography, CSRF protection
- **Testing**: pytest-django

## 📋 Prerequisites

- Python 3.8 or higher
- Azure OpenAI API key and endpoint
- Git (for cloning)

## �� Quick Start

### 2. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-django-secret-key-here
DEBUG=True

# Azure OpenAI Settings
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your-deployment-name

# Database Settings
FIELD_ENCRYPTION_KEY=your-32-character-encryption-key
```

### 5. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Start the Development Server

```bash
python manage.py runserver
```

### 8. Access the Application

Open your browser and navigate to:
- **Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 📖 Detailed Setup Instructions

### Environment Configuration

#### 1. Python Virtual Environment

The application **must** run within a Python virtual environment for dependency isolation:

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Verify activation
which python  # Should point to venv directory
```

#### 3. Environment Variables

Create a `.env` file with the following variables:

```env

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-35-turbo
```

### Database Setup

#### 1. Initial Migration

```bash
# Create initial migrations
python manage.py makemigrations chatbot

# Apply migrations
python manage.py migrate
```

#### 2. Create Admin User

```bash
python manage.py createsuperuser
# Follow the prompts to create admin credentials
```

### Application Usage

#### 1. User Registration and Login

1. **Access**: http://127.0.0.1:8000/
2. **Register**: Create a new account with Analyst or Admin role
3. **Login**: Use your credentials to access the application

#### 2. Database Connection Setup

1. **Navigate**: Go to Database Connection page
2. **Configure**: 
   - Enter a connection label
   - Use "Browse" button to select SQLite file
   - Enter full file path manually if needed
3. **Validate**: System will test the connection immediately
4. **Save**: Connection is stored securely

#### 3. Chat Interface

1. **Access Chat**: Navigate to the chat interface
2. **Schema View**: Left pane shows database schema tree
3. **Natural Language**: Type queries in natural language
4. **AI Processing**: System generates and executes SQL
5. **Results**: View formatted results with download options

#### 4. Available Commands

- **Natural Language**: "Show me all users"
- **Schema Command**: `/schema` - View database structure
- **SQL Generation**: `/sql <query>` - Generate SQL from natural language
- **Query Execution**: `/run <query>` - Execute natural language query

## 🧪 Testing

### Run All Tests

```bash
# Install pytest if not already installed
pip install pytest pytest-django

# Run tests
python -m pytest
```

### Run Specific Test Categories

```bash
# Authentication tests
python -m pytest chatbot/tests/test_auth.py

# Database connection tests
python -m pytest chatbot/tests/test_db_connection.py

# Chat functionality tests
python -m pytest chatbot/tests/test_chat.py
```

## 🔧 Development

### Project Structure

```
vibe-coding-project/
├── chatbot/                 # Main Django app
│   ├── models.py           # User, DatabaseConnection, ChatHistory models
│   ├── views.py            # Authentication, chat, and API views
│   ├── forms.py            # Custom forms for user registration
│   ├── agents.py           # LangChain/LangGraph agents
│   ├── templates/          # HTML templates
│   └── urls.py             # URL routing
├── core/                   # Django project settings
│   ├── settings.py         # Main configuration
│   └── urls.py             # Root URL configuration
├── requirements.txt        # Python dependencies
├── manage.py              # Django management script
└── README.md              # This file
```

### Key Components

#### Models
- **User**: Extended AbstractUser with role field
- **DatabaseConnection**: Encrypted SQLite connection storage
- **ChatHistory**: Persistent chat conversation storage

#### Views
- **Authentication**: Login, registration, password management
- **Database**: Connection management and validation
- **Chat**: AI-powered conversation interface
- **Profile**: User profile and settings

#### Agents
- **SchemaReaderAgent**: Database schema extraction
- **SQLGeneratorAgent**: Natural language to SQL conversion
- **AnsweringAgent**: SQL execution and result formatting

### Adding New Features

1. **Create Models**: Add to `chatbot/models.py`
2. **Create Views**: Add to `chatbot/views.py`
3. **Create Templates**: Add to `chatbot/templates/`
4. **Update URLs**: Add routes to `chatbot/urls.py`
5. **Run Migrations**: `python manage.py makemigrations && python manage.py migrate`

## 🔒 Security Considerations

### Authentication
- Django's built-in authentication system
- Password hashing with PBKDF2
- Session-based authentication
- CSRF protection enabled

### Data Protection
- Encrypted credential storage using Fernet
- SQL injection protection through parameterized queries
- Input validation and sanitization
- Role-based access control

### Environment Security
- Environment variables for sensitive data
- Virtual environment isolation
- Secure file permissions


**Note**: Always ensure the Python virtual environment is activated before running any commands. The application is designed to work exclusively within the virtual environment for dependency isolation and security.