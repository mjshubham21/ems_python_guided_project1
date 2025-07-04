import mysql.connector as mysql
import os
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD") # Get password from .env
DB_NAME = os.getenv("DB_NAME")

def dbConnection():
    return mysql.connect(
        host = "localhost",
        user = "root",
        password = DB_PASSWORD,
        database = DB_NAME
    )

def signup(userName, email, password):
    conn = dbConnection()
    cursor = conn.cursor()
    if not userName or not email or not password:
        return "Please fill all the fields"
    
    cursor.execute("SELECT * FROM registration WHERE userName = %s", (userName,))
    if cursor.fetchone():
        return "Username already exists"

    cursor.execute("SELECT * FROM registration WHERE email = %s", (email,))
    if cursor.fetchone():
        return "Email already exists"
    
    if len(password) < 8:
        return "Password must be at least 8 characters"
      
    cursor.execute("INSERT INTO registration (userName, password, email) VALUES (%s, %s, %s)", (userName, password, email))
            
    conn.commit()
    conn.close()

    return "Registration successful" if cursor.rowcount > 0 else "Registration failed"

def login(userName, password):
    conn = dbConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registration WHERE userName = %s AND password = %s", (userName, password))
    if cursor.fetchone():
        print("Login successful\n")
        options()
    else:
        print("Login failed\n")

# ------------------ EMPLOYEE CRUD OPERATIONS ------------------

def createEmp(eid, eName, eEmail, eSalary, eAddress):
    conn = dbConnection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employee (eid, eName, eEmail, eSalary, eAddress) VALUES (%s, %s, %s, %s, %s)",
                   (eid, eName, eEmail, eSalary, eAddress))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        print("Employee created successfully")
    else:
        print("Employee creation failed")

def viewAllEmp():
    conn = dbConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employee")
    rows = cursor.fetchall()
    conn.close()

    # Define column headers
    headers = ["EID", "Employee Name", "Email", "Salary", "Address"]

    # Print table using tabulate
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def viewEmpByID(eid):
    conn = dbConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employee WHERE eid = %s", (eid,))
    row = cursor.fetchone()
    conn.close()
    if row:
        print(f"eid: {row[0]}, eName: {row[1]}, eEmail: {row[2]}, eSalary: {row[3]}, eAddress: {row[4]}")
    else:
        print("Employee not found.")

def updateEmp(eid, eName, eEmail, eSalary, eAddress):
    conn = dbConnection()
    cursor = conn.cursor()
    cursor.execute("UPDATE employee SET eName = %s, eEmail = %s, eSalary = %s, eAddress = %s WHERE eid = %s",
                   (eName, eEmail, eSalary, eAddress, eid))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        print("Employee updated successfully")
    else:
        print("Employee update failed")

def deleteEmp(eid):
    conn = dbConnection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employee WHERE eid = %s", (eid,))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        print("Employee deleted successfully")
    else:
        print("Employee deletion failed")

# ------------------ OPTIONS AFTER LOGIN ------------------

def options():
    while True:
        print("\nSelect an operation:")
        print("1. Create Employee")
        print("2. View All Employees")
        print("3. View Employee by ID")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("---------------------------")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            eid = int(input("Enter Employee ID: "))
            eName = input("Enter Name: ")
            eEmail = input("Enter Email: ")
            eSalary = int(input("Enter Salary: "))
            eAddress = input("Enter Address: ")
            createEmp(eid, eName, eEmail, eSalary, eAddress)

        elif choice == '2':
            viewAllEmp()

        elif choice == '3':
            eid = int(input("Enter Employee ID: "))
            viewEmpByID(eid)

        elif choice == '4':
            eid = int(input("Enter Employee ID to update: "))
            eName = input("Enter new Name: ")
            eEmail = input("Enter new Email: ")
            eSalary = int(input("Enter new Salary: "))
            eAddress = input("Enter new Address: ")
            updateEmp(eid, eName, eEmail, eSalary, eAddress)

        elif choice == '5':
            eid = int(input("Enter Employee ID to delete: "))
            deleteEmp(eid)

        else:
            print("Invalid option, please try again.")

        again = input("\nDo you want to perform another operation? (Y/N): ").strip().upper()
        if again != 'Y':
            print("Logged out successfully.")
            break


# ------------------ MAIN PROGRAM ------------------

while True:
    print("\n=== Employee Management System ===")
    print("1. Sign Up")
    print("2. Login")
    print("3. Exit")
    print("---------------------------")

    main_choice = input("Enter your choice: ").strip()

    if main_choice == '1':
        userName = input("Enter username: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        print(signup(userName, email, password))

    elif main_choice == '2':
        userName = input("Enter username: ")
        password = input("Enter password: ")
        login(userName, password)

    elif main_choice == '3':
        print("Thank you for using the system. Goodbye!")
        break

    else:
        print("Invalid input. Please try again.")
