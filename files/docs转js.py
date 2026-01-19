import docx
import json
import re

def organize_nce4(file_path, output_js):
    doc = docx.Document(file_path)
    
    full_data = []
    current_lesson = None
    
    # 用于临时存储当前课的所有文本
    temp_text = []
    
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
            
        # 匹配标题行，例如: Lesson 1 Finding fossil man 发现化石人
        if re.match(r'^Lesson \d+', text, re.I):
            # 如果已有收集到的课程，先进行处理
            if current_lesson:
                full_data.append(process_lesson(current_lesson, temp_text))
            
            current_lesson = text
            temp_text = []
        else:
            temp_text.append(text)
            
    # 处理最后一课
    if current_lesson:
        full_data.append(process_lesson(current_lesson, temp_text))

    # 写入 JS 文件
    with open(output_js, 'w', encoding='utf-8') as f:
        f.write("const data_New_Concept_English_4_zh_CN_dual = ")
        json.dump(full_data, f, ensure_ascii=False, indent=2)
        f.write(";")

def process_lesson(title, lines):
    """
    逻辑：根据文档结构，通常上半部分是英文，'参考译文' 之后是中文。
    我们将英文段落和中文段落按顺序一一对应。
    """
    en_paragraphs = []
    cn_paragraphs = []
    is_translation = False
    
    for line in lines:
        if "参考译文" in line:
            is_translation = True
            continue
        
        if is_translation:
            cn_paragraphs.append(line)
        else:
            en_paragraphs.append(line)
            
    pairs = []
    # 取两者中较短的长度进行匹配，防止溢出
    length = min(len(en_paragraphs), len(cn_paragraphs))
    for i in range(length):
        pairs.append({
            "en": en_paragraphs[i],
            "cn": cn_paragraphs[i]
        })
        
    return {
        "title": title,
        "pairs": pairs
    }

# 使用方法
try:
    # 请确保文件名与你本地的一致
    organize_nce4('NCE 4 - 中英.docx', 'data_nce4_full.js')
    print("整理完成！已生成 data_nce4_full.js")
except Exception as e:
    print(f"出错啦: {e}")