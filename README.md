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
>获得汽车品牌下各个型号的id
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

一、数据处理与准备
数据清洗与预处理

论坛帖子：
去除无用信息：清洗广告、无效回复和与主题无关的内容。
结构化处理：提取问题、回答、用户关注点（如车型、问题类别）并标注上下文关系。
消除冗余：合并重复问题及类似答案，避免信息噪音。
维修手册：
转化为易检索格式：将手册的结构（章节、索引、图表）分解成问答形式。
提取关键内容：针对DIY用户，提取简单易操作的部分，比如常见故障诊断、维护流程。
构建知识库

使用向量数据库（如 FAISS 或 Milvus）存储处理后的文本数据。
将论坛内容和手册内容嵌入到同一向量空间中，方便检索。
对于维修手册数据，可添加标签（如【原厂】或【技术文档】）来区分数据来源。
数据标注

人工标注：为论坛问题和维修手册数据生成 Q&A 对，标注出问题类别（如保养、改装、常见故障等）。
语义关联：建立问题与解决方案的语义关联，确保模型能够正确检索答案。
知识更新

定期更新：定期爬取和清洗论坛新内容，确保知识库的时效性。
版本管理：对维修手册进行版本控制，以区分旧款车型与新款车型的数据。
二、扩充数据来源
增加其他数据来源

用户手册：每款车型的用户手册是基础，可以提供保养和基本操作的信息。
行业标准：如国家或地区关于汽车维修保养的规范（例如机油更换周期）。
视频内容：提取 DIY 修车教程的字幕或关键步骤描述，用于补充知识库。
其他论坛和社交平台：如 Reddit、Quora 或本地汽车论坛的相关讨论内容。
配件电商数据：加入改装配件的技术规格和兼容性信息。
用户反馈数据

收集用户提问和回答，形成一个动态学习系统。
引入评分机制，根据用户反馈优化知识库内容。
三、如何确保数据的精准性和真实性
数据分级与溯源

按可信度为数据分级：
1级：官方维修手册和用户手册。
2级：高质量论坛内容或经验帖。
3级：其他用户生成内容（如个人意见）。
回答时提供来源标注，用户可选择是否信任数据来源。
质量校验

结合专业知识校验：通过行业专家或资深技师对知识库中的数据定期审查。
自动化校验：用维修手册或行业规范校对论坛数据中的维修保养步骤。
模型验证

设置测试数据集：使用真实的用户提问和高质量答案来验证模型的表现。
监控生成内容：通过反馈环路，分析用户对模型回答的满意度，筛除错误数据。
动态更新和纠错机制

建立纠错反馈系统：用户可以标记错误答案或提交问题。
定期 retrain 模型：结合新数据重新训练模型，使其适应最新内容。
四、系统实现和增强
实现 RAG

使用分片机制：对论坛、手册、标准进行分片存储，分开检索后融合答案。
引入检索排序模型：利用语义匹配和相关性评分，优先提供最相关的内容。
个性化推荐

根据用户车型和改装需求，提供定制化答案。
使用用户历史查询数据，为其推荐相关内容。
互动性与解释性

提供“逐步解答”：针对复杂维修问题，逐步列出诊断和操作步骤。
答案可视化：生成操作图示或引用维修手册的图解。
兼容性验证

确保改装相关回答考虑到车型兼容性，提供明确的适配说明。
五、未来扩展与优化
多语言支持：如果目标用户群体广泛，可考虑扩展到其他语言市场。
集成语音助手：允许用户通过语音与模型互动，适合动手时无法打字的场景。
实时更新社区趋势：通过大数据分析，挖掘论坛中热度最高的主题并优先优化相关知识。