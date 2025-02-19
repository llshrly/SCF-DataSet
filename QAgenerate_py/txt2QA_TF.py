import time
import pandas as pd
from openai import OpenAI
import os
import json
import requests
import numpy as np

def get_files_absolute_paths(folder_path):
    result = []
    # 确保给定的路径是存在的
    if not os.path.exists(folder_path):
        print(f"The path {folder_path} does not exist.")
        return []

    # 列出给定文件夹中的所有文件（不包括子文件夹）
    for file in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file)):
            # 构造文件的绝对路径
            file_path = os.path.abspath(os.path.join(folder_path, file))
            result.append(file_path)
        # 输出文件的绝对路径
        # print(file_path)
    return result


def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    return content


def get_llm_response(input_text):          #通过txt出题
    url = 'your_dify_url'

    data = {
    "inputs": {},
    "query": input_text,
    "response_mode": "blocking",
    "conversation_id": "",
    "user": "abc-123",
    }
    json_data = json.dumps(data)
    response = requests.post(url,
                             data=json_data,
                             headers={
                                 "Content-Type": "application/json",
                                 'Authorization': f'Bearer  your_dify_workflow_apikey'  #apikey 
                             }
                             )

    response_text = response.text

    return json.loads(response_text)['answer']



def cache(array):
    array_5x3 = array.reshape((5, 3))
    df = pd.DataFrame(array_5x3)
    return df

    

folder_path = r'D:'
files_path = get_files_absolute_paths(folder_path)

failed_files = []  # 用于存储失败的文件路径
error=[]
df = pd.DataFrame()

for file_index,file_path in enumerate(files_path):
    time.sleep(5)  # 暂停5秒
    file_content = read_txt_file(file_path)  # 读取文本内容
    print(file_content)
    try:

        llm_response = get_llm_response(file_content)  # 调用工作流生成题目
        match = re.search(r'\[.*?\]', llm_response, re.DOTALL)
        print(match.group(0))
        data=json.loads(match.group(0))
        returndf = pd.DataFrame([
            {
                "question": item["question"],
                "answer": item["answer"]
            }
            for item in data
            ])
        returndf = returndf.assign(url=str(file_path))
        df = pd.concat([df, returndf], axis=0, ignore_index=True)  # 将数据追加到df
    except Exception as e:
        print(f"error: {file_path}, Error: {e}")
        failed_files.append(file_path)  # 将出错的file_path添加到列表中
        error.append(e)


# 打印失败的文件列表
#print("Failed files:", failed_files)
# 循环结束后，df包含所有满足条件的文件处理结果

new_column_names = ['question','answer','file']
df.columns = new_column_names
df.to_excel('dataset\TF.xlsx', index=False)


error_df = pd.DataFrame({
    'url': failed_files,
    'error': error
})

error_df.to_excel('dataset\error_TF.xlsx', index=False)