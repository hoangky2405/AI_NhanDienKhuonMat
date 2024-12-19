import mysql.connector
import datetime
from tkinter import messagebox
import time

# hàm Connection tới database
def connectdatabase():
    connection=mysql.connector.connect(
        host="localhost",
        user="root",
        database="face",
        password=""
    )
    return connection

# hàm insert nếu id nhập vào chưa có trong database và update nếu trong database đã có id
def insertOrUpdate(id,name):
    con=connectdatabase()
    query = "select * from people where id ="+str(id)
    cursor=con.cursor()
    cursor.execute(query)
    records=cursor.fetchall()
    isRecorrdExit = 0
    for row in records:
        isRecorrdExit = 1
    if(isRecorrdExit == 0):
        query = "insert into people (id,name) values (%s,%s)"
        cursor.execute(query,(id,name))
    else:
        query = "update people set name = %s where id = %s" 
        cursor.execute(query,(name,id))
    con.commit()
    con.close()
    cursor.close()

# hàm tìm kiếm People theo id
def getProfile(id):
    conn=connectdatabase()
    cmd="select * from people where id = "+str(id)
    cursor=conn.cursor()
    cursor.execute(cmd)
    records=cursor.fetchall()
    profile=None
    for row in records:
        profile=row
    conn.close()
    return profile