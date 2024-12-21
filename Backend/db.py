import psycopg2
from psycopg2.extras import RealDictCursor
import uuid
from config import Config

def get_db_connection():
    try:
        conn = psycopg2.connect(Config.DATABASE_URL)
        return conn
    except Exception as e:
        raise RuntimeError(f"Error connecting to the database: {e}")
    
def add_measurement(data):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO measurement (id, chest, waist, shoulder, armlength, height, leg, shirt)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data['id'],
                data['chest'],
                data['waist'],
                data['shoulder'],
                data['arm_length'],
                data['height'],
                data['leg'],
                data['shirt']
            ))
            conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def get_measurement(id):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM measurement
                WHERE id = %s
            """, (id,))
            result = cursor.fetchone()
            return result
    finally:
        conn.close()
