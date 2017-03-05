import csv

##该脚本用于抽取应用学生的信息

applycsall = open('cs2015-2017-score-ngbk.csv', 'r')
allreader = csv.reader(applycsall)
allreaderlist = []
for line in allreader:
    print(line)
    allreaderlist.append(line)

applycsall.close()

del allreaderlist[0]

studentlist = ""
for student in allreaderlist:
    studentlist += student[1] + ","

f = open("slist_csa.txt","w")
f.write(studentlist)
f.close()

