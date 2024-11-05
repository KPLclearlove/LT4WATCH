import requests
import csv
import os

class Seconds:
    def __init__(self, brandID):
        self.brandID = brandID

    def seconds_list_get(self, page_num):
        url = 'https://api2scsou.che168.com/api/v11/search'
        params = {
            'pageindex': f'{page_num}',
            'pagesize': 10,
            'brandid': self.brandID,
            'ishideback': 1,
            'personalizedpush': 1,
            'cid': 110100,
            'pid': 110000,
            'lat': 40.04353058733718,
            'iscxcshowed': -1,
            'scene_no': 12,
            'pageid': 1730423614_8631,
            'ssnew': 1,
            'userid': 0,
            's_pid': 110000,
            's_cid': 110100,
            '_appid': '2sc.m',
            'v': '11.41.5',
        }
        request = requests.get(url=url, params=params)
        data = request.json()
        carlist = data['result']['carlist']
        if not carlist:
            return False
        else:
            infoid_list = [list['infoid'] for list in carlist]
            return infoid_list

    def reviews_get_save(self, infoid_list):
        """
        获取车辆信息并保存到 CSV 文件中
        :param infoid_list: 车辆信息ID列表
        :param csv_filename: CSV 文件名
        """
        url = 'https://apiuscdt.che168.com/apic/v2/car/getcarinfo'
        car_data_list = []

        for infoid in infoid_list:
            params = {
                'infoid': f'{infoid}',
                'ucuserauth': '',
                'gpscid': '110100',
                'iscardetailab': 'B',
                'encryptinfo': '',
                'fromtag': '0',
                'pvareaid': '0',
                'userid': '0',
                's_pid': '110000',
                's_cid': '110100',
                '_appid': '2sc.m',
                'v': '11.41.5',
            }
            request = requests.get(url=url, params=params)
            data = request.json()

            # 提取车辆信息
            car_info = {
                'infoid': data['result']['infoid'],
                'carname': data['result']['carname'],
                'brandid': data['result']['brandid'],
                'brandname': data['result']['brandname'],
                'seriesid': data['result']['seriesid'],
                'seriesname': data['result']['seriesname'],
                'specid': data['result']['specid'],
                'cid': data['result']['cid'],
                'cname': data['result']['cname'],
                'pid': data['result']['pid'],
                'displacement': data['result']['displacement'],
                'gearbox': data['result']['gearbox'],
                'mileage': data['result']['mileage'],
                'price': data['result']['price'],
                'remark': data['result']['remark'],
                'vincode': data['result']['vincode'],
                'userid': data['result']['userid'],
                'dealerid': data['result']['dealerid'],
                'transfercount': data['result']['transfercount'],
                'firstregshortdate': data['result']['firstregshortdate'],
                'firstregdate': data['result']['firstregdate'],
                'firstregyear': data['result']['firstregyear'],
                'firstregstr': data['result']['firstregstr'],
                'environmental': data['result']['environmental'],
                'isloan': data['result']['isloan'],
                'downpayment': data['result']['downpayment'],
                'haswarranty': data['result']['haswarranty'],
                'isbrandcar': data['result']['isbrandcar'],
                'iscontainfe': data['result']['iscontainfe'],
                'isnewcar': data['result']['isnewcar'],
                'islatestcar': data['result']['islatestcar'],
                'videourl': data['result']['videourl'],
                'fromtype': data['result']['fromtype'],
                'publicdate': data['result']['publicdate'],
                'countyname': data['result']['countyname'],
                'imageurl': data['result']['imageurl'],
                'followcount': data['result']['followcount'],
                'examine': data['result']['examine'],
                'insurance': data['result']['insurance'],
                'colorname': data['result']['colorname'],
                'carusename': data['result']['carusename'],
                'isev': data['result']['isev'],
                'fuelname': data['result']['fuelname'],
                'batterypower': data['result']['batterypower'],
                'lifemileage': data['result']['lifemileage'],
                'quickcharge': data['result']['quickcharge'],
                'slowcharge': data['result']['slowcharge'],
                'guidanceprice': data['result']['guidanceprice'],
                'drivingmode': data['result']['drivingmode'],
                'levelname': data['result']['levelname'],
                'flowmode': data['result']['flowmode'],
                'setcount': data['result']['setcount'],
                'isttpcity': data['result']['isttpcity'],
                'isybyq': data['result']['isybyq'],
                'is4sby': data['result']['is4sby'],
                'isjpck': data['result']['isjpck'],
                'accelerate': data['result']['accelerate'],
            }
            car_data_list.append(car_info)


        # 写入数据到CSV文件
        csv_filename = data['result']['brandname']
        file_exists = os.path.isfile(f'{csv_filename}.csv')
        with open(f'{csv_filename}.csv', 'a', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=car_data_list[0].keys())

            # 如果文件不存在，写入表头
            if not file_exists:
                writer.writeheader()

            writer.writerows(car_data_list)  # 写入所有车辆信息

    def fetch_and_save_reviews(self ):
        page_num = 74
        all_infoid_list = []

        print("开始抓取车辆信息...")
        while True:
            infoid_list = self.seconds_list_get(page_num)
            if not infoid_list:
                print("没有更多数据，退出抓取。")
                break
            all_infoid_list.extend(infoid_list)  # 将获取的 infoid 添加到列表中
            self.reviews_get_save(all_infoid_list)
            print(f"第{page_num}页数据抓取完成，信息ID: {infoid_list}")
            page_num += 1

a = Seconds(15)
a.fetch_and_save_reviews()


