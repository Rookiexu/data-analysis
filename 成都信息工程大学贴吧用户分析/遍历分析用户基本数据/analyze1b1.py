import pymysql as SQL
import database as DBS
import csv
import Analyzer

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
print('open postdata.csv')
f = open("postdata.csv","r",encoding='utf-8',errors='ignore')
wr = csv.reader(f)
f = open("result.csv","w",encoding='utf-8',errors='ignore')
csvw = csv.writer(f)
#首先统计一次数据集文件中有多少位不同的用户
differuserlist = []
i = 0
print("finding user ",end='\r')
for line in wr:
    print("finding user ",i,end='\r')
    if len(line) > 3:
        if line[2] in analyzeduserlist or line[2] in differuserlist:
            continue
        differuserlist.append(line[2])
        i+=1
dlen = len(differuserlist)
print('\n',dlen," users found!")

#再根据用户数进行遍历，多次在文件内进行查找用户信息
i = 0
xresult = []
for username in differuserlist:
    sum_count = 0
    sum_at90 = []
    sum_ur = []
    sum_kmap = []
    sum_azone = []
    print("processing..." , str(i) , "/" , dlen,end='\r')
    #以上几个变量是用于算总量的,下面的代码用于循环读取文件内容并分析（从节约内存的角度考虑，我们需要循环读取）
    f.seek(0) # seek to the begining of the file
    m = 0
    dataset = []
    while True:
        x = 0
        m+=1
        for line in wr:
            if len(line) !=0:
                x+=1
                dataset.append(line)
            if x == READ_BUFFER_SIZE:
                break
        if x == 0: #when i = 0 which means eof met.
            break
        #对读取到的数据进行分段分析
        #首先获得该用户的累计发帖量与30天发帖量
        sum_count += Analyzer.getTotalPostsSum(username,dataset)
        #其次分析该用户的活跃时间段
        #azone = Analyzer.getActivityTimeZone(username,dataset)
        #在分析其90天的活跃度
        #at90 = Analyzer.getActivityTimeLine(username,90,dataset)
        #然后分析用户关系链
        #ur = Analyzer.getReadlationCircle(username,dataset)
        #然后分析该用户的常用关键字
        #kmap = Analyzer.getKeymap(username,dataset)
        #=======================基本信息分析完成，汇总数据=============================
        #sum_count += count
    #id，累计发帖量，近30天发帖量，活跃度，活跃时间段，用户关系链，常用关键字，保留
    wstr = [str(username),str(sum_count),"0",sum_at90,sum_azone,sum_ur,sum_kmap,"1"]
    xresult.append(wstr)
    i+=1
#[print(x[1],end='\t') for x in xresult]
#print("\nsaving....")
#csvw.writerows(xresult)

#print("\ndone.")
f.close()
f.close()