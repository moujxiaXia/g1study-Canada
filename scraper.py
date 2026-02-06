import requests
from bs4 import BeautifulSoup
import re

def scrape_questions(url):
    """
    从指定URL爬取题目信息
    """
    try:
        # 发送HTTP请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # 解析HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 根据URL判断语言
        language = 'zh' if 'language=zh' in url else 'en'
        
        questions = []
        
        # 查找题目容器
        # 注意：这里的解析逻辑需要根据实际网站结构调整
        question_elements = soup.find_all('div', class_='question-item')
        
        for elem in question_elements:
            try:
                # 提取题目文本
                question_text_elem = elem.find('div', class_='question-text')
                question_text = question_text_elem.get_text(strip=True) if question_text_elem else ''
                
                # 提取选项
                options = {}
                options_container = elem.find('div', class_='options')
                if options_container:
                    option_items = options_container.find_all('div', class_='option')
                    for i, option in enumerate(option_items):
                        option_letter = chr(65 + i)  # A, B, C, D
                        options[option_letter] = option.get_text(strip=True)
                
                # 提取正确答案
                correct_answer_elem = elem.find('div', class_='correct-answer')
                correct_answer = correct_answer_elem.get_text(strip=True) if correct_answer_elem else ''
                
                # 提取解释
                explanation_elem = elem.find('div', class_='explanation')
                explanation = explanation_elem.get_text(strip=True) if explanation_elem else ''
                
                # 分类（简化处理，实际可能需要更复杂的逻辑）
                category = 'general'  # 默认分类
                
                if question_text and options:
                    questions.append({
                        'question_text': question_text,
                        'options': options,
                        'correct_answer': correct_answer,
                        'explanation': explanation,
                        'language': language,
                        'category': category
                    })
            except Exception as e:
                # 跳过解析出错的题目
                continue
        
        return questions
    except Exception as e:
        raise Exception(f"爬取失败: {str(e)}")

# 示例使用
if __name__ == '__main__':
    # 示例URL（需要替换为实际URL）
    test_url_zh = "https://www.ccdriving.ca/index.php?route=test/mock&test_type=view&language=zh_HK"
    test_url_en = "https://www.ccdriving.ca/index.php?route=test/mock&test_type=view&language=en"
    
    try:
        questions = scrape_questions(test_url_zh)
        print(f"成功爬取 {len(questions)} 道中文题目")
        
        # 打印第一道题目的信息作为示例
        if questions:
            print("第一道题目示例:")
            print(f"题目: {questions[0]['question_text']}")
            print(f"选项: {questions[0]['options']}")
            print(f"答案: {questions[0]['correct_answer']}")
            print(f"解释: {questions[0]['explanation']}")
    except Exception as e:
        print(f"错误: {e}")