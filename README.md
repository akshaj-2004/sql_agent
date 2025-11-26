# SQL Query Agent

An intelligent agent that translates natural language questions into SQL queries and executes them against a PostgreSQL database using LangChain and Ollama.

## 🎯 Overview

This project implements an AI-powered SQL agent that:
- Takes natural language questions as input
- Automatically examines your database schema
- Generates appropriate SQL queries
- Executes queries against PostgreSQL
- Returns results in natural language

**Perfect for**: Querying databases without writing SQL, data exploration, and quick analytics.

---

## 📋 Prerequisites

Before you begin, ensure you have:

1. **Python 3.12+** installed
2. **PostgreSQL** database running
3. **Ollama** installed with a model pulled (e.g., `llama3`)
4. **Virtual environment** activated

---

## 🚀 Quick Start

### Step 1: Install Ollama Model

If you haven't already, pull a model:

```bash
ollama pull llama3
```

Verify it's installed:
```bash
ollama list
```

### Step 2: Configure Environment

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/your_database
OLLAMA_MODEL=llama3
```

**Replace** `username`, `password`, and `your_database` with your PostgreSQL credentials.

### Step 3: Activate Virtual Environment

```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

Dependencies should already be installed, but if needed:

```bash
pip install langchain langchain-community langchain-ollama psycopg2-binary python-dotenv
```

### Step 5: Initialize Database

Run the setup script to create tables and populate sample data:

```bash
python setup_postgres.py
```

This creates three tables:
- **`department`** - Stores departments (HR, IT, Sales, Marketing)
- **`usermaster`** - Stores user information
- **`UserSkillAndRatings`** - Stores user skills with ratings (1-5)

### Step 6: Run the Agent

```bash
python sql_agent.py
```

You'll see:
```
--- SQL Query Agent ---
Connected to database.
Initializing Ollama with model: llama3

Agent ready! Enter your query (or 'exit' to quit).

Query: 
```

### Step 7: Ask Questions!

Type your questions in plain English:

```
Query: What is the average rating of people having python skill?
Result: The average rating of people having Python skill is 4.

Query: List all users in the IT department
Result: Alice Smith, Charlie Brown

Query: exit
```

---

## 💡 Example Queries

Try these questions:

- `"How many users are in each department?"`
- `"Who has the highest rating in Python?"`
- `"List all skills and their average ratings"`
- `"What is the email of users in the Sales department?"`
- `"Show me all users with a rating above 4"`
- `"Count the total number of skills in the database"`

---


**Tools Available:**
- `sql_db_list_tables` - Lists all database tables
- `sql_db_schema` - Shows table structure and sample data
- `sql_db_query` - Executes SQL queries
- `sql_db_query_checker` - Validates SQL syntax

---


## 🧪 Testing

Run the test script to verify everything works:

```bash
python test_queries.py
```

This executes several test queries and displays results with proper formatting.

---



