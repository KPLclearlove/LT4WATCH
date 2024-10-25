import csv
import os
from datetime import datetime

import requests

from series_code import Series

# 设置请求的 URL 和参数
koubeiUrl = 'https://k.m.autohome.com.cn/ajax/serieskoubei/getserieskoubeilistbytag'
carNameUrl = 'https://k.m.autohome.com.cn/ajax/serieskoubei/gettypetags'
seriesBrand = Series(279)
seriesIDList = seriesBrand.series_code_get('seriesid')
# 当需要获得一个品牌的多种车型的数据的时候使用，Series内填写品牌代码，seriesid返回的是该品牌所有车型的代码
for seriesID in seriesIDList:
    carNameParam = {
        'seriesId': f'{seriesID}',
        'specId': '0',
        'year': '0'
    }
    try:
        carName = requests.get(url=carNameUrl, params=carNameParam).json()['result']['seriesName']
        isElectric = requests.get(url=carNameUrl, params=carNameParam).json()['result']['isElectric']
    except:
        print(f'此车尚未上市')
    pageNum = 1
    flagPage = True

    if isElectric == True:
        csv_filename = f'[新能源]{carName}.csv'
    else:
        csv_filename = f'[燃油车]{carName}.csv'
    # 检查文件是否存在，决定写入模式
    file_exists = os.path.isfile(csv_filename)

    if file_exists:
        print(f'{carName}[{seriesID}]已存在，跳过')
    if not file_exists:
        while flagPage:
            koubeiParam = {
                'seriesId': f'{seriesID}',
                'specId': '0',
                'gradeEnum': '0',
                'pageIndex': f'{pageNum}',
                'pageSize': '20',
                'year': '0',
                'order': '0',
                'v': '20240410'
            }

            # 发送请求
            resp = requests.get(url=koubeiUrl, params=koubeiParam)

            # 检查响应状态
            if resp.status_code == 200:
                # 解析 JSON 数据
                data = resp.json()

                # 获取评论列表
                try:
                    reviews = data['result']['list']
                except:
                    reviews = False

                # 打开 CSV 文件以写入或追加
                with open(csv_filename, 'a', newline='', encoding='utf-8-sig') as csvfile:
                    writer = csv.writer(csvfile)
                    print(file_exists)
                    # 检查文件是否存在，决定写入模式
                    if pageNum >= 2:
                        file_exists = os.path.isfile(csv_filename)
                    # 如果文件不存在，写入表头
                    if not file_exists:
                        writer.writerow(
                            ['Feeling Summary', 'Bought Date', 'Bought City', 'Ownership Period', 'Created', 'Best',
                             'Worst'])

                    # 遍历评论数据，提取需要的信息
                    if reviews:
                        for review in reviews:
                            feeling_summary = review.get('feeling_summary', '')  # ①

                            # 处理日期格式
                            bought_date_str = review.get('bought_date', '')  # ②
                            bought_city = review.get('boughtCityName', )  # ③
                            ownership_period = review.get('carOwnershipPeriod', )  # ④
                            created_str = review.get('created', '')  # ⑤

                            # 日期格式转换
                            try:
                                # 转换 bought_date
                                bought_date = datetime.strptime(bought_date_str, '%Y年%m月').date()
                                bought_date_formatted = bought_date.strftime('%Y.%m.%d')
                            except ValueError:
                                bought_date_formatted = bought_date_str  # 如果转换失败，保持原格式

                            try:
                                # 转换 created
                                created = datetime.strptime(created_str, '%Y-%m-%d %H:%M:%S').date()
                                created_formatted = created.strftime('%Y.%m.%d')
                            except ValueError:
                                created_formatted = created_str  # 如果转换失败，保持原格式

                            best = review.get('best', '')  # ⑥
                            worst = review.get('worst', '')  # ⑦

                            # 写入一行数据
                            writer.writerow(
                                [feeling_summary, bought_date_formatted, bought_city, ownership_period, created_formatted,
                                 best, worst])
            else:
                print(f"请求失败，状态码：{resp.status_code}")
            print(f"第{pageNum}页")
            pageNum = pageNum + 1
            if not reviews:
                print(f'{carName}[{seriesID}]已完成')
                flagPage = False
            resp.close()
