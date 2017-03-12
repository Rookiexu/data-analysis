import csv
import ast
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
font_set = FontProperties(fname="SIMLI.TTF", size=20)
#该脚本的作用是分析由 generateTable.py 得到的汇总数据
#源数据格式如下：
#[学号,考号,姓名,班级, [  [成绩1：考试时间,类型,缺考,总分,听力,阅读,写作],[成绩2：考试时间,类型,总分,听力,阅读,写作]  ] ]
#  0    1   2    3                                                 4

GRAPH_TITLE = "计算机学院"

CET4 = "大学英语国家四级"
CET6 = "大学英语国家六级"

exam_season = [
    '20161217',
    '20160618',
    '20151219',
    '20150613',
    '20141220',
    '20140614',
    '20131214'
]

def todo(tips):
    ops = input(">>>>>"+tips+"(Y/N)")
    if ops == "Y" or ops == "y" or len(ops) == 0:
        return True
    return False

def wantsave(filename,datalist,tips="是否要储存结果记录集？"):
    ops = input(">>>>>"+tips+"(Y/N)")
    if ops == "Y" or ops == "y" or len(ops) == 0:
        f = open(filename,"w")
        csvw = csv.writer(f)
        csvw.writerows(datalist)
        f.close()
        print(">>>>>结果记录集已经储存至",filename)

#数据筛选函数，通过这个函数可以筛选出指定学院/指定年级的数据
#如果要过滤该学生，该函数返回true，否则返回false
def filterStudent(student):
    #student 变量应该为一个list，其结构如下：
    # [学号,考号,姓名,班级,[[成绩1：考试时间,类型,缺考,总分,听力,阅读,写作],[成绩2：考试时间,类型,总分,听力,阅读,写作]]
    #通过学号筛选,学号例如 ： 2015 05 1152
    #修改下面的if块来修改筛选条件
    if student[0][4:6] == "05": #and student[0][0:4] != "2016": #筛选出计算机学院
    #if student[0][:6] == "201305": 
        #这里筛选出计算机学院2013级学生
        return False
    return True


stulist = []
#载入数据集
print("\n\n加载数据...")
f = open('csCET46list.csv','r')
csvr = csv.reader(f)
for line in csvr:
    if len(line) > 1 and filterStudent(line) == False:
        line[4] = ast.literal_eval(line[4])
        stulist.append(line)
f.close()
del stulist[0]
dllen = len(stulist)
print("数据总数：",dllen,end='\n\n---\n')

#求极差
if todo("是否要计算每一名同学的CET4与CET6极差?"):
    v426list = []
    #开始求极差
    dissmissed = 0
    counted = 0
    for stu in stulist:
        print(stu)
        #分类成绩list
        #[成绩1：考试时间,类型,缺考,总分,听力,阅读,写作]
        #           0     1   2    3    4   5    6
        cet4 = [ x for x in stu[4] if x[1]==CET4  ]
        cet6 = [ x for x in stu[4] if x[1]==CET6  ]
        #求4，6级极差
        if len(cet6) == 0:
            print("没有考六级。")
            dissmissed +=1
        elif len(cet4) == 0:
            print("没有考4级。")
            dissmissed +=1
        else:
            #[学号,考号,姓名,班级, [ 成绩列表 ] ]
            mincet4 = min( [ int(x[3]) for x in cet4  ] )
            maxcet6 = max( [ int(x[3]) for x in cet6  ] )
            v426 = maxcet6 - mincet4
            v426list.append([stu[2],v426])
            counted +=1
    v426list.sort(key=lambda x:x[1])
    for x in v426list:
        print(x[0],",",x[1])
    print("\n----\n原始数据共",dllen,";其中有",dissmissed,"名学生因为没有考四或六级而被跳过;剩余有效数据",counted,"条。\n")
    wantsave("result_extreme_deviation.csv",v426list)

