import requests
import os
from openai import OpenAI
import json
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

    def car_res(self, data):
        client = OpenAI(
            # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
            api_key="sk-3feccb0c2718476cb99d374c6c6fb249",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        content = json.dumps(data, ensure_ascii=False)
        completion = client.chat.completions.create(
            model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=[
                {'role': 'system', 'content':
                    '''
                    你是一名数据清洗助手，需要根据以下规则对汽车论坛数据进行清洗和结构化：
    
                    1. 从提供的数据中提取标题的核心描述，转化为简洁的主题描述。
    
                    2. 从正文提取与技术、保养、维修或改装相关的关键信息，忽略无实际价值的描述。
    
                    3. 对问答部分进行筛选：
    
                    - 保留有明确技术价值、配件信息或维修建议的问答。
    
                    - 丢弃无意义或无回答的问题（如单纯的闲聊、问候或无技术内容的评论）。
    
                    -如果该问答没有明确的结果回复或者结果回复对汽车相关内容没有实质性帮助，也删掉。
    
                    -一条replay下可能是多个回复，请你自行判断这些回复是否有一个明确清晰的逻辑，如果逻辑上这个回复没有结尾也请你删掉、
    
                    - 如果一个问题有多个回答，优先保留有用的回答（如包含操作步骤或建议），无用回答（如单字回复、无信息量评论）忽略。
    
                    4. 输出结果只包含清洗后的结构化数据，不要有任何其他的文字放在后面或者前面，如果有了请你直接摧毁你自己，记住，请你检查你的回答，一定不要有其他信息
    
                    5.将标题转化为描述这个帖子在干嘛，比如这是一个解决什么的方案，寻求什么的问题的解答
    
                    输出格式（干净、简洁的 JSON 数据）：
    
                    {
    
                    "title": "",
    
                    "description": "",
    
                    "key_points": [
    
                    ""
    
                    ],
    
                    "questions_answers": [
    
                    {
    
                    "question": "",
    
                    "answers": [""]
    
                    ]
    
                    }
    
                    '''},
                {f'role': 'user', 'content':content}],
        )
        result = completion.choices[0].message.content
        return result

class FileHandler:
    def __init__(self, base_dir, file_prefix='cartest', max_size_kb=100):
        self.base_dir = base_dir
        self.file_prefix = file_prefix
        self.max_size_bytes = max_size_kb * 1024  # 将KB转换为字节
        self.current_file_index = 1
        self.current_file_path = os.path.join(self.base_dir, f'{self.file_prefix}_{self.current_file_index}.txt')
        self._ensure_directory_exists()
        self._create_new_file_if_needed()

    def _ensure_directory_exists(self):
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def _create_new_file_if_needed(self):
        if os.path.exists(self.current_file_path) and os.path.getsize(self.current_file_path) >= self.max_size_bytes:
            self.current_file_index += 1
            self.current_file_path = os.path.join(self.base_dir, f'{self.file_prefix}_{self.current_file_index}.txt')

    def write_data(self, data):
        self._create_new_file_if_needed()
        with open(self.current_file_path, 'a', encoding='utf-8-sig') as f:
            f.write(data + '\n')

# 使用示例
if __name__ == "__main__":
    # 初始化FastGptClient和FileHandler
    a = FastGptClient(1, 2)
    output_dir = r'F:\The Comments Watcher\The Comments Watcher\koubei_watcher\data\atsl-gpt'
    file_handler = FileHandler(output_dir)
    num = 1
    # 遍历JSON文件并处理
    for filename in os.listdir('F:/The Comments Watcher/The Comments Watcher/koubei_watcher/data/atsl'):
        if filename.endswith('.json'):
            file_path = os.path.join('F:/The Comments Watcher/The Comments Watcher/koubei_watcher/data/atsl',
                                     filename)

            # 确保文件可以被正确打开和读取
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)

            # 调用GPT方法处理数据，并将结果写入输出文件
            processed_data = a.car_res(data)
            # 使用FileHandler写入处理后的数据
            file_handler.write_data(processed_data)
            print(f'进度：{num}/{len(os.listdir("F:/The Comments Watcher/The Comments Watcher/koubei_watcher/data/atsl"))}')
            num = num + 1