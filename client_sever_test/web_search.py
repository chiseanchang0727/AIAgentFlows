from typing import Literal
from pydantic import BaseModel
from pydantic_extra_types.timezone_name import TimeZoneName
from openai import OpenAI
from mcp.server import FastMCP
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

app = FastMCP('web-search')

print("Start web_search.py.")

class UserLocation(BaseModel):
    type: Literal["approximate"] = "approximate"
    city: str
    country: str = None
    region: str = None
    timezone: TimeZoneName

# openai web search
@app.tool()
def web_search(
    input: str,
    model: Literal['gpt-4o', 'gpt-4o-mini'] = 'gpt-4o-mini',
    type: Literal['web_search_preview', 'web_search_preview_2025_03_11'] = 'web_search_preview',
    search_context_size: Literal["low", "medium", "high"] = 'medium',
    user_location: UserLocation = None
) -> list[str]:
    
    client = OpenAI(api_key=openai_api_key)

    response = client.responses.create(
        model = model,
        tools = [
            {
                "type": type,
                "search_context_size":  search_context_size,
                "user_location": user_location.model_dump() if user_location else None
            }
        ],
        input=input
    )

    return response.output_text