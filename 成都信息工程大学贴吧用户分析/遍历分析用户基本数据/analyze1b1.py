import BigDataQueryAPI as QueryAPI
import termanalyze as TermAnalyze
import pymysql as SQL
import database as DBS
import csv

#该脚本用于从目录下的postdata.csv读取数据并用于分析
#分析用户的活跃时间段，活跃度，关键字，关系链等
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
print('start analyzing.')
#连接数据库
print("conecting to the database...")
DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORLD_CH,db=DBS.NAME_CH,charset='UTF8')
DBCUR = DBCONN.cursor()
DBCUR.execute("SET names 'utf8mb4'")
print("databse conected!")
#result中的子项目结构：
#[帖子ID    储存贴吧名   回帖作者  回帖内容    回帖日期    回帖目标]
#   0          1           2        3           4         5
#开始循环分析
procesed = []
i = 0
sumx = len(result)
for post in result:
    i+=1
    info = "process..." + str(i) + "/" + str(sumx)
    print(info,end='\r')
    #获取一个用户信息，然后开始分析，接着插入数据库
    if post[2] in procesed:
        continue
    procesed.append(post[2])
    #获取该用户在数据库里面的ID
    #读取所有用户信息
    SEL = "SELECT ID FROM `tieba_user_bigdate` WHERE USERNAME=\"" + post[2] +"\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    print(info,"\tretrive id...",end='\r')
    xid = DBCUR.fetchall()[0]
    print(info,"\tid retrived,id=",xid,end='\t')
    print(info,"\tstart process...",end='\t')
    #首先获得该用户的累计发帖量与30天发帖量
    print(info,"\tget total posts and latest 30 days post...",end='\t')
    count,count30 = QueryAPI.getTotalPostsSum(xid)
    #其次分析该用户的活跃时间段
    print(info,"\tanalyzing active timeline...",end='\t')
    azone = QueryAPI.getActivityTimeZone(xid)
    #在分析其90天的活跃度
    print(info,"\tanalyzing active timezone...",end='\t')
    at90 = QueryAPI.getActivityTimeLine(xid,90)
    #然后分析用户关系链
    print(info,"\tanalyzing user relation...",end='\t')
    ur = QueryAPI.getReadlationCircle(xid)
    #然后分析该用户的常用关键字
    print(info,"\tanalyzing keyword...",end='\t')
    kmap = QueryAPI.getKeymap(xid)
    #基本信息分析完成，开始提交到数据库
    

print("\ndone.")
DBCUR.close()
DBCONN.close()