import requests


class FastGptClient:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def get_response(self, message_content):
        # 设置请求数据，包括 chatId 和消息内容
        data = {
            "chatId": False,  # 使用指定的 chatId 来使用上下文功能
            "stream": False,
            "detail": False,
            "variables": {
                "uid": "",
                "name": ""
            },
            "messages": [
                {
                    "role": "user",
                    "content": message_content  # 用户输入的内容
                }
            ]
        }

        # 发送POST请求到FastGpt API
        response = requests.post(self.api_url, headers=self.headers, json=data)

        # 检查请求结果并返回content字段
        if response.status_code == 200:
            content = response.json().get("choices")[0]["message"]["content"]
            return content
        else:
            print(f"请求失败: 状态码 {response.status_code}")
            print("错误信息:", response.text)
            return None


# 使用示例
if __name__ == "__main__":
    api_url = 'http://localhost:3002/api/v1/chat/completions'  # 如果遇到404，可以试试去掉/v1
    api_key = 'fastgpt-c03LZFyO6OKFRb6NRQKEtMswEcex2rX0H9bN7Pb8DfhCH5H89OejsRTTmO'  # 替换为实际API密钥

    # 创建FastGptClient实例
    client = FastGptClient(api_url, api_key)

    # 调用get_response方法并传入消息内容
    result = client.get_response('你是第几次回复我')
    print(result)#1462
