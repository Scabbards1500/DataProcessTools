import requests
import json

url = "https://ai.gileadchina.cn/gpustackrd3/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer gpustack_64805edbe6790aa3_3ec197b7e68eee3159ccf0d334f38fcf"
}

data = {
    "seed": None,
    "stop": None,
    "temperature": 1,
    "top_p": 1,
    "max_tokens": 4096,
    "frequency_penalty": None,
    "presence_penalty": None,
    "model": "qwen2.5-vl_72b_bf16",
    "messages": [
        {
            "role": "user",
            "content": "我是你爹"
        }
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    result = response.json()
    print("模型回复：", json.dumps(result, ensure_ascii=False, indent=2))
else:
    print(f"请求失败，状态码：{response.status_code}")
    print("返回内容：", response.text)

