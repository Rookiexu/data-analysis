import csv

def save(filename,datalist):
    ff = open(filename, 'w')
    writer = csv.writer(ff)
    writer.writerows(datalist)
    ff.close()


lllmates = open('lllmates.csv', 'r')
lllreader = csv.reader(lllmates)
applycsall = open('cs2015-2017-score-ngbk.csv', 'r')
allreader = csv.reader(applycsall)
lllmateslist = []
for line in lllreader:
    print(line)
    lllmateslist.append(line[0])

allreaderlist = []
for line in allreader:
    print(line)
    allreaderlist.append(line)
lllmates.close() 
applycsall.close()

#开始筛选李莉丽班级和清静班级学生
header = allreaderlist[0]
del allreaderlist[0]
lllscorelist = [header]
qingjinglist = [header]
for student in allreaderlist:
    if student[0] in lllmateslist:
        lllscorelist.append(student)
    else:
        qingjinglist.append(student)
save('lll-score.csv',lllscorelist)
save('qj-score.csv',qingjinglist)


#接下来筛选出所有选了web，3+1和李莉丽的人
web3p1llllist = [header]
for student in allreaderlist:
    if student[6] and student[7] and student[0] in lllmateslist:
        web3p1llllist.append(student)

for s in web3p1llllist:
    print(s)
save('web3p1lll-score.csv',web3p1llllist)


#接下来求出对于每个人来说，平均分贡献最大的科目和贡献最小的科目
#以及选修对绩点的提升还是下降
#公式：((A-50)*0.1*a+(B-50)*0.1*b+(C-50)*0.1*c+(D-50)*0.1*d+(E-50)*0.1*e+(F-50)*0.1*f+(G-50)*0.1*g+(H-50)*0.1*h)/(a+b+c+d+e+f+g+h)
mheader = ["学号","姓名","总绩点","绩点（不算选修）","选修影响","总平均分","得分最高科目","得分最低科目"]
xplisy = [mheader]
csl = [3,4,1.5,4,3,4,1,0.5] #学分列表，顺序：大学英语3,电子技术基础,工程实践2,离散数学,面向对象程序设计(C++),数据结构,体育3,形势与政策2
         #索引：            8          9          10      11        12                  13    14     15
majors = ["大学英语3:","电子技术基础:","工程实践2:","离散数学:","面向对象程序设计(C++):","数据结构:","体育3:","形势与政策2:"]
for student in allreaderlist:
    nonaltscore = student[8:16]
    nopass = True
    for x in nonaltscore:
        x = x.replace(" ","")
        if not x:
            nopass = False
            break
    if nopass:
        nonaltscore = [int(x) for x in nonaltscore]
        maxs = max(nonaltscore)
        maxspos = nonaltscore.index(maxs)
        mins = min(nonaltscore)
        minpos = nonaltscore.index(mins)
        #求非选修绩点
        sumx = 0.0
        gpa = round(sum( [(x[0]-50)*0.1*x[1] for x in zip(nonaltscore,csl)])/21,2)
        symbol = "="
        if float(student[4]) < gpa:
            symbol = "+"
        elif float(student[4]) > gpa:
            symbol = "-"
        xplisy.append([student[0],student[1],student[4],gpa,symbol,student[5],majors[maxspos] + str(maxs),majors[minpos]+str(mins)])

print(xplisy)
save("noALTclassGPAAnalyze.csv",xplisy)