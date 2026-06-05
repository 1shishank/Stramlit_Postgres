import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            database="Bank_DB",
            user="postgres",
            password="Helloworld12#",
            host="127.0.0.1",
            port=5432
        )
        return conn
    except Exception as e:
        print(f"Connection Error: {e}")
        return None


