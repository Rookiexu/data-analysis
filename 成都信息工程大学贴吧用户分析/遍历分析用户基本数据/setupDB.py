import database as DBS
import pymysql as SQL
import csv


#该脚本用于读取 postdata.csv 然后，针对每一个独立用户在数据库里面建立相应的索引
#postdata.csv结构
#从postdata.csv读取数据
result = []
print('open postdata.csv')
f = open("postdata.csv","r",encoding='utf-8',errors='ignore')
wr = csv.reader(f)
i = 0
for line in wr:
    if len(line) !=0:
        i+=1
        print("reading data....",line[4],i,end='\r')
        result.append(line)
f.close()
print('done.\ndata retrived:',len(result))
print('start setup database record for every user.')
#获取所有独立用户，然后为每个独立用户在数据库建立相应的record
#[帖子ID    储存贴吧名   回帖作者  回帖内容    回帖日期    回帖目标]
#   0          1           2        3           4         5
distinctUserList = []
i = 0
sumx = len(result)
for post in result:
    i+=1
    print("gathering distinct user...",i,"/",sumx,end='\r')
    if post[2] not in distinctUserList:
        distinctUserList.append(post[2])
print("\ndone.\n",len(distinctUserList),"distinct users gathered\nStart submit to databse.")
#开始数据库提交事务
print("conecting to the database...")
DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORLD_CH,db=DBS.NAME_CH,charset='UTF8')
DBCUR = DBCONN.cursor()
DBCUR.execute("SET names 'utf8mb4'")
#首先要获取数据库中已经存在的用户,方便跳过
print("retriving exist user list...")
SEL = "SELECT USERNAME FROM `tieba_user_bigdate` WHERE 1"
DBCUR.execute(SEL)
DBCONN.commit()
existlist = DBCUR.fetchall()
print(len(existlist),"users exist,they will be skipped.")
print("submitting data...")
INS_SUFFIX = "INSERT INTO `tieba_user_bigdate`( `USERNAME`, `POSTTOTAL`, `POST30DAYS`,`ACTIVETIMELINE`, `ACTIVETIMEZONE`,\
             `USERRELATION`, `REPLYKEYWORD`, `RESERVE`) VALUES ("
i = 0
skips = 0
sumx = len(distinctUserList)
for user in distinctUserList:
    if user not in existlist:
        INS =INS_SUFFIX + "\"" + user + "\",0,0,\"\",\"\",\"\",\"\",\"\")"
        DBCUR.execute(INS)
        i+=1
    else:
        skips+=1
    print("submiting...",i,"/",sumx,"(",skips,"skipped)",end='\r')
print("\ncommiting...")
DBCONN.commit()
print("done.")
DBCUR.close()
DBCONN.close()