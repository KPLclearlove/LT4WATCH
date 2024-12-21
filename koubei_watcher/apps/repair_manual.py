from bs4 import BeautifulSoup
import json

# 读取 HTML 文件
with open('A63489-2066461.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# 提取页面标题
title = soup.find('h4').text.strip()


# 定义解析内容函数
def parse_content(block):
    steps = []
    references = []
    images = []

    for li in block.find_all('li'):
        step_text = li.get_text(separator=' ', strip=True)  # 提取步骤文字
        image_tag = li.find('img')
        image_src = image_tag['src'] if image_tag else None  # 提取图片链接
        link_tag = li.find('a')
        link_href = link_tag['href'] if link_tag else None  # 提取跳转链接

        # 添加每一步
        steps.append({
            'step': step_text,
            'image': image_src,
            'link': link_href
        })

    # 提取 "参见" 的引用
    for ref in block.find_all('a', class_='x-cell-link-2-0'):
        references.append({
            'text': ref.text.strip(),
            'href': ref['href']
        })
        print(references)
    return {'steps': steps, 'references': references}


# 提取主要内容块
content_blocks = soup.find_all('div', class_='x-servinfosub-2-0')
structured_sections = []

# 解析每个内容块
for block in content_blocks:
    section_title = block.find('h5').text.strip() if block.find('h5') else "未命名部分"
    parsed_content = parse_content(block)

    structured_sections.append({
        'section_title': section_title,
        'steps': parsed_content['steps'],
        'references': parsed_content['references']
    })

# 解析全局跳转索引
jump_index = {}
for section in structured_sections:
    for reference in section['references']:
        jump_index[reference['href']] = {
            'source_section': section['section_title'],
            'description': reference['text']
        }

# 合成最终结构化数据
structured_data = {
    'title': title,
    'sections': structured_sections,
    'jump_index': jump_index
}

# 输出 JSON 数据
output_file = 'structured_manual.json'
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(structured_data, json_file, ensure_ascii=False, indent=4)

print(f"结构化数据已保存至 {output_file}")
