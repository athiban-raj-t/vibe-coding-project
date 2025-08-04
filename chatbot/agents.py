from langchain.schema import BaseChatMessageHistory
from langchain.agents import AgentExecutor
from langgraph.graph import StateGraph
import sqlite3
import openai
from django.conf import settings
from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI

# Placeholder for user session state
class ChatbotState:
    def __init__(self, user, db_connection):
        self.user = user
        self.db_connection = db_connection
        self.schema = None
        self.last_sql = None
        self.last_result = None

# Placeholder: Schema Reader Agent
class SchemaReaderAgent:
    def read_schema(self, db_connection):
        file_path = db_connection.file_path
        schema = {"tables": []}
        try:
            conn = sqlite3.connect(file_path)
            cursor = conn.cursor()
            # Get all table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = cursor.fetchall()
            for (table_name,) in tables:
                # Get columns for each table
                cursor.execute(f"PRAGMA table_info('{table_name}')")
                columns = cursor.fetchall()
                schema["tables"].append({
                    "name": table_name,
                    "columns": [
                        {"name": col[1], "type": col[2]} for col in columns
                    ]
                })
            conn.close()
        except Exception as e:
            schema["error"] = str(e)
        return schema

# Placeholder: SQL Generator Agent
class SQLGeneratorAgent:
    def generate_sql(self, user_query, schema):
        schema_str = ''
        for table in schema.get('tables', []):
            schema_str += f"Table: {table['name']}\nColumns: "
            schema_str += ', '.join(f"{col['name']} ({col['type']})" for col in table['columns']) + '\n'
        prompt = f"""
You are an expert SQL assistant. Only generate safe, syntactically correct SELECT statements for SQLite3.\nSchema:\n{schema_str}\nUser question: {user_query}\nSQL (SELECT only):
"""
        try:
            llm = AzureChatOpenAI(
                azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT,
                api_version="2025-01-01-preview",
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                api_key=settings.AZURE_OPENAI_API_KEY,
                temperature=0,
            )
            messages = [
                ("system", "You are an expert SQL assistant. Only generate safe, syntactically correct SELECT statements for SQLite3."),
                ("human", prompt)
            ]
            ai_msg = llm.invoke(messages)
            sql = ai_msg.content.strip()
            if not sql.lower().startswith('select'):
                return "-- ERROR: Only SELECT statements are allowed."
            return sql
        except Exception as e:
            return f"-- ERROR: {e}"

# Placeholder: Answering Agent
class AnsweringAgent:
    def execute_sql(self, db_connection, sql):
        # TODO: Implement SQL execution and result formatting
        return "Result: 1"

# Orchestration graph (scaffold)
def get_agent_executor(user, db_connection):
    state = ChatbotState(user, db_connection)
    schema_agent = SchemaReaderAgent()
    sql_agent = SQLGeneratorAgent()
    answer_agent = AnsweringAgent()
    # TODO: Build LangGraph StateGraph for orchestration
    # For now, just return the state and agents
    return state, schema_agent, sql_agent, answer_agent 