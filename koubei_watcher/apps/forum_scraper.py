import requests
import re
import json
import pickle
import time
import random
import os
from gpt import FastGptClient

class Forum:

    def __init__(self, series_id):
        self.series_id = series_id

    def get_comment_series(self):
        total_list = []
        pageNum = 1
        flag = True
        series_id = self.series_id
        url = 'https://club.autohome.com.cn/frontapi/data/page/club_get_topics_list'
        while flag:
            comments_list = []
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

                if comments:
                    for comment in comments:
                        comments_list.append(comment['biz_id'])
                    print('第', pageNum, '页')
                    pageNum += 1
                    total_list.append(comments_list)
            except:
                flag = False
                print('已获取全部')
        return  total_list

    def get_comments(self):
        comment_list = self.get_comment_series()
        obj = re.compile(r"", re.S)
        header = {
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36 Edg/130.0.0.0"
        }
        for comment_id in comment_list:
            url = f'https://club.autohome.com.cn/bbs/thread//{comment_id}-1.html'
            resp = requests.get(url, headers=header, timeout=5)
            content = resp.text
            title_obj = re.compile(r"<title>汽车之家\|(.*?)\|", re.S)
            title = title_obj.search(content)

    def get_all(self, topic_id):
        series_id = self.series_id
        total_dict = {}
        cr_dict = {}
        total_cr = {}
        repeat_list1 = []  # 现在
        repeat_list2 = []  # 过去
        repeat_detect = True
        replies_list = []
        html_page = 1
        title_contents = None
        while repeat_detect == True:

            url = f'https://club.autohome.com.cn/bbs/thread//{topic_id}-{html_page}.html'
            header = {
                "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36 Edg/130.0.0.0"
            }

            try:
                html_resp = requests.get(url, headers=header)
                content = html_resp.text
            except json.JSONDecodeError:
                continue
            if html_page == 1:
                title_obj = re.compile(r"<title>汽车之家\|(.*?)\|", re.S)  # 标题
                title = title_obj.search(content)
                title = title.group(1)
                title_content_obj = re.compile(r'<div class="tz-paragraph">(.*?)</div>', re.S)  # 标题正文
                title_content = title_content_obj.findall(content)
                if title_content:
                    title_contents = [re.sub(r'<br>', '', item) for item in title_content]
            '''
            获得所有评论以及他们的回复,每个评论会形成一个字典，键为评论，值为评论的回复
            '''
            comment_obj = re.compile(
                r'<div class="reply-detail">\s*(?:<div layer1="text-s"></div>)?(.*?)(?:<div layer1="text-e">)?</div>',
                re.S
            )
            comments = comment_obj.findall(content)
            repeat_list1 = comments
            if repeat_list1 == repeat_list2:
                repeat_detect = False
                break
            repeat_list2 = repeat_list1
            cleaned_comments = []
            for comment in comments:
                # 去掉 <img> 标签和其他 HTML 标签
                cleaned_comment = re.sub(r'<img.*?>', '', comment)  # 去除所有 <img> 标签
                cleaned_comment = re.sub(r'<[^>]*>', '', cleaned_comment)  # 去除其他 HTML 标签
                # 去除多余的空白字符
                cleaned_comment = cleaned_comment.strip()
                cleaned_comments.append(cleaned_comment)

            comments_id_obj = re.compile(
                r'<div data-floor=".*?" data-reply-id="(.*?)" class="reply-bottom-editor fn-hide"></div>', re.S)
            comments_id_list = comments_id_obj.findall(content)
            comments_id_str = ",".join(comments_id_list)

            '''
            获得每个评论底下的回复
            '''

            url = "https://club.m.autohome.com.cn/comment/getcommentsbyreplyids"
            param = {
                "topicId": f"{topic_id}",
                "replyIds": comments_id_str,
                'tmemberid': '1',
                'bbsid': series_id
            }
            header = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
            }
            try:
                reply_resp = requests.get(url, params=param)
                reply_json = reply_resp.json()
            except  json.JSONDecodeError:
                continue
            reply_list = []
            replies_list = []
            for comment in reply_json['result']:
                reply_list = comment.get('comments', [])
                reply_list_list = []

                # 如果有回复内容，提取并添加到列表中
                if isinstance(reply_list, list):  # 确保 reply_list 是一个列表
                    for reply in reply_list:
                        # 检查 reply 的结构，提取实际内容
                        if 'content' in reply and reply['content']:
                            reply_list_list.append(reply['content'][0]['content'])

                # 无论是否有回复，都只添加一次到 replies_list
                replies_list.append(reply_list_list)

            cr_dict = dict(zip(cleaned_comments, replies_list))
            total_cr.update(cr_dict)
            html_page = html_page + 1
            html_resp.close()
        total_dict = {
            'title': title,
            'content': title_contents,
            'replay': total_cr
        }
        with open( f'{series_id}-{topic_id}.json', 'w', encoding='utf-8-sig') as f:
            json.dump(total_dict, f, ensure_ascii=False, indent=4)

    def gpt(self, data):
        api_url = 'http://localhost:3002/api/v1/chat/completions'  # 如果遇到404，可以试试去掉/v1
        api_key = 'fastgpt-c03LZFyO6OKFRb6NRQKEtMswEcex2rX0H9bN7Pb8DfhCH5H89OejsRTTmO'  # 替换为实际API密钥
        # 创建FastGptClient实例
        client = FastGptClient(api_url, api_key)
        title = data['title']
        content = data['content']
        reply = data['replay']
        result = client.get_response(f'请你帮我把这个论坛内容转化成描述性的文本用于被rag知识库理解,请你只输出结果，并且用[]把你输出的内容框起来供我正则抓取'
                                     f'帖子标题是{title},帖子正文是{content}'
                                     f'评论及其回复是{reply}')
        return  result


if __name__ == '__main__':
    car = Forum(series_id=3207)

    with open('topic_id.pkl', 'rb') as f:
        topic_id = pickle.load(f)

    for i in topic_id:
        for j in i:
            # 定义输出文件的完整路径
            file_path = os.path.join( f'{car.series_id}-{j}.json')

            # 如果文件已存在，则跳过该 topic_id
            if os.path.exists(file_path):
                print(f"{j} 已存在，跳过")
                continue
            else:
                print(f"{j} 已完成")
                car.get_all(topic_id=j)  # 调用 car.get_all 方法
                # 假设 car.get_all 会保存数据为 json 文件，确保它写入 file_path
                time.sleep(random.randrange(3, 8))
'''
if __name__ == '__main__':
    # 创建输出文件（如果尚未存在）
    num = 1
    with open('book.txt', 'w', encoding='utf-8-sig') as f:
        pass  # 如果只需要打开文件并确认其存在，则可以只写这一行
    for filename in os.listdir('F:/The Comments Watcher/The Comments Watcher/koubei_watcher/data/atsl/apps'):
        if num<=2792:
            num = num + 1
            continue
        if filename.endswith('.json'):
            file_path = os.path.join('F:/The Comments Watcher/The Comments Watcher/koubei_watcher/data/atsl/apps',
                                     filename)

            # 确保文件可以被正确打开和读取
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)

            car = Forum(series_id=1)  # 假设Forum类有__init__方法接受series_id参数

            # 调用GPT方法处理数据，并将结果写入输出文件
            processed_data = car.gpt(data)

            # 将处理后的数据写入输出文件，确保每条数据之间有换行符
            with open('book.txt', 'a', encoding='utf-8-sig') as f:
                f.write(processed_data + '\n')
            print(num)
            num += 1#2792
'''