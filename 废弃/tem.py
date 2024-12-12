

import requests
import re

total_dict = {}
cr_dict = {}
total_cr = {}
repeat_list1 = []#现在
repeat_list2 = []#过去
repeat_detect = True
html_page = 1
topic_id = 80084945
while  repeat_detect == True:

    url  = f'https://club.autohome.com.cn/bbs/thread//{topic_id}-{html_page}.html'
    header =  {
        "user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36 Edg/130.0.0.0"
    }

    html_resp = requests.get(url, headers= header)
    content = html_resp.text

    title_obj = re.compile(r"<title>汽车之家\|(.*?)\|", re.S)#标题
    title = title_obj.search(content)
    title = title.group(1)
    title_content_obj = re.compile(r'<div class="tz-paragraph">(.*?)</div>', re.S)#标题正文
    title_content = title_content_obj.findall(content)#
    print(title_content)
    if title_content:
        title_contents = [re.sub(r'<br>', '', item) for item in title_content]
    '''
    获得所有评论以及他们的回复,每个评论会形成一个字典，键为评论，值为评论的回复
    '''
    comment_obj = re.compile(
        r'<div class="reply-detail">\s*<div layer1="text-s"></div>(.*?)<div layer1="text-e"></div>',
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
    reply_list = []
    replies_list = []
    for comment in reply_json['result']:
        reply_list = comment['comments']
        if type(reply_list) == type(cleaned_comments):
            detect = 0
            reply_list_list = []
            for reply in reply_list:
                reply_list_list.append(reply['content'][0]['content'])

            reply_list.append(reply_list_list)
            replies_list.append(reply_list_list)

    cr_dict = dict(zip(cleaned_comments, replies_list))
    total_cr.update(cr_dict)
    html_page = html_page + 1
total_dict = {
    'title': title,
    'content': title_contents,
    'replay': total_cr
}
print(total_dict)




