import csv
import os

##该脚本用于抽取应用学生的信息

flist = os.listdir()

#print(flist)

studentlist = ""   #储存结果
processsum = 0
for file in flist:
    if file[file.find('.')+1:] == "csv" or file[file.find('.')+1:] == "CSV":
        applycsall = open(file, 'r',encoding="GB18030")
        allreader = csv.reader(applycsall)
        allreaderlist = []
        x = 0
        for line in allreader:
            #['20', '2014082021', '胡文昊  ', '男', '']
            if x >=2:
                #跳过前两行标题
                line[2] = line[2].encode('GB18030','ignore').decode('GB18030')
                processsum += 1
            try:
                print(processsum,line)
            except Exception as e:
                print(processsum,e)
            allreaderlist.append(line)
            x+=1
        applycsall.close()
        del allreaderlist[0]
        del allreaderlist[0]
        for student in allreaderlist:
            studentlist += student[2].replace(' ','') + ":" + file[:file.find('.')] + ":" + student[1] +","

f = open("slist_csa.txt","wb")
f.write(studentlist.encode('UTF-8','ignore'))
f.close()

print("\n----\n处理完毕，共",studentlist.count(','),"名学生。")

