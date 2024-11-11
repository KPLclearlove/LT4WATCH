import csv
import os
from datetime import datetime
import requests
from tqdm import tqdm

class CarReviewScraper:
    def __init__(self, series_brand):
        """
        初始化类，传入品牌系列代码
        :param series_brand: Series 类实例化对象，用于获取车型信息
        """
        self.series_brand = series_brand
        self.koubei_url = 'https://k.m.autohome.com.cn/ajax/serieskoubei/getserieskoubeilistbytag'
        self.car_name_url = 'https://k.m.autohome.com.cn/ajax/serieskoubei/gettypetags'

    def get_car_name_and_type(self, series_id):
        """
        根据系列 ID 获取车名和是否为电动车
        :param series_id: 车型的 seriesId
        :return: car_name (车名), is_electric (是否为电动车)
        """
        car_name_param = {
            'seriesId': f'{series_id}',
            'specId': '0',
            'year': '0'
        }
        try:
            response = requests.get(url=self.car_name_url, params=car_name_param).json()
            car_name = response['result']['seriesName']
            is_electric = response['result']['isElectric']
            return car_name, is_electric
        except:
            print(f'此车尚未上市或请求失败：Series ID {series_id}')
            return None, None

    def get_reviews(self, series_id, page_num):
        """
        获取指定车系的评论数据
        :param series_id: 车型的 seriesId
        :param page_num: 请求的页码
        :return: 评论数据列表，若无数据则返回 False
        """
        koubei_param = {
            'seriesId': f'{series_id}',
            'specId': '0',
            'gradeEnum': '0',
            'pageIndex': f'{page_num}',
            'pageSize': '20',
            'year': '0',
            'order': '0',
            'v': '20240410'
        }

        # 发送请求
        resp = requests.get(url=self.koubei_url, params=koubei_param)
        if resp.status_code == 200:
            data = resp.json()
            try:
                reviews = data['result']['list']
                return reviews
            except KeyError:
                return False
        else:
            print(f"请求失败，状态码：{resp.status_code}")
            return False

    def save_reviews_to_csv(self, reviews, csv_filename):
        """
        将获取的评论数据保存到 CSV 文件中
        :param reviews: 评论数据列表
        :param csv_filename: CSV 文件名
        """
        file_exists = os.path.isfile(csv_filename)
        with open(csv_filename, 'a', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)

            # 如果文件不存在，写入表头
            if not file_exists:
                writer.writerow(
                    ['Feeling Summary', 'Bought Date', 'Bought City', 'Ownership Period', 'Created', 'Best', 'Worst',
                     'Helpful Count', 'Visit Count', 'Purposes', 'Actual Battery Consumption', 'Actual Oil Consumption',
                     'Apperance Score', 'Consumption Score', 'Cost Efficiency Score', 'Interior Score', 'Power Score',
                     'Space Score', 'Driven Kilometers', 'Price', 'Specification Name'])
                '''
                writer.writerow(
                    ['Purposes'])
                '''
            # 遍历评论数据，提取需要的信息并写入
            for review in reviews:
                """
                主要为主观感受数据
                """
                feeling_summary = review.get('feeling_summary', '')  # 评论标题
                bought_date_str = review.get('bought_date', '')  # 购买日期
                bought_city = review.get('boughtCityName', '')  # 购买城市
                ownership_period = review.get('carOwnershipPeriod', '')  # 用车时间
                created_str = review.get('created', '')  # 发帖日期

                # 转换日期格式
                bought_date_formatted = self.format_date(bought_date_str, '%Y年%m月')
                created_formatted = self.format_date(created_str, '%Y-%m-%d %H:%M:%S')

                best = review.get('best', '').replace("【最满意】", "").strip()  # 最满意
                worst = review.get('worst', '').replace("【最不满意】", "").strip()  # 最不满意

                helpful_count = review.get('helpfulCount', '')  # 点赞数
                visit_count = review.get('visitCount', '')  # 浏览次数
                purpose_list = []
                purposes = review.get('purposes', [])  # 获取目的列表
                for purpose in purposes:
                    purpose_name = purpose.get('name', '')
                    if purpose_name:
                        purpose_list.append(purpose_name)  # 将目的名称添加到 purpose_list 中
                purposes_str = ', '.join(purpose_list)  # 目的列表转换为字符串

                '''
                汽车本身的数据
                '''
                actual_battery_consumption = review.get('actual_battery_consumption', '')  # 电耗
                actual_oil_consumption = review.get('actual_oil_consumption', '')  # 油耗

                apperance = review.get('apperance', '')  # 外观得分
                consumption = review.get('consumption', '')  # 耗能得分
                cost_efficient = review.get('cost_efficient', '')  # 性价比得分
                interior = review.get('interior', '')  # 内饰得分
                power = review.get('power', '')  # 动力得分
                space = review.get('space', '')  # 空间得分

                driven_kilometers = review.get('driven_kilometers', '')  # 行驶里程
                price = review.get('price', '')  # 价格（官方指导价，一般都比这个低）
                spec_name = review.get('specName', '')  # 车型配置

                # 写入一行数据
                writer.writerow([feeling_summary, bought_date_formatted, bought_city, ownership_period,
                                 created_formatted, best, worst, helpful_count, visit_count, purposes_str,
                                 actual_battery_consumption, actual_oil_consumption, apperance, consumption,
                                 cost_efficient, interior, power, space, driven_kilometers, price, spec_name])
                '''
                if purposes_str != '':
                    writer.writerow([purposes_str])
                '''

    def format_date(self, date_str, format_str):
        """
        将日期字符串转化为指定格式，转换失败时返回原日期字符串
        :param date_str: 原始日期字符串
        :param format_str: 目标日期格式
        :return: 格式化后的日期字符串
        """
        try:
            date_obj = datetime.strptime(date_str, format_str).date()
            return date_obj.strftime('%Y.%m.%d')
        except ValueError:
            return date_str

    def scrape_reviews(self, series_id_list=None):
        if series_id_list is None:
            series_id_list = self.series_brand.series_code_get('seriesid')

        # 添加 tqdm 进度条，用于显示总车型抓取进度
        for series_id in tqdm(series_id_list, desc="抓取车型评论进度"):
            car_name, is_electric = self.get_car_name_and_type(series_id)

            if car_name is None:
                continue  # 跳过未上市的车型

            csv_filename = f'[{("新能源" if is_electric else "燃油车")}] {car_name}.csv'

            if os.path.isfile(csv_filename):
                print(f'{car_name}[{series_id}]已存在，跳过')
                continue

            print(f'正在抓取 {car_name} 的评论...')
            page_num = 1

            # 使用 tqdm 作为分页抓取的进度条显示
            while True:
                reviews = self.get_reviews(series_id, page_num)
                if not reviews:
                    print(f'{car_name}[{series_id}]已完成')
                    break

                self.save_reviews_to_csv(reviews, csv_filename)

                # 每页处理完后显示当前页数的进度
                tqdm.write(f"第{page_num}页已完成")
                page_num += 1

