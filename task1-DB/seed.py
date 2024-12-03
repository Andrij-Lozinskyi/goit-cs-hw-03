from faker import Faker
import psycopg2
from psycopg2 import Error
import random

fake = Faker()

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "root"
DB_HOST = "localhost"
DB_PORT = "5432"

try:
    connection = psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = connection.cursor()

    users_data = []
    for _ in range(10):
        fullname = fake.name()
        email = fake.email()
        users_data.append((fullname, email))

    users_query = """
        INSERT INTO users (fullname, email) 
        VALUES (%s, %s) 
        RETURNING id;
    """
    
    user_ids = []
    for user in users_data:
        try:
            cursor.execute(users_query, user)
            user_ids.append(cursor.fetchone()[0])
        except psycopg2.IntegrityError:
            connection.rollback()
            continue

    cursor.execute("SELECT id FROM status;")
    status_ids = [row[0] for row in cursor.fetchall()]

    tasks_query = """
        INSERT INTO tasks (title, description, status_id, user_id)
        VALUES (%s, %s, %s, %s);
    """

    for _ in range(30):
        title = fake.catch_phrase()
        description = fake.text(max_nb_chars=200)
        status_id = random.choice(status_ids)
        user_id = random.choice(user_ids)
        
        cursor.execute(tasks_query, (title, description, status_id, user_id))

    connection.commit()
    print("Successfully inserted!")

except (Exception, Error) as error:
    print("Error connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Connection is closed!")