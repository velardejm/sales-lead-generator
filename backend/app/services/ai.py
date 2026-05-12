import json
from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_brief(search_results):
    formatted = "\n".join([f"{r['title']}: {r['snippet']}" for r in search_results])

    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """You are a sales research assistant for QTIC (Qatar Technical International Metal Industries).

QTIC services: TSA coating, sandblasting, painting, structural steel fabrication, 
CNC cutting, machining, in-situ repair and maintenance.

Ideal clients: oil and gas operators, heavy construction, marine, industrial facilities 
with aging equipment needing corrosion protection or structural repair.

Given search results about a company, return a JSON object with exactly these fields:
- summary: what the company does (2-3 sentences)
- service_angle: which QTIC service to lead with and why (1-2 sentences)
- buying_signal: any recent activity worth mentioning (1 sentence, or null if none)
- data_quality: "rich" if you have enough to work with, "limited" if the data was thin
- contact_info: any phone numbers, emails, or contact details found in the search results (1-2 lines, or null if none found)"""
            },
            {
                "role": "user",
                "content": f"Research results:\n{formatted}"
            }
        ]
    )

    return json.loads(response.choices[0].message.content)


def detect_buying_signal(news_results):
    formatted = "\n".join([f"{r['title']}: {r['snippet']}" for r in news_results])

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """You are a buying signal detector for QTIC, a repair, maintenance, 
fabrication and coating company in Qatar.

Given recent news about a company, determine if there is a buying signal — 
any activity suggesting they might need industrial repair, maintenance, 
fabrication, coating, or corrosion protection services.

Return a JSON object with exactly these fields:
- signal_detected: true or false
- reason: one sentence explaining why, or null if no signal"""
            },
            {
                "role": "user",
                "content": f"Recent news:\n{formatted}"
            }
        ]
    )

    return json.loads(response.choices[0].message.content)