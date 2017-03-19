
############################333
#       下面是单词数据查询接口
############################333
#获取一个单词的发帖量最高的前10位用户和单词的时间线
@app.route('/api/tiebabigdata/wordstatisc/<word>')
def api_statisword(word):
    if TermAnalyze.checkExist(word) == True:
        return "错误！数据已经存在！"
    usercount,timeline = TermAnalyze.statisANDTimeline(TermAnalyze.searchForInclude(word))
    tstr,ustr = TermAnalyze.slice(usercount,timeline)
    TermAnalyze.saveToDB(ustr,tstr,word)
    return ustr+"<hr/>"+tstr
############################333
#       下面是用户数据查询接口
############################333
#获取用户的累计发帖量和最近30天发帖数据
@app.route('/api/tiebabigdata/postsum/<int:xid>')
@app.route('/api/tiebabigdata/postsum/<session>/<int:xid>')
def api_postsum(xid,session=""):
    if session != "":
        if QueryAPI.checkSession(session) == False:
            return  "会话无效或已经过期！"
    count,count30 = QueryAPI.getTotalPostsSum(xid)
    return str(count) + "," + str(count30)

#获取活跃时间段图数据
@app.route('/api/tiebabigdata/activitytimezon/<int:xid>')
@app.route('/api/tiebabigdata/activitytimezon/<session>/<int:xid>')
def api_activitytimezone(xid,session=""):
    if session != "":
        if QueryAPI.checkSession(session) == False:
            return  "会话无效或已经过期！"
    listt =  QueryAPI.getActivityTimeZone(xid)
    return str(listt)


#获取最近活跃度图
@app.route('/api/tiebabigdata/activitytimeline/<int:xid>/<int:days>')
@app.route('/api/tiebabigdata/activitytimeline/<session>/<int:xid>/<int:days>')
def api_activitytimeline(xid,days,session=""):
    if session != "":
        if QueryAPI.checkSession(session) == False:
            return  "会话无效或已经过期！"
    listt =  QueryAPI.getActivityTimeLine(xid,days)
    return str(listt)

#获取用户关系图数据
@app.route('/api/tiebabigdata/relationcircle/<int:xid>')
@app.route('/api/tiebabigdata/relationcircle/<session>/<int:xid>')
@as_json
def api_relationcircle(xid,session=""):
    if session != "":
        if QueryAPI.checkSession(session) == False:
            return  "会话无效或已经过期！"
    listt =  QueryAPI.getReadlationCircle(xid)
    i=0
    iljson = []
    for v in listt[1]:
        iljson.append([dict(name=listt[0][i],values=v)])
        i+=1
    ditt = {}
    return dict(label=listt[0],value=iljson)

#获取常用关键字图
@app.route('/api/tiebabigdata/keymap/<int:xid>')
@app.route('/api/tiebabigdata/keymap/<session>/<int:xid>')
def api_keymap(xid,session=""):
    if session != "":
        if QueryAPI.checkSession(session) == False:
            return  "会话无效或已经过期！"
    listt =  QueryAPI.getKeymap(xid)
    return str(listt)

#获取用户标签
@app.route('/api/tiebabigdata/gettags/<int:xid>')
@app.route('/api/tiebabigdata/gettags/<session>/<int:xid>')
def api_gettags(xid,session=""):
    if session != "":
        if QueryAPI.checkSession(session) == False:
            return  "会话无效或已经过期！"
    return "这是一个测试页面，显示API的用法"