#求听力，阅读，写作对总分的贡献情况
if True:
    #首先需要数据分类
    #[学号,考号,姓名,班级, [  [成绩1：考试时间,类型,缺考,总分,听力,阅读,写作],[成绩2：考试时间,类型,总分,听力,阅读,写作]  ] ]
    #本次分类后得到的数据为每一年四六级的数据数组
    # 下面两个list的数据结构如下：
    # [  [考试年份1,[ 成绩列表:考试时间,类型,缺考,总分,听力,阅读,写作 ]]， [考试年份2,[ 成绩列表:学生信息 ]],[考试年份3,[ 成绩列表:学生信息 ]],......   ]
    CET4SCORE = []
    CET6SCORE = []
    #构造符合以上条件的结构体
    for season in exam_season:
        CET4SCORE.append( [ season , [ y+[x[0]] for x in stulist for y in x[4] if y[0] == season and y[1] == CET4 ].copy() ] )
        CET6SCORE.append( [ season , [ y+[x[0]] for x in stulist for y in x[4] if y[0] == season and y[1] == CET6 ].copy() ] )
    print("\n---\n进行分类后的数据长度,CET4：",sum([ len(x[1]) for x in CET4SCORE ]),",CET6：",sum([len(x[1]) for x in CET6SCORE]),"(大多数人考了不止一次)")
    print("其中，CET4成绩包含",[x[0] for x in CET4SCORE],"时间段的数据\nCET6包含",[x[0] for x in CET6SCORE],"时间段的数据\n---")
    #开始绘制图表
    #绘制CET4，所有时间段的成绩数据（隐藏姓名）
    if todo("是否显示四级成绩在过去几次考试中的变化趋势？"):
        #所有成绩排序后绘制
        cet4val = []
        cet4x = []
        cet4label = []
        for cet4 in CET4SCORE:
            #[考试年份1,[ 成绩列表:[考试时间,类型,缺考,总分,听力,阅读,写作] ]]
            #print("len_cet4_x@cet4[1]=",len(cet4[1]))
            cet4val.append([ x[3] for x in cet4[1] ])
            cet4label.append(cet4[0])
        print("CET4每一年的参考人数：",[ len(x) for x in cet4val])
        for v in cet4val:
            cet4x.append( range(1,len(v)+1) )
        x = 0
        for v in cet4val:
            cet4val[x].sort(reverse=True)
            x+=1
        with plt.style.context('fivethirtyeight'):
            colors = ['b','g','r','c','m','y','k']
            x=0
            plt.plot([0,max([len(x) for x in cet4x])],[425,425],label="425 line",color='gainsboro')
            for v in zip(cet4x,cet4val,cet4label):    
                plt.plot(v[0],v[1],label=v[2],color=colors[x])
                plt.title(GRAPH_TITLE+"四级成绩变化趋势(2013级) - by Kanch",fontproperties=font_set)
                plt.xlabel("参考人数(一个数字为一个个体,姓名被隐藏)",fontproperties=font_set)
                plt.ylabel("四级得分",fontproperties=font_set)
                plt.legend(loc='upper right')
                x+=1
            plt.show()
        if todo("是否显示四级成绩在过去几次考试中的通过率以及最高成绩，最低成绩和平均分？"):
            caldata = [] #结构:[考试时间，通过率，最高分，最低分，平均分]
            for cet4 in CET4SCORE:
                #[考试年份1,[ 成绩列表:[考试时间,类型,缺考,总分,听力,阅读,写作] ]]
                #通过这个循环，将会得到每一次考试的通过率以及最高成绩，最低成绩和平均分
                passrate = str(round(len([x[3] for x in cet4[1] if int(x[3])>=425])/len(cet4[1])*100,2))+"%"
                maxs = max(cet4[1],key=lambda x:x[3])[3]
                rv = [x[3] for x in cet4[1] if x[3] != "0"]
                mins = min(rv)
                caldata.append([ cet4[0],passrate,maxs,mins ])
            caldata.reverse()
            print(caldata)
            #绘制通过率图
            with plt.style.context('fivethirtyeight'):
                xv = [caldata.index(x)+1 for x in caldata]
                plt.xticks(xv,[x[0][0:4]+"-"+x[0][4:6] for x in caldata])
                plt.plot(xv,[float(x[1].replace("%",'')) for x in caldata])
                plt.title(GRAPH_TITLE+"四级通过率变化趋势(2013级) - by Kanch",fontproperties=font_set)
                plt.xlabel("考试年份",fontproperties=font_set)
                plt.ylabel("四级通过率(%)",fontproperties=font_set)
                plt.show()
                #绘制最高分以及最低分图
                plt.xticks(xv,[x[0][0:4]+"-"+x[0][4:6] for x in caldata])
                plt.plot(xv,[x[2] for x in caldata],label="Max Score")  #最高得分
                plt.plot(xv,[x[3] for x in caldata],label="Min Score (excluding 0)")  #最低分（除0）
                plt.title(GRAPH_TITLE+"四级最高分与最低分变化趋势(2013级) - by Kanch",fontproperties=font_set)
                plt.xlabel("考试年份",fontproperties=font_set)
                plt.ylabel("考试分数",fontproperties=font_set)
                plt.legend(loc='upper right')
                plt.show()



    if todo("是否显示六级成绩在过去几次考试中的变化趋势？"):
        #绘制六级成绩变化趋势，姓名被隐藏
        #所有成绩排序后绘制
        cet6val = []
        cet6x = []
        cet6label = []
        for cet6 in CET6SCORE:
            #[考试年份1,[ 成绩列表:[考试时间,类型,缺考,总分,听力,阅读,写作] ]]
            #print("len_cet4_x@cet4[1]=",len(cet4[1]))
            cet6val.append([ x[3] for x in cet6[1] ])
            cet6label.append(cet6[0])
        print("CET6每一年的参考人数：",[ len(x) for x in cet6val])
        for v in cet6val:
            cet6x.append( range(1,len(v)+1) )
        x = 0
        for v in cet6val:
            cet6val[x].sort(reverse=True)
            x+=1
        with plt.style.context('fivethirtyeight'):
            colors = ['b','g','r','c','m','y','k']
            x=0
            plt.plot([0,max([len(x) for x in cet6x])],[425,425],label="425 line",color='gainsboro')
            for v in zip(cet6x,cet6val,cet6label):
                plt.plot(v[0],v[1],label=v[2],color=colors[x])
                plt.title(GRAPH_TITLE+"六级成绩变化趋势(2013级) - by Kanch",fontproperties=font_set)
                plt.xlabel("参考人数(一个数字为一个个体,姓名被隐藏)",fontproperties=font_set)
                plt.ylabel("六级得分",fontproperties=font_set)
                plt.legend(loc='upper right')
                x+=1
            plt.show()
        if todo("是否显示六级成绩在过去几次考试中的通过率以及最高成绩，最低成绩和平均分？"):
            caldata = [] #结构:[考试时间，通过率，最高分，最低分，平均分]
            for cet6 in CET6SCORE:
                #[考试年份1,[ 成绩列表:[考试时间,类型,缺考,总分,听力,阅读,写作] ]]
                #通过这个循环，将会得到每一次考试的通过率以及最高成绩，最低成绩和平均分
                if len(cet6[1]) == 0:
                    continue
                passrate = str(round(len([x[3] for x in cet6[1] if int(x[3])>=425])/len(cet6[1])*100,2))+"%"
                maxs = max(cet6[1],key=lambda x:x[3])[3]
                rv = [x[3] for x in cet6[1] if x[3] != "0"]
                mins = min(rv)
                caldata.append([ cet6[0],passrate,maxs,mins ])
            caldata.reverse()
            print(caldata)
            #绘制通过率图
            with plt.style.context('fivethirtyeight'):
                xv = [caldata.index(x)+1 for x in caldata]
                plt.xticks(xv,[x[0][0:4]+"-"+x[0][4:6] for x in caldata])
                plt.plot(xv,[float(x[1].replace("%",'')) for x in caldata])
                plt.title(GRAPH_TITLE+"六级通过率变化趋势(2013级) - by Kanch",fontproperties=font_set)
                plt.xlabel("考试年份",fontproperties=font_set)
                plt.ylabel("六级通过率(%)",fontproperties=font_set)
                plt.show()
                #绘制最高分以及最低分图
                plt.xticks(xv,[x[0][0:4]+"-"+x[0][4:6] for x in caldata])
                plt.plot(xv,[x[2] for x in caldata],label="Max Score")  #最高得分
                plt.plot(xv,[x[3] for x in caldata],label="Min Score (excluding 0)")  #最低分（除0）
                plt.title(GRAPH_TITLE+"六级最高分与最低分变化趋势(2013级) - by Kanch",fontproperties=font_set)
                plt.xlabel("考试年份",fontproperties=font_set)
                plt.ylabel("考试分数",fontproperties=font_set)
                plt.legend(loc='upper right')
                plt.show()
    
    if True:
        #这里的代码专用于计算机学院，如果你要分析其它学院，请删掉这里的if块
        #绘制计算机学院2013级，2014级，2015级在同时间段内的过级情
        everylevel = []  #[年级，过级率，最高分，最低分，平均分]
        for cet4 in CET4SCORE:
            #抽取出每一届的第一次四级情况
            #[考试时间,类型,缺考,总分,听力,阅读,写作,学号]
            if(len(cet4[1])) == 0 or cet4[0][4:6]!="12":
                continue
            passrate = str(round(len([x[3] for x in cet4[1] if int(x[3])>=425 and x[7][:4] == cet4[0][:4]])/len(cet4[1])*100,2))+"%"
            maxs = max(cet4[1],key=lambda x:x[3])[3]
            rv = [x[3] for x in cet4[1] if x[3] != "0"]
            mins = min(rv)
            avg = round(sum([int(x[3]) for x in cet4[1]])/len(cet4[1]),2)
            everylevel.append([ cet4[0][:4],passrate,maxs,mins,avg ])
        everylevel.reverse()
        print(everylevel)
        #绘制图表
        with plt.style.context('fivethirtyeight'):
            xv = [everylevel.index(x)+1 for x in everylevel]
            plt.xticks(xv,[x[0]+"级" for x in everylevel])
            plt.plot(xv,[float(x[1].replace("%",'')) for x in everylevel])
            plt.title(GRAPH_TITLE+"第一次四级通过率对比图 - by Kanch",fontproperties=font_set)
            plt.xlabel("年级",fontproperties=font_set)
            plt.ylabel("四级通过率(%)",fontproperties=font_set)
            plt.show()
            #绘制最高分以及最低分图
            plt.xticks(xv,[x[0]+"级" for x in everylevel])
            plt.plot(xv,[x[2] for x in everylevel],label="Max Score")  #最高得分
            plt.plot(xv,[x[3] for x in everylevel],label="Min Score (excluding 0)")  #最低分（除0）
            plt.plot(xv,[x[4] for x in everylevel],label="Average Score")  #平均分
            plt.title(GRAPH_TITLE+"第一次四级最高分与最低分与平均分对比图 - by Kanch",fontproperties=font_set)
            plt.xlabel("年级",fontproperties=font_set)
            plt.ylabel("考试分数",fontproperties=font_set)
            plt.legend(loc='middle right')
            plt.show()

        
