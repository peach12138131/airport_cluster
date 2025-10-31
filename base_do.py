from dotenv import load_dotenv
import pandas as pd
import requests
import json
import os

import base64
import re
import time
from datetime import datetime
import asyncio
import httpx
import os
import re
import pytz
import ipaddress
from openai import OpenAI
from os import path as osp
import base64


def png_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded_string}"


def jpg_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded_string}"

GPT4O_API_KEY = 's'
GPT4O_API_URL = "https://api.openai.com/v1/chat/completions"

GPT4O_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {GPT4O_API_KEY}"
}


def LLM_generate(text, image_paths=[], temp=None, presence_penalty=None, is_print=False, llm_name='basedo-r',
                 sys_prompt=""):
    API_KEY = ""
    API_URL = ""
    HEADERS = {}
    selected_model = ''
    if llm_name == 'gpt4o':
        API_URL = GPT4O_API_URL
        HEADERS = GPT4O_HEADERS
        selected_model = 'gpt-4.1'
    elif llm_name == 'basedo-r':
        API_URL = 'http://8.219.186.79:8095/v1/chat/completions'
        HEADERS = GPT4O_HEADERS
        selected_model = 'basedo-r'
    else:
        API_URL = GPT4O_API_URL
        HEADERS = GPT4O_HEADERS
        selected_model = 'gpt-4.1'
    num = 10
    res = ""
    messages = [{"role": "user", "content": text}]
    while num > 0 and len(res) == 0:
        try:
            content = [{"type": "text", "text": text}]
            for image_path in image_paths:
                with open(image_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}})

            data = {"model": selected_model, "stream": False,
                    "messages": [{"role": "system", "content": sys_prompt}, {"role": "user", "content": content}]}
            data = json.dumps(data)
            response = requests.post(API_URL, headers=HEADERS, data=data)
            response_json = response.json()
            res = response_json['choices'][0]['message']['content']
        except Exception as e:
            print(e)
            num -= 1
    if is_print:
        print("yes print")
    return res

# # 示例调用
if __name__ == "__main__":
    print(LLM_generate(
        'Please help me analyze the popular routes for private charter flights at Seletar Airpor (WSSL), recent patterns of takeoffs and landings, trends in popular aircraft models, and so on.',
        llm_name='basedo-r'))