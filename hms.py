# import packages

import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
from streamlit_option_menu import option_menu
from mydb import get_connection

# configure streamlit app settings
st.set_page_config(
    page_title="HR DASHBOARD",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Sidebar navigation with icons
with st.sidebar:
    menu = option_menu("Human Resource Dashboard",
                       ["Home", "Employee Management", "Analytics", "Salary & Payroll", "Leave Management"],
                       icons=["house", "person-badge", "bar-chart", "currency-dollar", "calendar-event"],
                       menu_icon="grid-fill",
                       default_index=0
                       )

# Home
if menu == "Home":
    st.title("📊 HR Dashboard Overview")
    st.write(
        """
        Welcome to the **HR Analytics Dashboard**, your all-in-one platform for managing and analyzing 
        human resource data. This dashboard helps HR professionals track key metrics, manage employee 
        records, monitor attendance, analyze performance trends, and oversee payroll and leave requests efficiently.  

        📌 **Key Features of This Dashboard:**  
        - 📂 **Employee Management:** Add, edit, and manage employee records easily.  
        - 📈 **Analytics:** Gain insights into workforce trends, performance scores, and departmental efficiency.  
        - 💰 **Salary & Payroll:** Track employee salaries and manage payroll processes seamlessly.  
        - 🏖 **Leave Management:** Handle employee leave requests and approvals with ease.  

        Navigate through the sections using the sidebar to explore and manage your HR operations effectively.  
        """
    )

    # Employee Management
elif menu == "Employee Management":
    # Establish database connection
    conn = get_connection()
    mycursor = conn.cursor()
    # Add new employee
    with st.form("add_employee"):
        name = st.text_input("Employee Name")
        contact = st.text_input("Employee Contact")
        email = st.text_input("Employee Email")
        department = st.selectbox("Department", ["HR", "Finance", "IT", "Sales", "Marketing"])
        position = st.text_input("Position")
        salary = st.number_input("Salary", min_value=0)
        attendance = st.slider("Attendance Score (1-100)", 1, 100, 80)
        performance = st.slider("Performance Score (1-100)", 1, 100, 75)
        submit = st.form_submit_button("Add Employee")

        if submit:
            mycursor.execute(
                "INSERT INTO employees (EmployeeName, EmployeeContact, EmployeeEmail, Department, Position, Salary, Attendance, Performance_Score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (name, contact, email, department, position, salary, attendance, performance)
            )
            conn.commit()
            st.success("✅ Employee added successfully!")
            mycursor.close()
            conn.close()

            # Display employees
            df = pd.read_sql("SELECT * FROM employees", conn)
            st.dataframe(df)

# Analytics
elif menu == "Analytics":
    conn = get_connection()
    mycursor = conn.cursor()
    st.title("HR Analytics")
    df = pd.read_sql("SELECT * FROM employees", conn)
    conn.close()

    if not df.empty:
        st.subheader("Department Distribution")
        fig = px.histogram(df, x='department', title='Employee Count by Department')
        st.plotly_chart(fig)

        st.subheader("Performance vs. Attendance")
        fig = px.scatter(df, x='attendance', y='performance_score', color='department',
                         title='Attendance vs Performance')
        st.plotly_chart(fig)
    else:
        st.warning("No data available.")

# Salary & Payroll

elif menu == "Salary & Payroll":
    conn = get_connection()

    st.title("Salary Analysis")
    df = pd.read_sql("SELECT * FROM employees", conn)
    conn.close()

    if not df.empty:
        st.subheader("Salary Distribution")
        fig = px.box(df, y='Salary', title='Salary Range Across Employees')
        st.plotly_chart(fig)
    else:
        st.warning("No data available.")

# Leave Management
elif menu == "Leave Management":
    conn = get_connection()
    mycursor = conn.cursor()
    st.title("Leave Requests")

    # Leave Request Form
    with st.form("leave_request_form"):
        employee_id = st.number_input("Employee ID", min_value=1)
        employee_name = st.text_input("Employee Name")
        leave_type = st.selectbox("Leave Type",
                                  ["Sick Leave", "Annual Leave", "Maternity Leave", "Paternity Leave", "Unpaid Leave"])
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        submit_leave = st.form_submit_button("Submit Leave Request")

        if submit_leave:
            mycursor.execute(
                "INSERT INTO leave_requests (EmployeeID,EmployeeName, LeaveType, StartDate, EndDate) VALUES (%s, %s, %s, %s, %s)",
                (employee_id, employee_name, leave_type, start_date, end_date))
            conn.commit()
            st.success("Leave request submitted successfully!")
            mycursor.close()
            conn.close()

    # Display Leave Requests
    leave_df = pd.read_sql("SELECT * FROM leave_requests", conn)
    st.dataframe(leave_df)
    conn.close()





