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
print('setting data...')
QueryAPI.setDataset(result)
print('done.')
print('start analyzing.')
#连接数据库
print("conecting to the database...")
DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORLD_CH,db=DBS.NAME_CH,charset='UTF8')
DBCUR = DBCONN.cursor()
DBCUR.execute("SET names 'utf8mb4'")
print("databse conected!")
#筛选出已经分析过的用户
SEL = "SELECT USERNAME FROM `tieba_user_bigdate` WHERE RESERVE=\"1\""
DBCUR.execute(SEL)
analyzeduserlist = DBCUR.fetchall()
analyzeduserlist = [x[0] for x in analyzeduserlist]
print(len(analyzeduserlist),"users has been analyzed,they will be skipped!")
#result中的子项目结构：
#[帖子ID    储存贴吧名   回帖作者  回帖内容    回帖日期    回帖目标]
#   0          1           2        3           4         5
#开始循环分析
procesed = []
i = 0
skipped = 0
sumx = len(result)
xresult = []
for post in result:
    i+=1
    info = "process..." + str(i) + "/" + str(sumx) + "(skipped:" + str(skipped) +")" # + post[2] + "\t"
    print(info,end='\r')
    #获取一个用户信息，然后开始分析，接着插入数据库
    if post[2] in procesed or post[2] in analyzeduserlist:
        skipped += 1
        print(info,"skipped.",end='\t')
        continue
    procesed.append(post[2])
    username = post[2]
    print(info,"\tstart process...",end='\r')
    #首先获得该用户的累计发帖量与30天发帖量
    print(info,"\tget posts sum and 30 days sum...",end='\r')
    count,count30 = QueryAPI.getTotalPostsSum(username)
    #其次分析该用户的活跃时间段
    print(info,"\tanalyzing active timeline...",end='\r')
    azone = QueryAPI.getActivityTimeZone(username)
    #在分析其90天的活跃度
    print(info,"\tanalyzing active timezone...",end='\r')
    at90 = QueryAPI.getActivityTimeLine(username,90)
    #然后分析用户关系链
    print(info,"\tanalyzing user relation...",end='\r')
    ur = QueryAPI.getReadlationCircle(username)
    #然后分析该用户的常用关键字
    print(info,"\tanalyzing keyword...",end='\r')
    kmap = QueryAPI.getKeymap(username)
    #基本信息分析完成，储存信息到文件
    #储存为csv文件，格式如下：
    #id，累计发帖量，近30天发帖量，活跃度，活跃时间段，用户关系链，常用关键字，保留
    wstr = [str(username),str(count),str(count30),at90,azone,ur,kmap,"1"]
    #print(wstr)
    xresult.append(wstr)
print("\nsaving....")
f = open("result.csv","wb",encoding='utf-8',errors='ignore')
csvw = csv.writer(f)
csvw.writerows(xresult)
f.close()
print("\ndone.")
DBCUR.close()
DBCONN.close()