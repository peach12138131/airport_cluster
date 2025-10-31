
import requests
import json
from datetime import datetime
import os
import random
from typing import List, Dict, Any, Optional,Generator
from collections import defaultdict
import time
import re




airport_data = [
    {"RANK": 1, "ICAO": "KTEB", "TAKE-OFF_VOLUME": 77001},
    {"RANK": 2, "ICAO": "KPBI", "TAKE-OFF_VOLUME": 44170},
    {"RANK": 3, "ICAO": "KDAL", "TAKE-OFF_VOLUME": 41132},
    {"RANK": 4, "ICAO": "KHPN", "TAKE-OFF_VOLUME": 38655},
    {"RANK": 5, "ICAO": "KVNY", "TAKE-OFF_VOLUME": 35249},
    {"RANK": 6, "ICAO": "KLAS", "TAKE-OFF_VOLUME": 32937},
    {"RANK": 7, "ICAO": "KPDK", "TAKE-OFF_VOLUME": 32289}
]



keywords_designer_prompt="""
Output language:English
You are an excellent SEO optimization specialist with expertise in search engine ranking optimization. You are now tasked with conducting critical keyword research for SEO optimization. The company needs to complete a series of article clusters, and you need to extract up to 10 keywords from one article based on materials provided by the client company: Primary keywords: include airport name. Secondary keywords: or include airport code, or the city where the airport is located, or other semantic variations. Among these, 3 should be long-tail keywords, and 2 keywords should be derived from current trending topics.
Background: Keyword research refers to the process of finding keywords to compete for rankings in search engines. The purpose is to understand the potential intent of customer searches and how they search. It also involves analyzing and comparing keywords to find the best keyword opportunities.

Your service company: JETBAY is a global private jet booking platform headquartered in Singapore, with 6 branches worldwide, committed to providing excellent global service. It provides a fast, competitive and seamless booking experience, connecting over 10,000 private jets and various fleets worldwide to bring excellent service to customers.

Task objective:
Based on the provided article content, extract keyword combinations that comply with SEO best practices, ensuring perfect alignment with article intent and cluster strategy.

As a professional SEO expert, you should possess the following professional qualities and steps:

1: You need to have keen insight, using internet marketing or advertising operations thinking to identify the most compelling breaking news, industry dynamics and hot topics that can attract user engagement. Consider how to naturally connect these elements with your brand, then refine them into relevant keywords.
2: You need global thinking ability, capable of systematically thinking about the entire article cluster, naturally linking main articles and sub-articles.
3. There are logical connections and hierarchical progression between articles, covering different stages of user search intent, avoiding keyword cannibalization (internal competition), content depth progression, avoiding repetition.


Workflow:
Step 1: Understand all article content, identify current keypoints,
Step 2: Use your professional knowledge to extract keywords,and summarize the data trend 

                                                                                              
JETBAY company provided materials:
airports: {0}
airport data : {1}


Output: Directly output keywords for this data.


"""

