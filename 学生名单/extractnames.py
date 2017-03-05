import csv
import os

##该脚本用于抽取应用学生的信息

flist = os.listdir()

print(flist)

studentlist = ""   #储存结果
for file in flist:
    if file[file.find('.')+1:] == "csv" or file[file.find('.')+1:] == "CSV":
        applycsall = open(file, 'r')
        allreader = csv.reader(applycsall)
        allreaderlist = []
        for line in allreader:
            print(line)
            allreaderlist.append(line)
        applycsall.close()
        del allreaderlist[0]
        del allreaderlist[0]
        for student in allreaderlist:
            studentlist += student[2].replace(' ','') + ","

f = open("slist_csa.txt","w")
f.write(studentlist)
f.close()

