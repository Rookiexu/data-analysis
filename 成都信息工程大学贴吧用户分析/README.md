## 成都信息工程大学贴吧数据分析

这里的代码从 repo`ankanch/cuit-trs/tiebabigdata-user-analyze` 迁移而来。

这里的分析来至于对成都信息工程大学贴吧100万条回帖数据（不包括楼中楼）的分析。

抓取数据的爬虫请见这里: `ankanch/tieba-crawler` (目前为私有repo)

## 现有分析情况

[最后更新：2017-3-9]

目前这里拥有用户活跃时间段分析以及根据用户活跃时间段来实现k-means聚类。

稍后这里会加入基于用户回帖数据的VSM分析。
---
##文件说明

###**【TimeZoneAnalyzsis.py】**

用户活跃时间段分析

###**【TimeZoneClassify】**

根据用户的活跃时间段进行k-means聚类（k=3）。

###**【keyword4eachuseroftieba.py】**

用户关键词分析

###**【QueryFunctions.py】**
 >trs/Web/datasourceconfig/

基本的数据库操作函数

###**【locations.txt，schools.txt】**
 >trs/Web/templates/

这里存放了基本的地理位置信息和学院信息，方便用户分类

---

__该文件更新缓慢__

---
【k-means用户活跃时间段聚类分析结果】

#####聚类前的全体数据

![聚类前的全体数据](https://github.com/ankanch/data-analysis/raw/master/%E6%88%90%E9%83%BD%E4%BF%A1%E6%81%AF%E5%B7%A5%E7%A8%8B%E5%A4%A7%E5%AD%A6%E8%B4%B4%E5%90%A7%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/Data/result/all.png)

#####去除极端值（>400）

![去除极端值（>400）](https://github.com/ankanch/data-analysis/raw/master/%E6%88%90%E9%83%BD%E4%BF%A1%E6%81%AF%E5%B7%A5%E7%A8%8B%E5%A4%A7%E5%AD%A6%E8%B4%B4%E5%90%A7%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/Data/result/less400-9.png)

#####3个簇的平均活跃时间段

![3个簇的平均活跃时间段](https://github.com/ankanch/data-analysis/raw/master/%E6%88%90%E9%83%BD%E4%BF%A1%E6%81%AF%E5%B7%A5%E7%A8%8B%E5%A4%A7%E5%AD%A6%E8%B4%B4%E5%90%A7%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/Data/result/2cr1.png)

#####簇1

![簇1](https://github.com/ankanch/data-analysis/raw/master/%E6%88%90%E9%83%BD%E4%BF%A1%E6%81%AF%E5%B7%A5%E7%A8%8B%E5%A4%A7%E5%AD%A6%E8%B4%B4%E5%90%A7%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/Data/result/2cr1.png)

#####簇2

![簇2](https://github.com/ankanch/data-analysis/raw/master/%E6%88%90%E9%83%BD%E4%BF%A1%E6%81%AF%E5%B7%A5%E7%A8%8B%E5%A4%A7%E5%AD%A6%E8%B4%B4%E5%90%A7%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/Data/result/2c2.png)


#####簇3

![簇3](https://github.com/ankanch/data-analysis/raw/master/%E6%88%90%E9%83%BD%E4%BF%A1%E6%81%AF%E5%B7%A5%E7%A8%8B%E5%A4%A7%E5%AD%A6%E8%B4%B4%E5%90%A7%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/Data/result/2c3.png)
