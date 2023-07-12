from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from prompt_manager import PromptManager
import openai
import os
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
admyrer = PromptManager()

@app.post("/generate_brief")
async def generate_brief(request_data: dict):
    brand_introduction = request_data.get("brand_introduction")
    deliverables = request_data.get("deliverables")
    social_media_platforms = request_data.get("social_media_platforms")
    budget = request_data.get("budget")
    target_audience = request_data.get("target_audience")

    print(request_data)
    prompt = admyrer.get_brief_prompt(
        brand_introduction=brand_introduction,
        deliverables=deliverables,
        social_media_platforms=social_media_platforms,
        budget=budget,
        target_audience=target_audience
    )

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Follow the below instructions and provide your response in proper markdown(.md) format."},
            {"role": "user", "content": f"{prompt}"}
        ]
    )

    return completion.choices[0].message