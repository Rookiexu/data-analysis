import csv

#该脚本的作用是从查询到的4，6级数据中，按照以下格式将所有学生的成绩汇总，然后存入文件
# [学号,考号,姓名,班级, [  [成绩1：考试时间,类型,缺考,总分,听力,阅读,写作],[成绩2：考试时间,类型,总分,听力,阅读,写作]  ] ]
#

CET4 = "大学英语国家四级"
CET6 = "大学英语国家六级"

#加载记录集
stulist = []
f = open('result.csv','r')
csvr = csv.reader(f)
for line in csvr:
    if len(line) > 1:
        #print(line)
        stulist.append(line)
f.close()

del stulist[0]
print("数据总数：",len(stulist))
#记录集结构
# ['考试年份', '准考证号', '学号', '姓名', '性别', '总分', '缺考', '班级', '听力', '阅读', '写作', '考试类型']
#       0          1        2      3       4       5       6      7       8      9       10        11
#
#处理记录集

#筛选出大家的4，6级分值差
sidrl = []
stu46list = []  #储存每一次4，6级成绩的数据 [学号,考号,姓名,班级,[[成绩1：考试时间,类型,缺考,总分,听力,阅读,写作],[成绩2：考试时间,类型,总分,听力,阅读,写作]]
for stu in stulist:
    pid = stu[2]
    #首先找出一个学生的所有成绩
    scl = [ x for x in stulist if x[2]==pid and pid not in sidrl ]
    sidrl.append(pid)
    if len(scl) <= 0:
        if stu[2] in sidrl:
            print(stu[3],"已经处理，跳过;")
        else:
            print(stu[3],"没有考试记录;")
    else:
        print(scl[0][3],"有",len(scl),"条考试记录;",end='\t')
        #求4，6级差值
        cet4 = [ x for x in scl if x[11] == CET4 ]
        cet6 = [ x for x in scl if x[11] == CET6 ]
        print("其中有四级考试",len(cet4),"次，六级考试",len(cet6),"次.",end='\t')
        stucetinfo = [stu[2],stu[1],stu[3],stu[7],[  ]]
        #             0学号   1考号   2姓名  3班级  4成绩
        #插入学生信息数组
        for exam in cet4:
            stucetinfo[4].append( [ exam[0],exam[11],exam[6],exam[5],exam[8],exam[9],exam[10] ]  )
        for exam in cet6:
            stucetinfo[4].append( [ exam[0],exam[11],exam[6],exam[5],exam[8],exam[9],exam[10] ]  )
        stu46list.append(stucetinfo)
print("\n---\n原始数据:",len(stulist),"条,独立学生数据：",len(stu46list),"条")

f = open("csCET46list.csv","w")
csvw = csv.writer(f)
csvw.writerows(stu46list)
f.close()
