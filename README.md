# 供应链金融大模型评测数据集

<b>简体中文</b>|[English](./README_EN.md)

## 简介

本项目旨在实现行业数据集的自动化生成，生成的数据集可应用于测评大模型在特定行业领域的知识能力。相关研究详见文章:[《供应链金融大模型评测体系的建立》](https://mp.weixin.qq.com/s?__biz=MzU0NjkxMzkwMQ==&mid=2247485540&idx=1&sn=eb8c79bedc1f50785bc55fce66c84068&chksm=fafdd5995128080f995e1f631e0f73344ae482dd7a8f5a370c9efac12947248ffac5cb305029&mpshare=1&scene=1&srcid=0822x2QD1f09JbtdGj9tYmjh&sharer_shareinfo=5ee13f993ca383ad4700be911123e393&sharer_shareinfo_first=1646c336ffd0b1259e9e605b0418717c#rd)

目前支持单项选择题、判断题、问答题三种题型。通过 Dify 工作流实现题目生成的自动化，并结合python脚本调用 API ，完成出题材料的批量读取、生成和格式化输出。本项目生成的供应链金融数据集，已通过 Opencompass 平台对大模型行业知识能力进行测评。

供应链金融领域模型知识能力评测结果如下：

<p align="center">
  <img src="./images/图片0.png" width="30%" alt="模型评测结果">
</p>

数据集预览，总计包含2959道单选题、975道判断题和1161道简答题：

<p align="center">
  <img src="./images/图片01.png" width="80%" alt="模型评测结果">
</p>


## 目录结构说明

```bash


.
├── dataset                  # 已生成的数据集
│   ├── mcq.jsonl
│   ├── qa.jsonl
│   └── TorF.jsonl
├── docs                        # 项目相关文档
│   └── 数据集评测背景及过程.pdf
├── dify_file                # Dify 工作流
│   ├── check_mcq.yml
│   ├── check_TF.yml
│   ├── generate_mcq.yml
│   ├── generate_qa.yml
│   └── generate_TF.yml
├── QAgenerate               # Python 项目
│   ├── checkQA_mcq.py    # 校验文件
│   ├── checkQA_TF.py
│   ├── txt2QA_qa.py      # 文本生成文件
│   ├── txt2QA_mcq.py
│   ├── txt2QA_TF.py
│   ├── url2QA_TF.py          # 链接生成文件
│   ├── url2QA_mcq.py
│   ├── url2QA_qa.py
│   ├── cutPdf.py             # 其他文件（文件切割、格式转换）
│   ├── data2jsonl.py
│   ├── txt_list              # 文件夹  存放文本素材
│   └── dataset               # 文件夹  存放生成数据集
├── README.md
├── README_EN.md
```

## 环境

### 1. Dify: 版本 0.6.14

您可以根据需要，在本地部署 Dify 或使用其[云服务](https://dify.ai/zh)。若选择通过运行 Dify 的 docker-compose.yml 文件进行 Dify 服务的启动，请事先确保机器上已经安装了 [Docker](https://docs.docker.com/get-started/get-docker/) 和 [Docker Compose](https://docs.docker.com/compose/install/)。详细配置流程请参见 [Dify 指南](https://docs.ai/v/zh-hans)。

### 2. Python : 版本 3.11

本项目需要 [Python](https://www.python.org/downloads/) 环境进行出题素材的批量读取、Dify 工作流调用和题目数据集的格式化输出。

## 运行

### 1. Dify 工作流导入

本项目中的题目生成、校验所用的dify工作流，均已导出为 DSL 文件，并位于本项目的 [dify_file](./dify_file/)文件夹中，在运行前，首先需要将对应工作流导入您的 Dify 工作室中。
<p align="center">
  <img src="./images/图片1.png" width="80%" alt="dify导入图片">
</p>


### 2. LLM 节点配置

<p align="center">
  <img src="./images/图片2.png" width="25%" alt="描述文字1" hspace="20">
  <img src="./images/图片3.png" width="60%" alt="描述文字2">
</p>

配置模型供应商时，可以根据 Dify 页面提示，申请所需模型的 API Key 并使用。工作流内默认的模型是 minimax-6.5s和 qianwen1.5 模型，可以根据实际的使用需要和个人偏好修改 LLM 节点的模型供应商和模型。若更换模型需在工作流内修改 LLM 节点的模型选择。

### 3. API Key 申请与填写

#### (1)申请
<p align="center">
  <img src="./images/图片4.png" width="80%" alt="dify导入图片">
</p>

在工作流编辑界面的左侧导航栏点击“访问 API”，然后点击右上角的 API 密钥进行申请，在记录申请的 API key 的同时还需记录下右上角的 API 服务器地址。

#### (2)填写

在py文件中调用dify工作流的方法中填写对应的url和api key。

```python

def get_llm_response(input_text):         
    url = 'your_dify_url'     #add your dify url
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
                                 'Authorization': f'Bearer your_dify_workflow_apikey'  #add your workflow apikey 
                             }
                             )
    response_text = response.text
    
    return json.loads(response_text)['answer']
```


<b>请注意dify工作流和py文件的对应：</b>

生成题目的dify工作流仅由题型区分，每一条用于生成题目的工作流不论输入文本还是链接都可以生成对应题型，但不同的材料来源在批量输入时的处理方式不同，因此分别写了对应的py脚本。


<table>
    <tr>
        <th> dify 文件 </th>
        <th> python 文件 </th>
        <th> 描述</th>
    </tr>
    <tr>
        <td rowspan="2"><a href="./dify_file/generate_mcq.yml">generate_mcq.yml</a></td>
        <td><a href="./QAgenerate_py/txt2QA_mcq.py">txt2QA_mcq.py</a></td>
        <td>由文本生成单选题</td>
    </tr>
    <tr>
        <td><a href="./QAgenerate_py/url2QA_mcq.py">url2QA_mcq.py</a></td>
        <td>由url生成单选题</td>
    </tr>
    <tr>
        <td rowspan="2"><a href="./dify_file/generate_TF.yml">generate_TF.yml</a></td>
        <td><a href="./QAgenerate_py/txt2QA_TF.py">txt2QA_TF.py</a></td>
        <td>由文本生成判断题</td>
    </tr>
    <tr>
        <td><a href="./QAgenerate_py/url2QA_TF.py">url2QA_TF.py</a></td>
        <td>由url生成判断题</td>
    </tr>
    <tr>
        <td rowspan="2"><a href="./dify_file/generate_qa.yml">generate_qa.yml</a></td>
        <td><a href="./QAgenerate_py/txt2QA_qa.py">txt2QA_qa.py</a></td>
        <td>由文本生成简答题</td>
    </tr>
    <tr>
        <td><a href="./QAgenerate_py/url2QA_qa.py">url2QA_qa.py</a></td>
        <td>由url生成简答题</td>
    </tr>
</table>


### 4. 生成

#### 1）输入

出题材料的来源支持文本格式和网页链接：

- 文本格式为 txt 文件，需要将文本文件依据合适的内容长度划分为多个 txt 文件并放在一个文件夹内。

  出于当前工作流输入限制和工作流的设置，推荐将每个 txt 文档的字数控制在 1000 至 5000 之间。您也可以根据出题材料的特点，修改工作流内关于出题数量的提示词。

- 若出题材料为网页链接 url，则需要将待读取的 url 全部存于一个 `.xlsx` 文件的一个表中，且列名为 `url`。您可根据素材修改提示词。

#### 2）输出

根据生成的题型不同，输出格式会有所区别：

##### (1)选择题


| question | A | B | C | D | answer | file/url |
|  :---:  |  :---:  |  :---:  |  :---:  |  :---:  |  :---:  |  :---:   |

##### (2)判断题

| question | answer | file/url | 
|  :---:  |  :---:  |  :---:  |

##### (3)问答题

| question | answer | file/url | 
|  :---:  |  :---:  |  :---:  |


## 5.校验

当出题的文本素材的质量不稳定时，尤其是以网页链接为来源生成题目的时候，容易出现“信息题”，这类题目以具有时效性的信息或者局部的数据为考点，对于考核模型在特定领域的知识能力没有意义，因此需要将这类题目筛去，当题目数量较多时，人工筛选显然不现实，此时一种较好的解决方式就是让一个性能较好的大模型将初步生产的问题数据集做一遍，剔除做错的题目，可以将上述类型的“信息题”被筛去。
对应的dify工作流分别是[check_mcq.yml](./dify_file/check_mcq.yml)和[check_TF.yml](./dify_file/check_TF.yml)；调用上述工作流的python脚本分别是[checkQA_mcq.py](./QAgenerate_py/check_mcq.py)和[checkQA_TF.py](./QAgenerate_py/check_TF.py)。
运行前的准备与生成时相同，需导入工作流、配置模型和申请api key。

# 数据集

本项目目前生成的数据集包括选择题2959题、判断题975题、问答题1161题。为了便于测评已经全部转换为`.jsonl`格式，数据集的格式转换请参见本项目中的[data2jsonl.py](./QAgenerate_py/data2jsonl.py)。

# 模型测评

### 快速测评

本项目生成的数据集的模型测评基于[Opencompass](https://opencompass.org.cn/home)，相关配置可以参照其[使用指南](https://opencompass.org.cn/doc)。对应的数据集格式`.jsonl`的转换方式已经在”数据集“部分说明。
使用自定义数据集选择选择题（mcq）较易上手，可以直接上传mcq数据集至指定路径，通过临时性数据集的评测方式，进行简单的配置文件编辑，即可展开。而使用问答题测评则需要对数据集进行“定制化测评”，修改其默认评估指标。

### 注：
#### 1.问答题测评：
opencompass的问答题qa的默认评估指标是正确率（适配的问答题类型为确定答案的，例如“question：20+50=？answer：70“），而本项目生成的问答题为主观题，其恰当的评估指标应为匹配率，若不对该指标做出调整，会得到问答题评测得分结果为0的情况。

#### 2.判断题测评：
判断题测评有以下两种方式:
##### （1）使用问答题的测评方式并添加提示词

将TorF. jsonl上传至指定路径，在配置文件的部分进行以下修改，在确保指定数据集的同时使用qa方式进行测评，并添加提示词限制模型回答的输出:
```text
 {"path": "/your_dataset_path/panduan.jsonl", "data_type": "qa", "infer_method": "gen", "human_prompt":"问题:{question}\n请回复该问题，要求只能回答Y或者N，正确请回复:Y,错误请回复N"}
```

##### （2）使用选择题的测评方式并修改数据集字段

将判断题转换为选择题，其他过程与选择题测评相同：

例：
将:` “answer：T ”`  转换为: `“A：T, B：F, C：不确定, answer：A”`

本项目选择将判断题转换为选择题格式进行测评，且[datasest](./dataset/)文件夹中的[TorF.jsonl](./dataset/TorF.jsonl) 文件中，数据集格式已经按照上述例子进行了转换:


```text
{"question": "虚拟经济中，交易的便利性是商业繁荣的必要条件。这句话是", "A": "正确的", "B": "错误的", "C": "不确定", "answer": "A"}
{"question": "区块链技术的进步使得主体在价值创造过程中，拥有分享更多利益的博弈手段。这句话是", "A": "正确的", "B": "错误的", "C": "不确定", "answer": "A"},
{"question": "区块链技术的出现将完全消除交易中的信用问题。这句话是", "A": "正确的", "B": "错误的", "C": "不确定", "answer": "B"}
```
