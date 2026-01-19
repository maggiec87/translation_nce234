import re

# 读取文件内容
with open('data_nce3.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 正则表达式说明：
# (Lesson\s+\d+.*?) -> 捕获 Lesson 1 部分
# 第[0-9一二三四五六七八九十百]+课[:：\s]* -> 匹配 第X课、第X课：等
# (.*?) -> 捕获后面的实际标题
pattern = r'("title":\s*")(Lesson\s+\d+.*?)(第[0-9一二三四五六七八九十百]+课[:：\s]*)(.*?)"'

# 执行替换
cleaned_content = re.sub(pattern, r'\1\2 \4"', content)

# 保存新文件
with open('data_nce3_cleaned.js', 'w', encoding='utf-8') as f:
    f.write(cleaned_content)

print("处理成功，已生成 data_nce3_cleaned.js")