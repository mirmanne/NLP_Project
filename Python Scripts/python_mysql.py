import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password"
)

my = mydb.cursor()
my.execute("CREATE DATABASE ASSIGNMENT")