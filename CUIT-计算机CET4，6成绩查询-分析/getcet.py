# coding: utf-8
import requests
import csv
from bs4 import BeautifulSoup

exam_season = [
    20161217,
    20160618,
    20151219
]

exam_type = [
    '大学英语国家六级'.encode('GB2312'),
    "大学英语国家四级".encode('GB2312')
]

sdata = {
    "func":"login",
    'Op':'大学英语国家六级'.encode('GB2312'),
    'hdName':'',
    'HdXm':"张龙".encode('GB2312'),
    'TheTime':20161217,
    'imageField22.x':18,
    'imageField22.y':13
}

#用于请求cookies
header = {
    'Host': 'jxgl.cuit.edu.cn',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,en-US;q=0.8,en;q=0.6,zh;q=0.4'
}

#用于请求成绩
headerget = {
    'Host': 'jxgl.cuit.edu.cn',
    'Connection': 'keep-alive',
    'Content-Length': '140',
    'Cache-Control': 'max-age=0',
    'Origin': 'http://jxgl.cuit.edu.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #'Referer': 'http://jxgl.cuit.edu.cn/Jxgl/Djks/Default.asp?Op=%B4%F3%D1%A7%D3%A2%D3%EF%B9%FA%BC%D2%C1%F9%BC%B6',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.8,en;q=0.6,zh;q=0.4'
}

#该函数用于生成查询字符串
def genQuery(name):
    try:
        sdata['HdXm'] = name.encode('GB2312')
    except:
        sdata['HdXm'] = name.encode('GB18030')
    return sdata

def cacluateScore(a,b,c):
    return int(a) + int(b) + int(c)

#学号，确保是指定学院的，默认为计算机学院15级
def isCS(sid3,schoolhead="201505"):
    if sid3.find(schoolhead) < 0:
        return False
    return True

#当存在重名的时候，我们通过这个限制条件确保查询的人的确是我们希望
#查询的那个人，通过学号确保
def isStudentWeWant(sidinfo,stuid):
    if sidinfo[2] == stuid:
        return True
    return False

#该函数用于匹配出一个学生的姓名，考号，学号，姓名，性别，总分，缺考，违纪，听力，阅读，写作，综合
def match(html,year,extype,majorclass,stuid):
    #提取数据所在表格
    spos = html.find("<TBODY><TR VALIGN=top ALIGN=left><TD bordercolor=#000000 bordercolorlight=#000000 bordercolordark=#FFFFFF align=\"Center\" valign=bottom>")
    epos = html.find("</TBODY>",spos)
    html = html[spos:epos]
    soup = BeautifulSoup(html,"html.parser")
    tds = soup.find_all('td')
    result = []
    subresult = []
    xc = 0
    for td in tds:
        buf = ""
        try:
            buf = td.find('font').contents[0]
        except Exception as e:
            buf = "ERROR:" + str(e)
        buf = buf.replace('\r\n','').replace('\n','')
        if xc < 12:
            subresult.append(buf)
            xc+=1
        else:
            #将查询到的记录添加到记录集中
            #在这里我们需要判断查询到的用户是否和目标用户一样
            #通过学号判断,由于每一次我们仅会查询一个，故找到目标用户后我们就应该
            #跳出循环，返回结果
            if len(subresult) > 0 and isStudentWeWant(subresult,stuid): #isCS(subresult[2]):
                #print(subresult)
                #手动计算总分
                subresult[5] = cacluateScore(subresult[8],subresult[9],subresult[10])
                subresult[0] = year
                subresult[7] = majorclass
                subresult[11] = extype
                result.append(subresult.copy())
                subresult.clear()
                break
            subresult.clear()
            subresult.append(buf)
            xc = 1
    if len(subresult) > 0 and isStudentWeWant(subresult,stuid): #isCS(subresult[2]):
        subresult[5] = cacluateScore(subresult[8],subresult[9],subresult[10])
        subresult[0] = year
        subresult[7] = majorclass
        subresult[11] = extype
        result.append(subresult.copy())
    return result


#获取必要session
session = requests.Session() 
session.get("http://jxgl.cuit.edu.cn/Jxgl/Djks/Default.asp?Op=%B4%F3%D1%A7%D3%A2%D3%EF%B9%FA%BC%D2%C1%F9%BC%B6",headers=header) 
print(session.cookies.get_dict())

#加载学生列表
f = open("slist_csa.txt","rb")
sstr = f.read()
sstr = sstr.decode("UTF-8","ignore")
f.close()
slist = sstr.split(",")
ssum = len(slist)
#print(slist,"\n学生数量：",ssum)
print("学生数量：",ssum)
#开始循环处理
result = []  #储存结果
#开始查询,我们要遍历查询是4级，6级，每一年（从开学到现在）所有数据
#用第一列（序号）代表考试年份（见前面的数组），最后一列（综合）代表考试类型（4，6级别）

#4级，6级
processed = 0
ssum *= len(exam_type) * len(exam_season) 
#下面为查询2016级学生的时候需要跳过的列表
skip_year = [20160618,20151219]
skip_exam = ['大学英语国家六级'.encode('GB2312')]
for extype in exam_type:
    #考试时间
    for exsea in exam_season:
        #学生列表
        sdata['Op'] = extype
        sdata['TheTime'] = exsea
        for student in slist:
            if len(student) > 1:
                # stu结构： [ 学生姓名,班级,学号 ] 
                stu = student.split(":")
                try:
                    print("正在查询",stu[0],"在",exsea,"进行的" + extype.decode("GB2312") +"...",end='\t\t\t')
                except Exception as e:
                    print("输出出错\t\t\t字符无法输出" + extype.decode("GB2312") +"...",end='\t\t\t')
                #如果学号前4位为2016，则只有四级成绩（2016年12月的），故需要跳过该类学生
                #下面这个if用于手动跳过2016级学生的六级全部，四级除2016-12月份之外的查询
                if stu[2][:4] == "2016" and (exsea in skip_year or extype in skip_exam):
                    processed+=1
                    print("跳过\t",processed,"/",ssum)
                    continue 
                #请求数据
                r = None
                try:
                    r = session.post("http://jxgl.cuit.edu.cn/Jxgl/Djks/Default.asp", data=genQuery(stu[0]),headers=headerget)
                except Exception as e:
                    print(e)
                    continue
                #print(r.status_code, r.reason)
                #print(r.headers)
                #重新编码，防止中文乱码
                print("完成\n\t\t\t\t\t\t\t解析数据...",end='\t')
                shtml = r.text.encode(r.encoding).decode('GB2312','ignore')
                xsresult = match(shtml,exsea,extype.decode("GB2312"),stu[1],stu[2])
                result.extend(xsresult)
                processed+=1
                print("完成\t",processed,"/",ssum)

#储存到文件
header = ["考试年份","准考证号","学号","姓名","性别","总分","缺考","违纪","听力","阅读","写作","考试类型"]
result.insert(0,header)
f = open("result.csv","w")
wcsv = csv.writer(f)
print("数据总量：",len(result),";原始数据长度:",ssum/len(exam_type)/len(exam_season) )
wcsv.writerows(result)
f.close()