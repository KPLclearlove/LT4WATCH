
import json
import requests
import re

total_dict = {}
cr_dict = {}
total_cr = {}
repeat_list1 = []#现在
repeat_list2 = []#过去
repeat_detect = True
replies_list = []
html_page = 1
topic_id = 109763466
title = None
title_contents = None
title_content = None
while repeat_detect:

    url  = f'https://club.autohome.com.cn/bbs/thread//{topic_id}-{html_page}.html'
    header =  {
        "user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36 Edg/130.0.0.0"
    }

    html_resp = requests.get(url, headers= header)
    content = html_resp.text

    if html_page == 1:
        title_obj = re.compile(r"<title>汽车之家\|(.*?)\|", re.S)#标题
        title = title_obj.search(content)
        title = title.group(1)
        title_content_obj = re.compile(r'<div class="tz-paragraph">(.*?)</div>', re.S)#标题正文
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

    repeat_list2 =repeat_list1
    cleaned_comments = []
    for comment in comments:
        # 去掉 <img> 标签和其他 HTML 标签
        cleaned_comment = re.sub(r'<img.*?>', '', comment)  # 去除所有 <img> 标签
        cleaned_comment = re.sub(r'<[^>]*>', '', cleaned_comment)  # 去除其他 HTML 标签
        # 去除多余的空白字符
        cleaned_comment = cleaned_comment.strip()
        cleaned_comments.append(cleaned_comment)

    comments_id_obj = re.compile(r'<div data-floor=".*?" data-reply-id="(.*?)" class="reply-bottom-editor fn-hide"></div>', re.S)
    comments_id_list = comments_id_obj.findall(content)
    comments_id_str = ",".join(comments_id_list)
    print(cleaned_comments)
    '''
    获得每个评论底下的回复
    '''

    url = "https://club.m.autohome.com.cn/comment/getcommentsbyreplyids"
    param = {
        "topicId": f"{topic_id}",
        "replyIds": comments_id_str,
        'tmemberid': '1',
        'bbsid': 3207
    }
    header = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
    }
    reply_resp = requests.get(url,params= param)
    reply_json = reply_resp.json()
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
    print(replies_list)
    print(len(cleaned_comments))
    cr_dict = dict(zip(cleaned_comments, replies_list))
    total_cr.update(cr_dict)
    html_page = html_page + 1
total_dict = {
    'title': title,
    'content': title_content,
    'replay': total_cr
}

if total_cr != {}:
    with open('total_dict.json', 'w', encoding='utf-8-sig') as f:
        json.dump(total_dict, f, ensure_ascii=False, indent=4)



