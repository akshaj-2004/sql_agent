"""
Test script to verify SQL queries return correct results.
This demonstrates the proper way to query user skills with names.
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def test_queries():
    db_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    print("=" * 60)
    print("SQL Query Tests")
    print("=" * 60)
    
    # Test 1: Average Python rating
    print("\n1. Average rating for Python skill:")
    cur.execute("""
        SELECT AVG(rating) 
        FROM userskillandratings 
        WHERE skill = 'Python'
    """)
    result = cur.fetchone()[0]
    print(f"   Result: {float(result):.1f}")
    
    # Test 2: Users in IT department
    print("\n2. Users in IT department:")
    cur.execute("""
        SELECT u.name 
        FROM usermaster u 
        JOIN department d ON u.department_id = d.id 
        WHERE d.name = 'IT'
    """)
    for row in cur.fetchall():
        print(f"   - {row[0]}")
    
    # Test 3: Skills count per user (WITH NAMES)
    print("\n3. Number of skills per user:")
    cur.execute("""
        SELECT u.name, COUNT(us.skill) as num_skills 
        FROM userskillandratings us 
        JOIN usermaster u ON us.user_id = u.id 
        GROUP BY u.name 
        ORDER BY num_skills DESC
    """)
    for row in cur.fetchall():
        print(f"   - {row[0]}: {row[1]} skills")
    
    # Test 4: All users and their skills
    print("\n4. All users and their skills:")
    cur.execute("""
        SELECT u.name, us.skill, us.rating 
        FROM usermaster u 
        LEFT JOIN userskillandratings us ON u.id = us.user_id 
        ORDER BY u.name, us.skill
    """)
    current_user = None
    for row in cur.fetchall():
        if current_user != row[0]:
            current_user = row[0]
            print(f"\n   {current_user}:")
        if row[1]:
            print(f"     - {row[1]} (rating: {row[2]})")
        else:
            print(f"     - No skills recorded")
    
    print("\n" + "=" * 60)
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    test_queries()
