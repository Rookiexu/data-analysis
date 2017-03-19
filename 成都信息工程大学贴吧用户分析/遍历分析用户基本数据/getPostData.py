import database as DBS
import pymysql as SQL
import csv

#该文件用户从数据库下载所有回帖数据，然后将其存放在目录下名为 postdata.csv的文件夹中


print("conecting to the database...")
DBCONN = SQL.connect(host=DBS.HOST, port=3306,user=DBS.USER,passwd=DBS.PASSWORD,db=DBS.NAME,charset='UTF8')
DBCUR = DBCONN.cursor()
print("downloading data...")
SEL = "SELECT * FROM `postdata`  WHERE 1"
DBCUR.execute("SET names 'utf8mb4'")
DBCUR.execute(SEL)
DBCONN.commit()
print("fetch_all...")
result = DBCUR.fetchall()
print("done.")
DBCUR.close()
DBCONN.close()
print("close connection.")
print("data retrived=",len(result))
print("saving data...")
f = open("postdata.csv","w",encoding='utf-8',errors='ignore')
wr = csv.writer(f)
wr.writerows(result)
f.close()
print("application completed!")