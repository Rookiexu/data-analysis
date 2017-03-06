import csv
import ast
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
font_set = FontProperties(fname="SIMLI.TTF", size=20)
#该脚本的作用是分析由 generateTable.py 得到的汇总数据
#源数据格式如下：
#[学号,考号,姓名,班级, [  [成绩1：考试时间,类型,缺考,总分,听力,阅读,写作],[成绩2：考试时间,类型,总分,听力,阅读,写作]  ] ]
#  0    1   2    3                                                 4

CET4 = "大学英语国家四级"
CET6 = "大学英语国家六级"

exam_season = [
    '20161217',
    '20160618',
    '20151219'
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

stulist = []
#载入数据集
print("\n\n加载数据...")
f = open('csCET46list.csv','r')
csvr = csv.reader(f)
for line in csvr:
    if len(line) > 1:
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
if todo("是否需要显示详细分析数据（带图表）？"):
    #首先需要数据分类
    #[学号,考号,姓名,班级, [  [成绩1：考试时间,类型,缺考,总分,听力,阅读,写作],[成绩2：考试时间,类型,总分,听力,阅读,写作]  ] ]
    #本次分类后得到的数据为每一年四六级的数据数组
    # 下面两个list的数据结构如下：
    # [  [考试年份1,[ 成绩列表:考试时间,类型,缺考,总分,听力,阅读,写作 ]]， [考试年份2,[ 成绩列表:学生信息 ]],[考试年份3,[ 成绩列表:学生信息 ]],......   ]
    CET4SCORE = []
    CET6SCORE = []
    #构造符合以上条件的结构体
    for season in exam_season:
        CET4SCORE.append( [ season , [ y for x in stulist for y in x[4] if y[0] == season and y[1] == CET4 ].copy() ] )
        CET6SCORE.append( [ season , [ y for x in stulist for y in x[4] if y[0] == season and y[1] == CET6 ].copy() ] )
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
            for v in zip(cet4x,cet4val,cet4label):    
                plt.plot(v[0],v[1],label=v[2])
                plt.title("计算机学院四级成绩变化趋势(2015级) - by Kanch",fontproperties=font_set)
                plt.xlabel("参考人数(一个数字为一个个体,姓名被隐藏)",fontproperties=font_set)
                plt.ylabel("四级得分",fontproperties=font_set)
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
            for v in zip(cet6x,cet6val,cet6label):
                plt.plot(v[0],v[1],label=v[2])
                plt.title("计算机学院六级成绩变化趋势(2015级) - by Kanch",fontproperties=font_set)
                plt.xlabel("参考人数(一个数字为一个个体,姓名被隐藏)",fontproperties=font_set)
                plt.ylabel("六级得分",fontproperties=font_set)
                plt.legend(loc='upper right')
            plt.show()
    if todo("是否显示四级级成绩单科贡献相关性？"):
        #分析4级中听力阅读写作对总成绩的贡献情况
        vscore = []         #这里按照年份存放了
        vreading = []       #每一次四级的成绩情况
        vlistening = []     #其结构为：
        vwriting = []       # [  [考试年份,[成绩列表]],.....]
        vlabel = ["Total Score","Listening","Reading","Writing"]
        #抽取总成绩，单科目成绩
        for cet4 in CET4SCORE:
            #[考试年份1,[ 成绩列表:考试时间,类型,缺考,总分,听力,阅读,写作 ]]
            vscore.append( [ cet4[0],[ int(x[3])-200 for x in cet4[1] ] ] ) #减去250是为了标准化数据，便于比较
            vlistening.append( [ cet4[0],[ x[4] for x in cet4[1] ] ] )
            vreading.append( [ cet4[0],[ x[5] for x in cet4[1] ] ] )
            vwriting.append( [ cet4[0],[ x[6] for x in cet4[1] ] ] )
        cet4x = []
        for v in vscore:
            cet4x.append( range(1,len(v[1])+1) )
        print("按照单科目对总分贡献度分类后，4级数据条数：",sum([len(x[1]) for x in vscore]))
        #绘图
        with plt.style.context('fivethirtyeight'):
            for v in zip(cet4x,vscore,vreading,vlistening,vwriting):
                plt.plot(v[0],v[1][1],label=vlabel[0])
                plt.plot(v[0],v[2][1],label=vlabel[1])
                plt.plot(v[0],v[3][1],label=vlabel[2])
                plt.plot(v[0],v[4][1],label=vlabel[3])
                plt.title("计算机学院四级单科对总成绩贡献度情况(2015级,考试时间:"+ v[1][0] +") - by Kanch",fontproperties=font_set)
                plt.xlabel("参考人数(一个数字为一个个体,姓名被隐藏)",fontproperties=font_set)
                plt.ylabel("该项得分",fontproperties=font_set)
                plt.legend(loc='lower left')
                plt.show()