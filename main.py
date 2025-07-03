# Employee Management System Pyton Project.

import mysql.connector as mysql
import os
from dotenv import load_dotenv

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD") # Get password from .env

conn = mysql.connect(
    host = "localhost",
    user = "root",
    password = DB_PASSWORD,
    database = "ems_python"
)

cursor = conn.cursor()

