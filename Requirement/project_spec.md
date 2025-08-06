
# 📘 Software Specification Document  
**Project Title**: DataChat Companion Web Application  
**Owner**: T. Athibanraj (Cognizant)  
**Tech Stack**: Django, LangGraph, LangChain, SQLite3  
**Deployment**: Internal (Intranet or On-Premise)

---

## 1. 🧭 Overview

A secure, role-based chatbot web application that enables business users to query their databases using natural language. The chatbot interprets queries, generates safe SQL `SELECT` statements, executes them, and returns results in a Markdown-formatted chat interface.

---

## 2. 👥 User Management

### 2.1 Roles

- **Analyst**:
  - View and manage own chat history and database connections.
  - Query connected databases.

- **Admin**:
  - View and manage all users' chat histories and database connections.
  - Perform administrative tasks like user management and system monitoring.

### 2.2 Authentication

- **Login Page**:
  - Fields: Username, Password
  - Buttons: Login, Register as New User
  - Links: Reset Password

- **Security**:
  - Passwords stored securely using Django’s hashing.
  - Session-based authentication with role-based access control.

### 2.3 User Profile

- Displayed at the top-right corner of the dashboard.
- Dropdown menu includes:
  - **Edit Profile**
  - **Change Password**
  - **Logout**

---

## 3. 🗄️ Database Connectivity

### 3.1 Default Configuration

- Default database: SQLite3

### 3.2 User-Specific Connections

- Users can connect their own databases (e.g., PostgreSQL, MySQL).
- Only **one active connection** per user.
- Credentials stored securely with encryption.
- Connection status shown in the **left pane**.

### 3.3 Connection Management

- Users can **change** or **remove** their existing connection.
- System **validates** new connection immediately.
- **Chat interface is disabled** until a valid connection is established.

---

## 4. 🧠 Chatbot Intelligence

### 4.1 Backend Framework

- **LangChain**: Prompt management, chaining tools, memory.
- **LangGraph**: Multi-step agent orchestration.

### 4.2 Agents

- **Schema Reader Agent**:
  - Reads and visualizes database schema.
  - Displays tables, columns, relationships.

- **SQL Generator Agent**:
  - Generates safe `SELECT` statements only.
  - Uses prompt templates and validation layer.

- **Answering Agent**:
  - Executes SQL queries.
  - Formats results in Markdown.

---

## 5. 💬 Chat Interface

### 5.1 Layout

- **Left Pane**:
  - Database connection status.
  - Schema visualization (tree view or diagram).
  - Connection management options.

- **Right Pane**:
  - Chat interface:
    - Scrollable output area.
    - Large input box.
    - Small send button.

### 5.2 Output Formatting

- Markdown support:
  - Bold, underline, tables, bullet points.
- Tabular results:
  - Scrollable view.
  - Downloadable as CSV.

---

## 6. 🧾 Chat History

- Stored per user.
- Includes:
  - Timestamp
  - User query
  - Generated SQL
  - Bot response
- Admins can view all users’ histories.

---

## 7. 📊 Schema Visualization

- Visual representation of database schema.
- Displayed in the left pane.
- Options:
  - Tree view of tables and columns.
  - Graph view of relationships (optional enhancement).

---

## 8. 🛠️ System Architecture

### 8.1 Frontend

- Django templates or React (optional)
- Responsive design using Bootstrap or Tailwind CSS

### 8.2 Backend

- Django views and models
- LangChain + LangGraph agents
- SQLite3 for default storage
- Optional support for other RDBMS

### 8.3 Security

- Role-based access control
- Encrypted credential storage
- CSRF protection
- Input sanitization and SQL validation

---

## 9. 🚀 Deployment

- Internal deployment on company intranet or private cloud.
- Docker-based containerization (optional)
- Admin dashboard for monitoring and maintenance

---

## 10. 📌 Future Enhancements

- Support for multiple database types
- Natural language follow-up questions
- Chat summarization
- Export full chat history
- Schema diagram generation using Graphviz or Mermaid

