import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(dotenv_path=".env")

# Function to establish a database connection
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Function to create tables
def create_tables():
    conn = get_connection()
    mycursor = conn.cursor()

    mycursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS employees(
            EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
            EmployeeName VARCHAR(255) NOT NULL,
            EmployeeContact VARCHAR(255) NOT NULL UNIQUE,
            EmployeeEmail VARCHAR(255) NOT NULL UNIQUE,
            Department VARCHAR(255) NOT NULL,
            Position VARCHAR(255) NOT NULL,
            Salary FLOAT NOT NULL,
            Attendance INT NOT NULL,
            Performance_Score INT NOT NULL
        )
        '''
    )

    mycursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS leave_requests(
            LeaveID INT AUTO_INCREMENT PRIMARY KEY,
            EmployeeID INT,
            EmployeeName VARCHAR(255) NOT NULL,
            LeaveType VARCHAR(255) NOT NULL,
            StartDate DATE NOT NULL,
            EndDate DATE NOT NULL,
            LeaveStatus VARCHAR(100) DEFAULT 'Pending',
            FOREIGN KEY (EmployeeID) REFERENCES employees(EmployeeID) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        '''
    )

    conn.commit()
    mycursor.close()
    conn.close()

# Run the function to create tables when this script is executed
if __name__ == "__main__":
    create_tables()
    print("✅ Database tables created successfully!")

