import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("Please enter your PostgreSQL connection string.")
        print("Format: postgresql://user:password@localhost:5432/dbname")
        db_url = input("Connection String: ").strip()
    
    try:
        conn = psycopg2.connect(db_url)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def create_tables(conn):
    commands = (
        """
        DROP TABLE IF EXISTS UserSkillAndRatings;
        DROP TABLE IF EXISTS usermaster;
        DROP TABLE IF EXISTS department;
        """,
        """
        CREATE TABLE department (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE usermaster (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            department_id INTEGER REFERENCES department(id)
        )
        """,
        """
        CREATE TABLE UserSkillAndRatings (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES usermaster(id),
            skill VARCHAR(255) NOT NULL,
            rating INTEGER CHECK (rating >= 1 AND rating <= 5)
        )
        """
    )
    cur = conn.cursor()
    for command in commands:
        cur.execute(command)
    cur.close()
    conn.commit()
    print("Tables created successfully.")

def insert_dummy_data(conn):
    cur = conn.cursor()
    
    # Departments
    departments = ['HR', 'IT', 'Sales', 'Marketing']
    dept_ids = []
    for dept in departments:
        cur.execute("INSERT INTO department (name) VALUES (%s) RETURNING id", (dept,))
        dept_ids.append(cur.fetchone()[0])
    
    # dept_ids will be [1, 2, 3, 4] roughly
    # Map them for easier access if needed, but the order is preserved.

    
    # Users
    users = [
        ('Alice Smith', 'alice@example.com', dept_ids[1]), # IT
        ('Bob Jones', 'bob@example.com', dept_ids[0]),   # HR
        ('Charlie Brown', 'charlie@example.com', dept_ids[1]), # IT
        ('David Wilson', 'david@example.com', dept_ids[2]), # Sales
        ('Eve Davis', 'eve@example.com', dept_ids[3])    # Marketing
    ]
    
    user_ids = []
    for user in users:
        cur.execute("INSERT INTO usermaster (name, email, department_id) VALUES (%s, %s, %s) RETURNING id", user)
        user_ids.append(cur.fetchone()[0])
        
    # Skills
    skills = [
        (user_ids[0], 'Python', 5),
        (user_ids[0], 'SQL', 4),
        (user_ids[1], 'Recruiting', 5),
        (user_ids[2], 'Java', 4),
        (user_ids[2], 'Python', 3),
        (user_ids[3], 'Negotiation', 5),
        (user_ids[4], 'SEO', 4)
    ]
    
    cur.executemany("INSERT INTO UserSkillAndRatings (user_id, skill, rating) VALUES (%s, %s, %s)", skills)
    
    conn.commit()
    cur.close()
    print("Dummy data inserted successfully.")

if __name__ == "__main__":
    conn = get_connection()
    if conn:
        create_tables(conn)
        insert_dummy_data(conn)
        conn.close()
