import requests

def get_reviews(series_id, page_num):
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
    koubei_url = 'https://k.m.autohome.com.cn/ajax/serieskoubei/getserieskoubeilistbytag'
    # 发送请求
    resp = requests.get(url=koubei_url, params=koubei_param)
    with open('../config/json模板.json', 'w', encoding='utf-8') as f:
        f.write(resp.text)
get_reviews(3411,1)