from mydb import get_connection

try:
    conn = get_connection()
    if conn.is_connected():
        print("Database connected successfully!")
    else:
        print("Database connection failed!")
except Exception as e:
    print(f"Error: {e}")
