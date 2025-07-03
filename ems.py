import mysql.connector as mysql
import os
from dotenv import load_dotenv

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD") # Get password from .env

def dbConnection():
    return mysql.connect(
        host = "localhost",
        user = "root",
        password = DB_PASSWORD,
        database = "ems_python"
    )

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
    


print(signup(userName= "mjshubham21", email= "123@456.com", password= "12345678"))

# Login
def login(userName, password):
    conn = dbConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registration WHERE userName = %s AND password = %s", (userName, password))
    if cursor.fetchone():
        return "Login successful"
    else:
        return "Login failed"
    

print(login(userName= "mjshubham21", password= "12345678"))

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

# View all employees function:
def viewAllEmp():
    conn = dbConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employee")
    rows = cursor.fetchall()
    for row in rows:
        print(f"eid: {row[0]}, eName: {row[1]}, eEmail: {row[2]}, eSalary: {row[3]}, eAddress: {row[4]}")
    conn.close()

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
# eid = int(input("Enter New Employee ID: "))
# eName = input("Enter New Employee Name: ")
# eEmail = input("Enter New Employee Email: ")
# eSalary = int(input("Enter New Employee Salary: "))
# eAddress = input("Enter New Employee Address: ")
# print(updateEmp(eid, eName, eEmail, eSalary, eAddress))

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