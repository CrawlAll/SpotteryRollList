Crawler For Traditional Sporttery


# 项目说明
### 一.SpotteryRollList
- 由下面这个链接进入第一层，链接如下
- http://info.sporttery.cn/roll/fb_list.php?page=1&c=%D7%E3%B2%CA%CA%A4%B8%BA
- 根据符合'冷门'关键字的进入第二层
- 子链接e.g.http://www.sporttery.cn/ctzc/zcsf/2017/1227/270648.html
- 详细会在SpotteryRollList/README.md中进一步说明

### 备注
    在第一层中是根据 '冷门' 这个字符串进行判断是否跟进第二层
    但是 在所跟进的第二层中并没有想要的表格数据
    所以在会出现 error：列表的下标越界，但不影响运行