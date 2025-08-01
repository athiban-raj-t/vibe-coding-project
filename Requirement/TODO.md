# ✅ Detailed TODO List for Business Data Chatbot Web Application  
**Environment Requirement**: All tasks must be implemented and executed within a **Python virtual environment** using `venv` or `virtualenv`.

---

## 📌 Phase 1: Core Setup & Authentication (Easy)

### - [x] **Set Up Python Virtual Environment**
**Details**:
- Create a virtual environment using `python -m venv venv`.
- Activate it and install Django and other initial dependencies.
- Add `venv/` to `.gitignore`.

**Acceptance Criteria**:
- Environment is activated and isolated.
- `requirements.txt` is generated with installed packages.
- Project runs only inside the virtual environment.

---

### - [x] **Initialize Django Project**
**Details**:
- Start a new Django project and app.
- Configure SQLite3 as the default database.
- Set up static files and templates.

**Acceptance Criteria**:
- Project runs with `python manage.py runserver`.
- Homepage loads without errors inside the virtual environment.

---

### - [x] **Create User Models with Roles (Analyst, Admin)**
**Details**:
- Extend `AbstractUser` to include a `role` field.
- Define role choices and enforce permissions in views.

**Acceptance Criteria**:
- Users are assigned roles during registration or by Admin.
- Role-based access is enforced and tested.

---

### - [x] **Implement Login, Registration, and Password Reset**
**Details**:
- Use Django’s built-in auth views and forms.
- Customize templates for login, registration, and password reset.
- Ensure secure password hashing.

**Acceptance Criteria**:
- Users can log in, register, and reset passwords.
- Authentication works inside the virtual environment.

---

### - [x] **Add User Profile Dropdown (Edit Profile, Change Password, Logout)**
**Details**:
- Add dropdown menu in the top-right corner of the dashboard.
- Link to views for profile editing, password change, and logout.

**Acceptance Criteria**:
- Dropdown is functional and visible after login.
- All options work correctly.

---

## 📌 Phase 2: Database Connectivity (Moderate)

### - [x] **Enable User-Specific Database Connections**
**Details**:
- Create a model to store encrypted DB credentials.
- Support SQLite3 only (per user).
- Validate and store only one active connection per user.

**Acceptance Criteria**:
- Users can input and save DB credentials securely.
- Only one active connection is allowed.
- All DB libraries are installed inside the virtual environment.

---

### - [x] **Validate Connection Immediately**
**Details**:
- On submission, test DB connection using credentials.
- Show success or error message.

**Acceptance Criteria**:
- Connection is validated instantly.
- Errors are handled gracefully.

---

### - [x] **Disable Chat Interface Until Valid Connection**
**Details**:
- Use a flag to check connection status.
- Disable chat input and show a prompt if no valid connection.

**Acceptance Criteria**:
- Chat interface is disabled until a valid connection is established.
- UI reflects connection status clearly.

---

### - [ ] **Allow Changing or Removing Connection**
**Details**:
- Provide UI to update or delete DB connection.
- Revalidate and update status accordingly.

**Acceptance Criteria**:
- Users can change or remove their connection.
- System updates and reflects changes immediately.

---

## 📌 Phase 3: Chatbot Intelligence (Moderate to Hard)

### - [ ] **Install and Configure LangChain + LangGraph**
**Details**:
- Install LangChain and LangGraph inside the virtual environment.
- Set up basic agent orchestration.

**Acceptance Criteria**:
- Agents are functional and respond to inputs.
- All dependencies are listed in `requirements.txt`.

---

### - [ ] **Implement Schema Reader Agent**
**Details**:
- Agent connects to user’s DB and reads schema.
- Returns structured schema data.

**Acceptance Criteria**:
- Schema is read and displayed correctly.
- Errors are handled gracefully.

---

### - [ ] **Implement SQL Generator Agent**
**Details**:
- Use prompt templates to generate safe `SELECT` statements.
- Validate SQL syntax and restrict to read-only queries.

**Acceptance Criteria**:
- Agent generates valid and safe SQL.
- SQL is validated before execution.

---

### - [ ] **Implement Answering Agent**
**Details**:
- Executes SQL queries and formats results in Markdown.
- Handles large result sets gracefully.

**Acceptance Criteria**:
- SQL is executed and results are returned.
- Output is readable and well-formatted.

---

## 📌 Phase 4: Chat Interface & History (Hard)

### - [ ] **Build Chat Interface (Right Pane)**
**Details**:
- Create scrollable chat window with input box and send button.
- Display bot and user messages.

**Acceptance Criteria**:
- Chat interface is responsive and functional.
- Messages are displayed in chronological order.

---

### - [ ] **Format Output with Markdown**
**Details**:
- Render Markdown in bot responses.
- Support bold, underline, tables, bullet points.

**Acceptance Criteria**:
- Markdown is rendered correctly.
- Tabular results are scrollable and downloadable as CSV.

---

### - [ ] **Store and Display Chat History**
**Details**:
- Create model to store chat logs per user.
- Include timestamp, query, SQL, and response.

**Acceptance Criteria**:
- Chat history is stored and retrievable.
- Admins can view all histories.

---

## 📌 Phase 5: Schema Visualization & Admin Tools (Advanced)

### - [ ] **Implement Schema Visualization (Tree View)**
**Details**:
- Display schema in collapsible tree format.
- Show tables and columns.

**Acceptance Criteria**:
- Tree view is interactive and accurate.
- Schema updates dynamically.

---

### - [ ] **Optional: Graph View of Relationships**
**Details**:
- Use Graphviz or Mermaid to visualize relationships.
- Provide toggle between tree and graph view.

**Acceptance Criteria**:
- Graph view is rendered correctly.
- Relationships are visually clear.

---

### - [ ] **Build Admin Dashboard**
**Details**:
- Create dashboard for Admins to monitor users, connections, and chat logs.
- Include filters and search options.

**Acceptance Criteria**:
- Admin dashboard is accessible only to Admins.
- Data is displayed clearly and securely.

---

## 📌 Phase 6: Deployment & Enhancements (Advanced)

### - [ ] **Dockerize the Application**
**Details**:
- Create Dockerfile and docker-compose setup.
- Ensure virtual environment is activated inside container.

**Acceptance Criteria**:
- App runs in Docker container with virtual environment.
- Environment variables are used for secrets.

---

### - [ ] **Deploy on Intranet or Private Cloud**
**Details**:
- Configure internal hosting (Apache/Nginx).
- Set up firewall and access controls.

**Acceptance Criteria**:
- App is accessible within company network.
- Security measures are verified.

---

### - [ ] **Implement Future Enhancements**
**Details**:
- Add support for multiple DB types.
- Enable follow-up questions and chat summarization.
- Export full chat history.
- Generate schema diagrams.

**Acceptance Criteria**:
- Enhancements are functional and integrated.
- User experience is improved.
