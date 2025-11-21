import requests
import json
from datetime import datetime
import os
import random
from typing import List, Dict, Any, Optional,Generator
from collections import defaultdict
import time

from airport_cluster_config import airport_data,keywords_designer_prompt,seo_matadata,seo_rewrite_prompt,seo_link,query_gpt_model
from base_do import LLM_generate


date_str = datetime.now().strftime("%Y%m%d")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = f"./output/airportcluster2"
os.makedirs(output_dir, exist_ok=True)


base_do_prompt="Please help me analyze the popular routes for private charter flights at Airpor {}, recent patterns of takeoffs and landings, related route information,trends in popular aircraft models, and so on."
j=0
for country, airports in airport_data.items():
    print(f"收集国家: {country}")
    country_dir = os.path.join(output_dir, country)
    os.makedirs(country_dir, exist_ok=True)
    for airport in airports:
        try:
            print(f"  国家: {country}，机场: {airport}")
            #获取机场数据
            print("获取机场数据")
            base_prompt=base_do_prompt.format(airport)
            airport_info=LLM_generate(base_prompt,llm_name='basedo-r')
            print(airport_info)
            

            #提取关键词
            print("提取关键词")
            keywords_prompt = keywords_designer_prompt.format(airport,airport_info)
            keywords=query_gpt_model(keywords_prompt, "")
            print(keywords)
            

            #生成metadata
            print("生成metadata")
            metadata_prompt = seo_matadata.format(airport, keywords,f"current time is {date_str} \n "+airport_info)
            
            metadata = query_gpt_model(metadata_prompt, "")
            print(metadata)
           

            # 3重写
            print("重写")
            seo_rewrite = seo_rewrite_prompt.format(airport_info,keywords,metadata)
            seo_article = query_gpt_model(seo_rewrite,"")
            

            # 植入链接
            print("植入链接")
            seo_link_prompt = seo_link.format(seo_article)
            final_seo_article = query_gpt_model(seo_link_prompt, "")
            

            final_seo_article = f"keywords\n{keywords}\n\n{final_seo_article}"

            log_content = f"collected news \n{final_seo_article} \n \nkeywords\n{keywords}\n\n"

            airport_dir = os.path.join(country_dir, airport)
            os.makedirs(airport_dir, exist_ok=True)

            seo_filename = os.path.join(airport_dir, f'{country}_{airport}_{timestamp}.txt')
            with open(seo_filename, 'w', encoding='utf-8') as f:
                f.write(final_seo_article)
                print(f'{country}_{airport}_{timestamp}.txt success')

            # j += 1
            # if j>=1:
            #     print(f'{country}测试完成')
            #     break
        except Exception as e:
            print(f'{country}_{airport}_{timestamp}.txt failed')
            print(f" 处理失败 {country}_{airport}_{timestamp}: {e}")
            continue
           






