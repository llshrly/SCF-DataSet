 # -*- coding: UTF-8 -*-
import pandas as pd
import json
# 读取Excel文件

df = pd.read_excel('.xlsx') # 替换为你的文件路径和工作表名

# 将DataFrame转换为JSON格式
json_data = df.to_json(orient='records',force_ascii=False)  # 'records'是将DataFrame转换为JSON数组的一种方式

print(json_data)

json_data=json.loads(json_data)

# 将数据保存为JSONL文件
# 打开文件准备写入
with open('YNdata.jsonl', 'w',encoding='utf-8') as file:
    # 遍历数据列表
    for data in json_data:
        
        # 将字典转换为JSON字符串
        json_str = json.dumps(data,ensure_ascii=False)
        # 写入文件，并添加换行符
        file.write(json_str + '\n')