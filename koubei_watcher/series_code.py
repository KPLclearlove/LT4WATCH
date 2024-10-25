import requests


class Series:
    def __init__(self, brandID):
        self.brandID = brandID

    def series_code_get(self, whatYouNeed=None):
        seriesUrl = 'https://car.m.autohome.com.cn/ajax/GetSeriesByBrandId1'
        seriesParams = {
            'r': '16',
            'brandid': f'{self.brandID}'
        }
        seriesNum = requests.get(url=seriesUrl, params=seriesParams)
        data = seriesNum.json()

        # 获取品牌名称
        # 处理多个fctlist，可能有多个品牌信息
        fctlists = data['seriesdata']['fctlist']

        # 创建空列表以存储结果
        series_names = []
        series_ids = []
        level_name_strs = []
        level_names = []
        whatYouNeedList = []

        # 遍历fctlist中的所有数据
        for fct in fctlists:
            brandName = fct['fctname']  # 打印品牌名称
            print(f"品牌名称: {brandName}")

            # 获取系列列表
            faction = fct['serieslist']

            if not whatYouNeed:
                # 填充列表
                for factions in faction:
                    series_names.append(factions.get('seriesName'))  # 获取系列名称
                    series_ids.append(factions.get('seriesid'))  # 获取系列 ID
                    level_name_strs.append(factions.get('levelNameStr'))  # 获取等级名称字符串
                    level_names.append(factions.get('levelName'))  # 获取等级名称

            if whatYouNeed:
                for factions in faction:
                    whatYouNeedList.append(factions.get(f'{whatYouNeed}'))

        # 如果没有指定whatYouNeed，返回所有四个列表
        if not whatYouNeed:
            return series_names, series_ids, level_name_strs, level_names

        # 如果指定了whatYouNeed，返回特定的数据列表
        return whatYouNeedList


if __name__ == '__main__':
    seriesBrand = Series(70)
    seriesIDList = seriesBrand.series_code_get('seriesid')
    print(seriesIDList)
