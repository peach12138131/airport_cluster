import requests
import json
from datetime import datetime
import os
import random
from typing import List, Dict, Any, Optional,Generator
from collections import defaultdict
import time
import re




# airport_data = {
#     "US": ["KTEB", "KDAL", "KPBI", "KHPN", "KVNY", "KIAD", "KLAS", "KOPF", "KPDK", "KSDL"],
#     "CA": ["CYYZ", "CYYC", "CYUL", "CYVR", "CYWG", "CYHU", "CYEG", "CYLW", "CYQB", "CYXE"],
#     "UK": ["EGLF", "EGGW", "EGKB", "EGSS", "EGTK", "EGWU", "EGJJ", "EGCC", "EGNX", "EGBB"]
# }
airport_data = {
    "US": ["KIAD"],
    "UK": ["EGNX", "EGBB"]
}
   




keywords_designer_prompt = """
Output language:English
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

### Keyword Distribution Framework (Flexible Guideline):
Aim for a balanced mix across these categories, but prioritize what naturally emerges from the content:

1. **Location-Specific Keywords (3-4 recommended)**
   - Incorporate airport names, codes, or city identifiers
   - Natural format variations welcomed:
     * private jet from [airport name]
     * private jet charter [airport name]
     * [airport name] private jet
     * [airport code] private jet flights
     * fly private to [city name]
     * [city] airport business aviation
   
2. **Service & Context Keywords (3-4 recommended)**
   - Service variations and semantic alternatives
   - Route-based combinations
   - User intent-driven phrases
   - Industry terminology that adds specificity

3. **Long-Tail Query Keywords (2-3 recommended)**
   - Typically 5+ words
   - Answer specific user questions or scenarios
   - Include concrete details (routes/prices/aircraft types when relevant)
   - Example patterns: "How much...", "Best [aircraft type] for...", "[Route] private jet cost"

**Note:** These are suggested distributions. If the article content naturally supports a different balance, prioritize keyword quality and relevance over rigid category quotas.

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

## CRITICAL RULES
**Never** create generic keywords like "private jet" or "charter flights" alone
**Always** tie keywords to specific airport/route/data mentioned in article
**Trending keywords:** Must cite specific 2025 data/trend from article
---


## INPUT VARIABLES
**Airport:** {0}
**Article Content:** {1}

---



Directly output your keywords
"""



seo_matadata="""
Output language:English
Role: As an SEO expert at a digital marketing agency. Your client has provided you with company name, service description, and keywords. Your task is to create title and meta description tags for their service pages. Your goal is to optimize pages for search engines and bring organic traffic to the website. When writing tags, keep in mind the company's target audience and brand guidelines.

**JETBAY** - Global private jet booking platform
- HQ: Singapore | 6 global branches | 10,000+ aircraft network  
- AI-powered matching | 24/7 availability | 20+ years charter expertise
- Target: UHNW individuals, C-suite executives, luxury travelers

As an SEO optimization expert, the metadata you write should meet the following advantages:

## Meta Title reference points (maximum 60 characters):
- Must include: Airport name + Primary keyword + "JETBAY"
- Add numbers when possible (2025, Top 5, etc.)

## Meta Description reference points (maximum 160 characters):
- Use primary keyword 1-2 times
- Include action verbs (Book, Compare, Discover)

## HTML meta tags:
- Format: lowercase-with-hyphens, keyword-focused


## Title tags:
- H1 = highest SEO weight, must contain main keyword
- H2/H3 = embed long-tail keywords naturally
- Keyword density: 2-3 percent across all content

**FAQ Section** (H2 with 2-3 questions as H3, no Q/A labels)
- Match common search intent, avoid overly technical topics
- Brief actionable answers, naturally integrate long-tail keywords
- Keyword density: 2-3 percent  across titles and answers



## Content Creation Workflow

### Step 1: Analyze Input
- Discard original titles/headings from airport data
- Identify most compelling angles for target audience
- Plan keyword integration strategy

### Step 2: Design Metadata

**Meta Title**
- Must include: Airport name + Primary keyword + "JETBAY"
- Add numbers when possible (2025, Top 5, etc.)

**Meta Description**
- Use primary keyword 1-2 times
- Include action verbs (Book, Compare, Discover)

**HTML Meta tag**

- Format: lowercase-with-hyphens, keyword-focused

### Step 3: Design Article Structure (Target: 1500 words)

**H1 Main Title** (≤60 characters, must include airport name)
- Format examples(flexible guidance, not rigid templates): 
    • [Airport Name]: [Topic/Benefit]
    • [Topic] at [Airport Name/Code] ([Year])
    • [Airport] [Region]: [Unique Positioning]
    • [Data Element] from/at [Airport Name]
    • [Service Type] Guide: [Airport] [Location Context]
    • [Question Format]: [Airport Name] [Topic]
- Prioritize clarity and searchability over creativity

**Required H2 Sections:**
### Add appropriate annotations within each Heading to describe the suggested content for that heading, and clearly mark that these are annotations, not body text

1. **Airport Overview & Location**
   - Geographic position, host city, cultural context
   - Keep concise, limit sub-headings (2-3 H3 max)
   [Note: Brief paragraphs, naturally integrate location keywords]

2. **Technical Information**
   - IATA/ICAO codes, runway specs, supported aircraft, operational status
   [Note: Present as bullet list, not prose]

**H2 Sections** (select 1-2 based on data quality,annotate that do not use table ):
- Popular Routes & Flight Times (5+ routes as bullets)
- Aircraft Type Recommendations
- Comparison with Regional Airports
- Local FBO Services & Amenities

**Additional H2 Sections** (2-3 sections based on keywords and content)
- Flexibly design headings that integrate target keywords naturally
- Choose topics that align with both airport_data insights and SEO strategy
[Note: Prioritize reader value and keyword relevance over rigid templates]

**H2: FAQ** (2-3 H3 questions, no Q/A labels)
- Match search intent, practical concerns only
- Brief answers with keywords, 2-3% density

### Step 3: Content Formatting Rules
- Use bullets for: technical specs, routes (5+), aircraft lists, rankings
- Omit low-value sections: too technical, low relevance, poor data

### Quality Check
- Keywords naturally integrated (not forced)
- Focus: reader value, not reporting


Input:
airports: {0}
keywords:{1}
original airport data : {2}


Output:
Integrate keywords into HTML meta tags , please output Meta Title (less than 60 characters), Meta Description (less than 160 characters), URL Slug, Titles (including H1-H3 for article content, and H2 FAQ section containing 2-3 questions and answers as H3 sections, remove Q, A identifiers)
"""




