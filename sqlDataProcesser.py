import pandas as pd
import mysql.connector
from mysql.connector import Error
import coreProcess

target='status'
query = "select * from tweets"

pwd='*****'
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=pwd,
        database="*****",
        charset='utf8'
    )
    if mydb.is_connected():
        print('DB connected')
        cursor = mydb.cursor()
        query = query
        cursor.execute("SHOW columns FROM tweets")
        dbcols =  [column[0] for column in cursor.fetchall()]
        cursor.execute(query)
        data = cursor.fetchall()
        df1 = pd.DataFrame(data, columns=dbcols)
        print(df1.dtypes)
        coreProcess.startProcess(df1,'Text')

except Error as e:
	print(e)


