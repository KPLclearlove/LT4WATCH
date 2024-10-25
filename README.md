# 结构：
## car_review_scraper:
### 功能:
1. 获得汽车特定型号的用户口碑数据
2. 保存成特定格式的csv文件
3. 更改数据格式
***此为json未添加的数据（手动添加）
```
客制化数据
在save_reviews_to_csv方法中添加
此为用户口碑数据官方提供的json文件中未添加在代码中的数据
示例：
1. actual_battery_consumption: 0#电耗
2. actual_oil_consumption: 8.1#油耗
3. apperance: 4#外观得分
4. consumption: 5#油耗得分
5. cost_efficient: 3#性价比得分
6. interior: 4#内饰得分
7. power: 5#驾驶感受得分
8. space: 5#空间评分
9. driven_kilometers: 8800#行驶里程km
10. price: 39.55#购车价格
11. headImage: "//i2.autoimg.cn/userscenter/g30/M03/CC/15/120X120_0_q87_autohomecar__ChxknGT-ziGAPn5rAACSzldIZjE177.png"#用户头像
12. helpfulCount: 32#点赞数
13. last_edit: "2024-03-31 14:30:17"#最后一次编辑时间
14. purposes:
		0: {id: 1, name: "上下班"}
		1: {id: 6, name: "商务差旅"}
		2: {id: 7, name: "越野"}
		3: {id: 8, name: "约会"}
		#买车用途
15. visitCount: 41378#浏览量
16. specName: "2024款 B5 四驱智远豪华版"#车型配置
```

>添加方式:
**添加表头 
if not file_exists:  
    writer.writerow(  
        ['Feeling Summary', 'Bought Date', 'Bought City', 'Ownership Period', 'Created', 'Best', 'Worst'])
添加数据
for review in reviews:  
    feeling_summary = review.get('feeling_summary', '')  
    bought_date_str = review.get('bought_date', '')  
    bought_city = review.get('boughtCityName', '')  
    ownership_period = review.get('carOwnershipPeriod', '')  
    created_str = review.get('created', '')
写入数据
writer.writerow([feeling_summary, bought_date_formatted, bought_city, ownership_period, created_formatted, best, worst])

## series_code:
### 功能：
	获得汽车品牌下各个型号的id
	即branid下的serieslist
	可以返回serieslist中的全部数据或者具体某一条数据
	本质是另一个request

## car_review_gui:
>图形化界面
其实没什么用
多了个能在里面挑选品牌车型和输出文件夹位置


## main：
>详情见运行后内容
品牌的brandid请参考
https://www.autohome.com.cn/price/brandid_1 \
比如这个链接中大众的id就是1
而车型的seriesid
https://www.autohome.com.cn/496/#pvareaid=6861421
这其中迈腾的id就是496
其他车型也是如此\
几个存在的问题：\
①网站并没有对汽车能源形式严格分类
只对驱动形式进行了分类\
即便是能上绿牌的混动车也返回的是燃油车
而增程车返回的竟然都是电车
所以我只对驱动形式上进行了分类输出\
②部分汽车品牌由于其拥有多个生产厂商
获取数据时并不会将他们分开

## 开发中
①二手车数据\
②口碑评论详细页数据（具体方面的评论（如油耗评论，车主实拍照片 ，口碑tag\
③车型口碑总体评分数据\
更新请见
https://github.com/KPLclearlove/LT4WATCH