seo_rewrite_prompt = """
# Role: Human Private Jet Website Article Editor
Output Language: English

## Main Task
Completely rewrite airport data and Transform raw airport data into SEO-optimized, reader-friendly web articles targeting non-professional audiences (Grade 6-8 reading level).

## Core Requirements

### Content Style
- **Tone**: Commercial marketing (not academic reports or encyclopedic)
- **Perspective**: Third-person narration throughout
- **Reading Level**: 11-14 years old comprehension (simple vocabulary, clear structure)
- **Length**: 800-1500 words (excluding FAQ section)

### SEO Standards
- **Keyword Integration**: 
  - First mention within opening 100 words
  - Overall density: 1-1.5%
  - Natural placement (avoid stuffing)
- **Structure**: Follow provided SEO format exactly (headers, meta tags, URL slug)

### Readability Rules
- **Sentences**: Max 25 words | Prioritize simple sentences over complex
- **Paragraphs**: 2-4 sentences each | Break content into scannable chunks
- **Vocabulary**: 
  - Avoid jargon; define technical terms on first use
  - Reduce multi-syllable words
  - Use concrete examples over abstract concepts
- **Formatting**: Use bullet points and short paragraphs (not tables)

## Writing Process

**Step 1**: Analyze Input
- Extract core facts and insights from airport data
- Discard original titles/headings completely
- Identify key information gaps to address

**Step 2**: Structure Content
- Apply SEO format (H1, H2, H3 hierarchy)
- Organize scattered data into logical narrative flow
- Ensure smooth transitions between sections

**Step 3**: Write & Optimize
- Draft content as a human editor (not AI-generated tone)
- Connect keywords naturally through coherent storytelling
- Simplify complex aviation concepts for general readers

**Step 4**: Quality Check
- Verify keyword density (1-1.5%) and placement
- Check sentence length (≤25 words) and paragraph size (2-4 sentences)
- Ensure Grade 6-8 reading level compliance
- Main body length should be less than 1500 words, excluding the FAQ section

## Restrictions
-  Do NOT mention competitor names or specific airlines
-  May reference: airports, aircraft models, manufacturers
-  Do NOT include annotations like [Note: ...] in final output
-  Do NOT use tables or overly technical formatting

## Output Format
Complete article ready for publication including:
1. Meta Title (≤60 characters)
2. Meta Description (120-160 characters)
3. URL Slug
4. Rewrited article with H1-H3 headers
5. FAQ section (2-3 Q&As)

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
                   model: str = "claude-sonnet-4-5-20250929", max_tokens: int = 10240, 
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