keywords_designer_prompt = """
# ROLE: Senior SEO Keyword Strategist for Aviation Industry
You are a specialized SEO expert with 10+ years of experience in travel/aviation keyword research.

---

## COMPANY CONTEXT
**JETBAY** - Global private jet charter platform
- HQ: Singapore | 6 global offices | 10,000+ aircraft network
- Target Audience: UHNW individuals, C-suite executives, luxury travelers
- Business Model: B2C charter booking (transactional intent primary)

---

## TASK OBJECTIVE
Extract **exactly 10 keywords** from the provided article content, following this mandatory distribution:

### Keyword Structure (MUST FOLLOW):
1. **Primary Keywords (3)** - Core focus
   - MUST include airport name/code (e.g., "ZBAA private jet charter")
   - Format: [Airport Name/Code] + [Service Type]
   - Example: "Beijing Capital International Airport private jet charter"

2. **Secondary Keywords (4)** - Supporting themes
   - Semantic variations (e.g., "business aviation ZBAA", "charter flights Beijing")
   - City-based alternatives (e.g., "Beijing airport private jet")
   - Service-adjacent terms (e.g., "VIP terminal Beijing", "jet charter rates ZBAA")

3. **Long-Tail Keywords (3)** - Specific user queries
   - Must be 5+ words
   - Include route/aircraft/price specifics
   - Example: "How much does a private jet cost from Beijing to Shanghai"
   - Example: "Best ultra-long-range jets for ZBAA departures"

---

## KEYWORD EXTRACTION METHODOLOGY

### STEP 1: Content Analysis (Silent - No Output)
Scan the article for:
- ✓ Airport identifiers (IATA/ICAO codes, full name, city)
- ✓ Route mentions (destinations, flight times)
- ✓ Aircraft types (models, categories)
- ✓ Quantitative data (prices, frequencies, passenger counts)
- ✓ User pain points (FAQs, "how to" sections)

### STEP 2: Trending Topic Integration (2 keywords MUST reflect 2025 trends)
**Current Aviation Trends to Consider:**
- Sustainable aviation fuel (SAF) adoption
- Ultra-long-range jet demand surge
- Post-pandemic leisure + business hybrid travel
- China Greater Bay Area connectivity boom
- Dynamic pricing / empty-leg optimization

**Action:** Identify 2 keywords from your 10 that naturally incorporate trending elements.
- Example: "Sustainable private jet charter ZBAA 2025"
- Example: "Beijing to Greater Bay Area business aviation routes"

### STEP 3: Search Intent Classification
Label each keyword with ONE intent type:
- **[T]** Transactional - "book", "charter", "hire", "cost"
- **[I]** Informational - "what is", "how to", "guide", "best"
- **[N]** Navigational - "[Brand] + [Service]"
- **[C]** Commercial Investigation - "vs", "comparison", "reviews"

### STEP 4: Keyword Difficulty Estimation
Assign difficulty score (1-10):
- 1-3: Low competition (long-tail, hyper-specific)
- 4-6: Medium (city + service combinations)
- 7-10: High (generic head terms like "private jet")

### STEP 5: Anti-Cannibalization Check
Ensure:
- ✓ No overlapping primary keywords between articles in the same cluster
- ✓ Each keyword targets different user journey stages:
  - Awareness: "private jet benefits"
  - Consideration: "ZBAA vs ZSPD charter comparison"
  - Decision: "book private jet ZBAA now"

---


---

## INPUT VARIABLES
**Airport Data:** {0}
**Article Content:** {1}

---

## CRITICAL RULES
**Never** create generic keywords like "private jet" or "charter flights" alone
**Always** tie keywords to specific airport/route/data mentioned in article
**Output language:** English only (regardless of input language)
**Trending keywords:** Must cite specific 2025 data/trend from article


---

Directly output your keywords
"""
seo_matadata="""
Output language:English
Role: As an SEO expert at a digital marketing agency. Your client has provided you with company name, service description, and keywords. Your task is to create title and meta description tags for their service pages. Your goal is to optimize pages for search engines and bring organic traffic to the website. When writing tags, keep in mind the company's target audience and brand guidelines.

Background: Meta Title and Meta Description are some HTML meta tags in web pages that mainly help search engines understand page content and are the most important first step in SEO optimization. Search engines analyze these Meta Titles to navigate search topic keywords and rank keywords accordingly, so the quality of Meta Titles will greatly affect SEO rankings.

Company Description: JETBAY is a global private jet booking platform headquartered in Singapore, with 6 branches worldwide, committed to providing excellent global service. It provides a fast, competitive and seamless booking experience, connecting over 10,000 private jets and various fleets worldwide to bring excellent service to customers. 24/7 aircraft availability, no purchase burden, extremely competitive pricing. The AI team has mastered the global private jet operations database, intelligently matching optimal flight resources, reducing empty flights, providing optimal charter solutions. JETBAY's mobile charter team has developed an AI platform deeply integrated with the database, using big data to optimize charter resources, achieving efficient, convenient, and sustainable flight experiences. Our charter service team has over 20 years of rich experience, providing top-tier, cost-effective flight solutions 24/7, ensuring customers enjoy seamless and personalized charter experiences. Our operations support team pays attention to every detail with the highest standards, ensuring your private flights are smooth and worry-free with rich industry experience and strong partnership networks.

As an SEO optimization expert, the metadata you write should meet the following advantages:
[
## Meta Title reference points (maximum 60 characters):
Meta Title must ncorporate airport name, primary keyword, and brand 
Write naturally for search engine users, avoiding excessive keyword stuffing
Meta Title content should be specific, concise, keeping length within 60 characters
Mention at least once the most competitive keyword, placing it at the front of the title
Avoid repeating the same Meta Title
Can include brand name at the end
Try to use numbers (2025, 7 methods, 8 steps, etc.)

## Meta Description reference points (maximum 160 characters):
Meta Description keyword-rich summary highlighting user intent 
Meta Description length should be kept within 120-160 characters
Mention the most competitive keyword 1-2 times
Use more verbs and clear calls to action
Try to make Meta Description appear unique in search results


## HTML meta tags:
Canonical tags, URL Slug (concise, keyword-based,Should follow a clean, descriptive format)


## Title tags:
Title tags have very important impact on SEO optimization, usually used to embed keywords and long-tail keywords, so search engines know which keywords your webpage content relates to. Weight decreases by numerical order, H1 has the highest weight, H6 the lowest, and so on. 

## FAQ posts, based on article content to propose questions and answers:
Focus on content layout: Titles should be concise and clear while containing keywords. Categorize based on FAQ content, questions and answers should be well organized
Question and answer design: Questions should be targeted, answers should be detailed and specific, maintaining objectivity
Keyword optimization strategy: Using long-tail keywords can improve article precision and attract more precise traffic, keyword density should not be too high, keeping 2%-3% is appropriate
]

Workflow:
1. Completely discard the article title and article headings from the original airport data; H1-H3 all need to be redesigned
2. Read through the entire article, identify what you think can most attract readers, design titles that can satisfy reader curiosity and align with article positioning
3. Must first design headings about the airport's basic introduction and Technical Information:
   - Basic introduction should include: airport overview, geographical location, host city, local culture and customs, etc. (avoid too many sub-headings )
   - Technical Information should include: IATA, ICAO, runway length, Aircraft Supported, and recent operational status
   - Naturally integrate keywords into these headings
4. After basic introduction, you can append headings such as route or aircraft type analysis, comparisons with other airports, localized regional content, etc., and select appropriate keywords to naturally integrate into them
5. FAQ design also needs to revolve around hot topics or trending themes
6. Add appropriate annotations within each Heading to describe the suggested content for that heading, and clearly mark that these are annotations, not body text
   - For example, Technical Information can be clearly presented using bullet points rather than descriptive sentences
   - For example, route information, common aircraft types, rankings, and other data can be introduced in simple tables for intuitive illustration

Important notes:
-The Article title (H1 title) needs to be related to the airport name, embody the main theme of the article ,and must under 60 characters, and possess an artistic flair
-Note that the focus is not reporting, but naturally integrating keywords into your article headings to attract readers
-Article length should not be too long, titles should not be excessive, expect final article 1500 words, can discard some headings based on content: too low importance, too low relevance, low attractiveness, too technical

Input:
airports: {0}
original airport data : {1}
keywords:{2}

Output:
Integrate keywords into HTML meta tags based on ideas mentioned in original airport data, please output Meta Title (less than 60 characters), Meta Description (less than 160 characters), URL Slug, Titles (including H1-H3 for article content, and H2 FAQ section containing 2-3 questions and answers as H3 sections, remove Q, A identifiers)"""




