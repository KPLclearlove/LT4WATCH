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
                    ['Feeling Summary', 'Bought Date', 'Bought City', 'Ownership Period', 'Created', 'Best', 'Worst'])

            # 遍历评论数据，提取需要的信息并写入
            for review in reviews:
                feeling_summary = review.get('feeling_summary', '')
                bought_date_str = review.get('bought_date', '')
                bought_city = review.get('boughtCityName', '')
                ownership_period = review.get('carOwnershipPeriod', '')
                created_str = review.get('created', '')

                # 转换日期格式
                bought_date_formatted = self.format_date(bought_date_str, '%Y年%m月')
                created_formatted = self.format_date(created_str, '%Y-%m-%d %H:%M:%S')

                best = review.get('best', '')
                worst = review.get('worst', '')

                # 移除 "【最满意】" 和 "【最不满意】" 的前缀
                best = review.get('best', '').replace("【最满意】", "").strip()
                worst = review.get('worst', '').replace("【最不满意】", "").strip()

                # 写入一行数据
                writer.writerow([feeling_summary, bought_date_formatted, bought_city, ownership_period,
                                 created_formatted, best, worst])

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