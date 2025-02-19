import time
import pandas as pd
from openai import OpenAI
import os
import json
import requests
import numpy as np


def get_llm_response(input_text):          #通过url出题
    response_text =[]
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
    #print(response_text)
    return json.loads(response_text)['answer']
    
def cache(array):
    array_5x3 = array.reshape((5, 3))
    df = pd.DataFrame(array_5x3)
    return df
       

# 读取 Excel 文件
url_list = pd.read_excel('.xlsx')['url']


df = pd.DataFrame()
failed_url = []  # 用于存储失败的链接
error=[]

for i in url_list:
    try:
        #time.sleep(0.5)  # 暂停0.5秒
        llm_response = get_llm_response(i)  # 调用工作流生成题目
        match = re.search(r'\[.*?\]', llm_response, re.DOTALL)
        print(match.group(0))
        data=json.loads(match.group(0))
        returndf = pd.DataFrame([
             {
                "question": item["question"],
                "answer": item["answer"],
                "original_text": item["original_text"]
            }
            for i
            for item in data
            ])
        returndf = returndf.assign(url=str(i))
        df = pd.concat([df, returndf], axis=0, ignore_index=True)  # 将数据追加到df
    except Exception as e:
        print(f"error: {i}, Error: {e}")
        failed_url.append(i)  # 将出错的file_path添加到列表中
        error.append(e)



new_column_names = ['question','answer','original_text','file']
df.columns = new_column_names
df.to_excel('dataset\TF.xlsx', index=False)


error_df = pd.DataFrame({
    'url': failed_url,
    'error': error
})

error_df.to_excel('dataset\error_data.xlsx', index=False)