seo_rewrite_prompt = """
# Role: Human Private Jet Website Article Editor
Output Language: English

## Main Task
Completely rewrite airport data according to the provided SEO format, forming website articles with human editorial characteristics. And improve the article's readability since your article's target audience is ordinary non-professionals, and the sentence difficulty should be at a Grade 6–8 reading level that can be read fluently.

## Workflow
1. Carefully read and understand the core information and viewpoints in original airport data, organize scattered knowledge points into complete coherent articles.
2. Completely discard the article title and article headings from the original airport data
3. Follow the provided SEO format and start rewriting and expanding more content as a real human author:
   - Use reasonable logic to connect scattered keywords, editing them into complete coherent articles
   - The article style should lean towards commercial marketing SEO content, avoiding academic reports and encyclopedia-style professional writing
   - Avoid using too many long complex sentences. Use simple sentences, structured data or tables , or clear bullet points for better readability and credibility.
   - Follow the header regulations in the format and naturally integrate keywords into the article,Ensure keywords appear within the first 100 words, with an overall density of 1-1.5%, and avoid keyword stuffing.
4. Review the article's paragraphs, sentences, and words to improve readability
    - Reading difficulty should meet a 11-14 year old reading level for fluent reading
    - Avoid using obscure words and reduce the frequency of multi-syllable words. Simplify or define industry terms, and add annotations or vivid explanations when terms are first encountered
    - Sentence length should not be too long; avoid complex sentences with more than 25 words
    - Paragraphs should not contain too many sentences; average 2-4 sentences per paragraph, with content divided into chunks for easy reading
5. Control the main text output to 800-1500 words, FAQ Post is not counted in the main text

## Important Notes
- Use third-person perspective or third-person narration in writing 
- Avoid overly long sentences, use simple sentences, words, and examples to improve readability and lower the reading barrier of the article.
- Do not mention other suppliers and airline names (if involved, you may mention airports, aircraft, and aircraft manufacturer names)


## Output Format
Directly output the written article, retain without any explanation or annotation. The final output should include: HTML Meta Tags (include Meta Title, Meta Description, URL Slug, Header), written article

## Initialization
Please write this content as a real human website article editor.
original airport data: {0}
keywords:{2}
SEO strategy format: {1}
"""


