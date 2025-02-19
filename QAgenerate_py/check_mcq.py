import time
import pandas as pd
from openai import OpenAI
import os
import json
import requests
import numpy as np


def checkQA(input_text):          #题目输入
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
    print(response_text)
    return json.loads(response_text)['answer']

def cache(array):
    array_1x2 = array.reshape((1, 2))
    df = pd.DataFrame(array_1x2)
    return df

c=['id','来源','Question','A','B','C','D'] #待读取字段
QA_list = pd.read_excel('.xlsx')[c]


df = pd.DataFrame()
df_error = pd.DataFrame()

for index, row in QA_list.iterrows():
    try:
        time.sleep(8)  # 暂停8秒   minimax多等一会比较稳定
        # 创建一个包含当前行所有数据的字符串
        Qstr = f"Question: {row['Question']}\nA: {row['A']}\nB: {row['B']}\nC: {row['C']}\nD: {row['D']}"
        print(Qstr)
        A = checkQA(Qstr)  # 调用工作流生成题目
        # 将响应转换成JSON对象，然后转换成NumPy数组
        Alist = json.loads(A)
        array = np.array(Alist)
        returndf = cache(array)  # 假设 cache 函数返回一个DataFrame
        # 将当前行和 returndf 合并
        combined_df = pd.DataFrame([row]).reset_index(drop=True).join(returndf.reset_index(drop=True))
        # 将数据追加到 df
        df = pd.concat([df, combined_df], axis=0, ignore_index=True)

    except Exception as e:
        df_error = pd.concat([df_error, pd.DataFrame([row])], axis=0, ignore_index=True)
        
        
new_column_names = ['id','来源','Question','A','B','C','D','answer','why']
df.columns = new_column_names

#result_df = pd.concat([QA_list, df], axis=1)

df.to_excel('check.xlsx', index=False)
df_error.to_excel('check_error.xlsx', index=False)


