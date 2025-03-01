import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=".env")

print(f"DB_HOST: {os.getenv('DB_HOST')}")
print(f"DB_USER: {os.getenv('DB_USER')}")
print(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")
print(f"DB_NAME: {os.getenv('DB_NAME')}")

print("🔄 Attempting to connect to MySQL...")

try:
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        
    )

    if conn.is_connected():
        print("✅ Connected to MySQL successfully!")
    else:
        print("❌ Connection attempt failed.")

    conn.close()

except mysql.connector.Error as err:
    print(f"❌ MySQL Connection Error: {err}")

