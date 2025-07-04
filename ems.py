import mysql.connector as mysql
import os
from dotenv import load_dotenv

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

while True:
    # Giving menu to user.
    print("Select the operation you wanna perform:")
    print("1. Sign up")
    print("2. Login")
    print("3. Create Employee")
    print("4. View All Employees")
    print("5. View Employee based on ID")
    print("6. Update Employee")
    print("7. Delete Employee")
    print("------------------")

    choice = int(input("Enter your choice:"))

    if choice == 1:
        def signup(userName, email, password):
            conn = dbConnection()
            cursor = conn.cursor()
            if userName == "" or email == "" or password == "":
                return "Please fill all the fields"
            cursor.execute("SELECT * FROM registration WHERE userName = %s", (userName,))
            if cursor.fetchone():
                return "Username already exists"

            cursor.execute("SELECT * FROM registration WHERE email = %s", (email,))
            if cursor.fetchone():
                return "Email already exists"
            elif len(password) < 8:
                return "Password must be at least 8 characters"
            cursor.execute("INSERT INTO registration (userName, password, email) VALUES (%s, %s, %s)", (userName, password, email))
            
            conn.commit()
            conn.close()
            if cursor.rowcount > 0:
                return "Registration successful"
            else:
                return "Registration failed"
        userName = input("Enter user name:")
        email = input("Enter email:")
        password = input("Enter password:")
        print(signup(userName, email, password))

    elif choice == 2:
    # Login
        def login(userName, password):
            conn = dbConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM registration WHERE userName = %s AND password = %s", (userName, password))
            if cursor.fetchone():
                return "Login successful"
            else:
                return "Login failed"
            

        userName = input("Enter user name:")
        password = input("Enter password:")
        print(signup(userName, password))

    elif choice == 3:
        # Create Employee function:
        def createEmp(eid, eName, eEmail, eSalary, eAddress):
            conn = dbConnection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO employee (eid, eName, eEmail, eSalary, eAddress) VALUES (%s, %s, %s, %s, %s)", (eid, eName, eEmail, eSalary, eAddress))
            conn.commit()
            conn.close()
            if cursor.rowcount > 0:
                print(f"eid: {eid}, eName: {eName}, eEmail: {eEmail}, eSalary: {eSalary}, eAddress: {eAddress}")
                return "Employee created successfully"
            else:
                return "Employee creation failed"

        print("Add Employee:")
        eid = int(input("Enter Emdemoployee ID: "))
        eName = input("Enter Employee Name: ")
        eEmail = input("Enter Employee Email: ")
        eSalary = int(input("Enter Employee Salary: "))
        eAddress = input("Enter Employee Address: ")
        createEmp(eid, eName, eEmail, eSalary, eAddress)

    elif choice == 4:
        # View all employees function:
        def viewAllEmp():
            conn = dbConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employee")
            rows = cursor.fetchall()
            for row in rows:
                print(f"eid: {row[0]}, eName: {row[1]}, eEmail: {row[2]}, eSalary: {row[3]}, eAddress: {row[4]}")
            conn.close()
        viewAllEmp()

    elif choice == 5:
        # View individual employee based on ID:
        def viewEmpByID(eid):
            conn = dbConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employee where eid = %s", (eid,))
            # conn.commit()
            for el in cursor.fetchall():
                # print(el)
                print(f"eid: {el[0]}, eName: {el[1]}, eEmail: {el[2]}, eSalary: {el[3]}, eAddress: {el[4]}")
            conn.close()
        viewId = int(input("Enter the ID of employee you wanna see: "))
        viewEmpByID(viewId)

    elif choice == 6:
        # Update employee function:
        def updateEmp(eid, eName, eEmail, eSalary, eAddress):
            conn = dbConnection()
            cursor = conn.cursor()
            cursor.execute("UPDATE employee SET eName = %s, eEmail = %s, eSalary = %s, eAddress = %s WHERE eid = %s", (eName, eEmail, eSalary, eAddress, eid))
            conn.commit()
            conn.close()
            if cursor.rowcount > 0:
                print(f"eid: {eid}, eName: {eName}, eEmail: {eEmail}, eSalary: {eSalary}, eAddress: {eAddress}")
                return "Employee updated successfully"
            else:
                return "Employee update failed"
            

        print("Update Employee:")
        eid = int(input("Enter New Employee ID: "))
        eName = input("Enter New Employee Name: ")
        eEmail = input("Enter New Employee Email: ")
        eSalary = int(input("Enter New Employee Salary: "))
        eAddress = input("Enter New Employee Address: ")
        print(updateEmp(eid, eName, eEmail, eSalary, eAddress))

    elif choice == 7:
        # Delete employee based in eid function:
        def deleteEmp(eid):
            conn = dbConnection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employee WHERE eid = %s", (eid,))
            conn.commit()
            conn.close()
            if cursor.rowcount > 0:
                return "Employee deleted successfully"
            else:
                return "Employee deletion failed"
            
        print("Delete Employee:")
        eid = int(input("Enter Employee ID to delete: "))
        print(deleteEmp(eid))
    else:
        print("Enter a valid option.")
    cont = input("Do you wanna perform more operations again? (Y/N):")
    print("---------------------------")
    if cont.lower() !=  'y':
        break