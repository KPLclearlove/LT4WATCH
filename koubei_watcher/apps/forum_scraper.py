import requests
import re


class Forum:

    def __init__(self, series_id):
        self.series_id = series_id

    def get_comment_series(self):
        pageNum = 1
        flag = True
        series_id = self.series_id
        url = 'https://club.autohome.com.cn/frontapi/data/page/club_get_topics_list'
        comments_list = []
        while flag:
            param = {
                'page_num': f'{pageNum}',
                'page_size': '50',
                'club_bbs_type': 'c',
                'club_bbs_id': '3207',
                'club_order_type': '1'
            }
            resp = requests.get(url, params= param)
            try:
                reviews = resp.json()
                comments = reviews['result']['items']

                for comment in comments:
                    comments_list.append(comment['biz_id'])
                pageNum = pageNum +1

            except:
                flag = False
                print('已结束')
            return comments_list

    def get_comments(self):
        comment_list = self.get_comment_series()
        obj = re.compile(r"", re.S)
        header = {
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36 Edg/130.0.0.0"
        }
        for comment_id in comment_list:
            url = f'https://club.autohome.com.cn/bbs/thread//{comment_id}-1.html'
            resp = requests.get(url, headers=header)
            content = resp.text
            title_obj = re.compile(r"<title>汽车之家\|(.*?)\|", re.S)
            title = title_obj.search(content)

if __name__ == '__main__':
    car = Forum(series_id = 3207 )
    car.get_comment_series()