seo_link="""
# Role: Human Private Jet Website Article Editor
Output Language: English
## Main Task
Task1: As a JETBAY website editor, you need to read the currently written article, analyze the article's logical flow and structure, make only minor modifications, naturally integrate JETBAY company descriptions and article links into the original article, and appropriately reduce the appearance frequency of other competing business jet charter companies.
Task2: The written article is one of the SEO cluster articles. You need to add natural internal linking architecture between Pillar articles and Content articles, ensuring that after linking, the current article structure remains complete and the language meaning unchanged.
## Workflow
1. Carefully read and understand the core information and viewpoints of the article, identify which segments can naturally integrate JETBAY company information
2. As a jetbay article editor, if the article involves relevant content, naturally insert JETBAY's business scope, brand positioning, market demands, etc., but must not conflict with the original article. Also reduce mentions of other competing business jet charter companies
  - Entry points must be natural, not contradicting the original article, do not force insertions of descriptions. If there are no suitable integration points in the entire article, you may choose not to insert descriptions
  - Modifications should be minimal, do not damage the original article structure
4.Determine whether the current article is a pillar article or content article, and establish natural internal linking
  - If it's a Pillar article, it should link to all related Content articles, naturally inserting links to sub-topic articles in relevant paragraphs, using descriptive anchor text that includes target keywords
  - If it's a content article, each Content article should link back to the main Pillar article, naturally mentioning the main topic at the beginning or end of the article
  - ross-linking: Content articles can also link to each other when content is related or complementary, avoid over-linking and maintain naturalness
  - Currently use article titles for linking, link format: [@@@HERE IS LINK:<linked article title>@@@]
3. Review the modified article to ensure the integrity of the original article structure and that no content is lost

## Important Notes
- Entry points must be natural, control integration frequency not too high, 1-3 times.
- Reduce the frequency of competitor company appearances,but can not change the original viewpoints
- Cannot modify any original article structure, cannot significantly add or delete original article content
- Use active voice to introduce company content (e.g., JETBAY ...)

## Output Format
Directly output the written article, retain without any explanation or annotation. The final output should include all original parts: HTML Meta Tags (include Meta Title, Meta Description, URL Slug, Header), written article

# Initialization
Please refer to relevant materials and complete your advertising integration task
Company Description: JETBAY is a global private jet booking platform headquartered in Singapore, with 6 branches worldwide, committed to providing excellent global services. It provides fast, competitive and seamless booking experiences, connecting over 10,000 private jets and various aircraft fleets globally, bringing excellent service to customers. 24/7 aircraft availability without the burden of purchasing, with highly competitive prices. The AI team has mastered the global private jet operation database, can intelligently match optimal flight resources, reduce empty flights, and provide optimal charter solutions. JETBAY's mobile charter team has developed an AI platform that deeply integrates with databases, uses big data to optimize charter resources, and achieves efficient, convenient, and sustainable flight experiences. Our charter service team has over 20 years of rich experience, providing top-tier, cost-effective flight solutions 24/7, ensuring customers enjoy seamless and personalized charter experiences. Our operational support team pays attention to every detail with the highest standards, and with rich industry experience and strong cooperation networks, ensures your private flight is smooth and worry-free.
JETBAY links:
| Category        | Link                                             | Keywords / Grouping               | Path                          |
|-----------------|--------------------------------------------------|-----------------------------------|-------------------------------|
| Home Page       | https://www.jet-bay.com                          | TBC                               | -                             |
| Jet Card        | https://www.jet-bay.com/jet-card                 | JetCard, Private Jet Ownership    | -                             |
| Empty Leg       | https://www.jet-bay.com/empty-leg                | Empty Leg, Empty Leg Flights      | -                             |
| Product Page    | https://www.jet-bay.com/services                 | Private Jet Rental                | /services                     |
| Product Page    | https://www.jet-bay.com/services/private-jet-charter | Private Jet                   | /services/private-jet-charter |
| Product Page    | https://www.jet-bay.com/services/group-air-charter   | Group                         | /services/group-air-charter   |
| Product Page    | https://www.jet-bay.com/services/corporate-air-charter | Business                   | /services/corporate-air-charter |
| Product Page    | https://www.jet-bay.com/services/air-ambulance   | Air Ambulance                     | /services/air-ambulance       |
| Product Page    | https://www.jet-bay.com/services/pet-travel/     | Pet Travel                        | /services/pet-travel          |
| Product Page    | https://www.jet-bay.com/services/event-charter/  | Event                             | /services/event-charter       |
| Destination     | https://www.jet-bay.com/destination/             | Destination                       | /destination                  |
| News            | https://www.jet-bay.com/news/                     | News                              | /news                         |
| Booking Process | https://www.jet-bay.com/charter-guide/booking-process | Booking                    | -                             |
| About Us        | https://www.jet-bay.com/about-us                  | About Us                          | /about-us                     |

original article:{0}
"""



def query_gpt_model(prompt: str, article: str, api_key: str=claude_key, base_url: str = "https://api.anthropic.com/v1", 
                   model: str = "claude-sonnet-4-20250514", max_tokens: int = 10240, 
                   temperature: float = 0.0,json_schema: dict = None) -> Optional[str]:
  
    url = f"{base_url}/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": f"{prompt}\n \n{article}"}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    if json_schema:
        payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": f"{prompt} + directlt output results in this json formate without explannation {str(json_schema)}\n \n{article}"}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_json = response.json()
        time.sleep(30)
        if "content" in response_json and len(response_json["content"]) > 0:
            text_content = response_json["content"][0]["text"]
            json_match = re.search(r'```(?:json)?\s*\n(.*?)\n```', text_content, re.DOTALL)
            json_text = ""
            if json_match:
                json_text = json_match.group(1)
                json_text = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', json_text)
            else:
                json_text = text_content  
                json_text = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', json_text)
            return json_text
        else:
            print("API返回内容格式异常")
            return None
    except requests.exceptions.RequestException as e:
        print(f"API请求异常: {e}")
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            print(f"API错误响应: {e.response.text}")
        return None

