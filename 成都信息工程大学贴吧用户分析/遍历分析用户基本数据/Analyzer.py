
#[帖子ID    储存贴吧名   回帖作者  回帖内容    回帖日期    回帖目标]
#   0          1           2        3           4         5

#用于分析本地数据的python脚本
#获取某一用户的发帖总数，由于采用了分段处理，故，这里每次返回给定dataset中的数量
def getUserPostSum(username,dataset):
    return len([x for x in dataset if x[2]==username])

def getActiveTimeZone(username,dataset):
    feqlist = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #time format:2017-03-05 10:36:00
    


def getReadlationCircle(username,dataset):
    pass

def getKeymap(username,dataset):
    pass

def getActivityTimeLine(username,days,dataset):
    pass