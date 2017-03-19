import BigDataQueryAPI as QueryAPI
import termanalyze as TermAnalyze

#该脚本用于从目录下的postdata.csv读取数据并用于分析
#分析用户的活跃时间段，活跃度，关键字，关系链等
result = []
print('open postdata.csv')
f = open("postdata.csv","r",encoding='utf-8',errors='ignore')
wr = csv.reader(f)
print('reading data...')
for line in wr:
    pass
f.close()
print('done.\ndata retrived:',len(result))
print('start analyzing.')
#开始循环分析