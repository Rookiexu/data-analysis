## 说明

这里的代码实现了从学校教务处查询计算机学院所有学生（2015级）从入学到现在参加的4，6级考试的成绩，并用于分析。

您可以在这里阅读从数据的获取到储存到分析。

http://akakanch.com/archives/661


## 文件说明

`result.csv`：查询结果记录集

`slist_csa.txt`：2015级全体学生名单（应用+工程+树莓）

`cet-result.xlsx`：用于数据分析的电子表格

`analyze.py`：用户分析四六级成绩的脚本文件

`generateTable.py`：用于统一学生信息的脚本

`getcet.py`：用于查询成绩的脚本

`csCET46list.csv`：计算机学院学生四六级情况

## 分析结果概要

计算机学院2015级四级和六级几次考试的成绩变化图，简直，一年比一年低，缺考越来越多。。。。。

目测越到后面，过的人越来越少了。

![2015级3次四级成绩变化图](https://github.com/ankanch/data-analysis/raw/master/CUIT-%E8%AE%A1%E7%AE%97%E6%9C%BACET4%EF%BC%8C6%E6%88%90%E7%BB%A9%E6%9F%A5%E8%AF%A2-%E5%88%86%E6%9E%90/%E5%88%86%E6%9E%90%E7%BB%93%E6%9E%9C/2015%E7%BA%A73%E6%AC%A1%E5%9B%9B%E7%BA%A7%E6%88%90%E7%BB%A9%E5%8F%98%E5%8C%96%E5%9B%BE.png)

![2015级3次六级成绩变化图](https://github.com/ankanch/data-analysis/raw/master/CUIT-%E8%AE%A1%E7%AE%97%E6%9C%BACET4%EF%BC%8C6%E6%88%90%E7%BB%A9%E6%9F%A5%E8%AF%A2-%E5%88%86%E6%9E%90/%E5%88%86%E6%9E%90%E7%BB%93%E6%9E%9C/2015%E7%BA%A73%E6%AC%A1%E5%85%AD%E7%BA%A7%E6%88%90%E7%BB%A9%E5%8F%98%E5%8C%96%E5%9B%BE.png)

![通过率变化图](https://github.com/ankanch/data-analysis/raw/master/CUIT-%E8%AE%A1%E7%AE%97%E6%9C%BACET4%EF%BC%8C6%E6%88%90%E7%BB%A9%E6%9F%A5%E8%AF%A2-%E5%88%86%E6%9E%90/%E5%88%86%E6%9E%90%E7%BB%93%E6%9E%9C/figure_1-3.png)

![最高分，最低分变化图](https://github.com/ankanch/data-analysis/raw/master/CUIT-%E8%AE%A1%E7%AE%97%E6%9C%BACET4%EF%BC%8C6%E6%88%90%E7%BB%A9%E6%9F%A5%E8%AF%A2-%E5%88%86%E6%9E%90/%E5%88%86%E6%9E%90%E7%BB%93%E6%9E%9C/figure_1-6.png)




### 版本

v1.0 @ 2017-3-12