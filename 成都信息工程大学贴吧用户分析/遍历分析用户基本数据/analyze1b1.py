import BigDataQueryAPI as QueryAPI
import termanalyze as TermAnalyze
import pymysql as SQL
import database as DBS
import csv

#该脚本用于从目录下的postdata.csv读取数据并用于分析
#分析用户的活跃时间段，活跃度，关键字，关系链等

#采用多次从文件读取的方法（节约内存）
#下面这个变量定义了每次要从文件中读取的行数
READ_BUFFER_SIZE = 5000


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
DBCUR.close()
DBCONN.close()
#打开数据集文件
result = []
print('open postdata.csv')
f = open("postdata.csv","r",encoding='utf-8',errors='ignore')
wr = csv.reader(f)
f = open("result.csv","w",encoding='utf-8',errors='ignore')
csvw = csv.writer(f)
#首先统计一次数据集文件中有多少位不同的用户
differuserlist = []
i = 0
for line in wr:
    print("finding user ",i,end='\r')
    if len(line) > 3:
        if line[2] in analyzeduserlist or line[2] in differuserlist:
            continue
        differuserlist.append(line[2])
        i+=1
print('\n',len(differuserlist)," users found!")
#再根据用户数进行遍历，多次在文件内进行查找用户信息
for user in differuserlist:
    sum_count = 0
    sum_count30 = 0
    sum_at90 = []
    sum_ur = []
    sum_kmap = []
    #以上几个变量是用于算总量的,下面的代码用于循环读取文件内容并分析（从节约内存的角度考虑，我们需要循环读取）
    while F.EOF:
        i = 0
        for line in wr:
            if len(line) !=0:
                i+=1
                result.append(line)
            if i == READ_BUFFER_SIZE:
                break
        print('done.\ndata retrived:',len(result))
        print('setting data...')
        QueryAPI.setDataset(result)
        #result中的子项目结构：
        #[帖子ID    储存贴吧名   回帖作者  回帖内容    回帖日期    回帖目标]
        #   0          1           2        3           4         5
        #开始循环分析
        i = 0
        sumx = len(result)
        xresult = []
        for post in result:
            i+=1
            info = "process..." + str(i) + "/" + str(sumx) 
            print(info,end='\r')
            username = post[2]
            print(info,"\tstart process...                 ",end='\r')
            #首先获得该用户的累计发帖量与30天发帖量
            print(info,"\tget posts sum and 30 days sum...",end='\r')
            count,count30 = QueryAPI.getTotalPostsSum(username)
            #其次分析该用户的活跃时间段
            print(info,"\tanalyzing active timeline...     ",end='\r')
            azone = QueryAPI.getActivityTimeZone(username)
            #在分析其90天的活跃度
            print(info,"\tanalyzing active timezone...      ",end='\r')
            at90 = QueryAPI.getActivityTimeLine(username,90)
            #然后分析用户关系链
            print(info,"\tanalyzing user relation...        ",end='\r')
            ur = QueryAPI.getReadlationCircle(username)
            #然后分析该用户的常用关键字
            print(info,"\tanalyzing keyword...               ",end='\r')
            kmap = QueryAPI.getKeymap(username)
            #基本信息分析完成，储存信息到文件

    #id，累计发帖量，近30天发帖量，活跃度，活跃时间段，用户关系链，常用关键字，保留
    wstr = [str(username),str(count),str(count30),at90,azone,ur,kmap,"1"]
    xresult.append(wstr)
    print("\nsaving....")
    csvw.writerows(xresult)

print("\ndone.")
f.close()
f.close()