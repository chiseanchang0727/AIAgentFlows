from typing import Literal
from pydantic import BaseModel
from pydantic_extra_types.timezone_name import TimeZoneName
from openai import OpenAI
from mcp.server import FastMCP
import os
import logging
from dotenv import load_dotenv

# === Load environment ===
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# === Setup logging ===
logger = logging.getLogger("web_search")
logger.setLevel(logging.DEBUG)
logger.propagate = False 

handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# === Start MCP App ===
app = FastMCP('web-search')
logger.info("FastMCP 'web-search' app initialized.")

# === Pydantic Model ===
class UserLocation(BaseModel):
    type: Literal["approximate"] = "approximate"
    city: str
    country: str = None
    region: str = None
    timezone: TimeZoneName

# === Web Search Tool ===
@app.tool()
def web_search(
    input: str,
    model: Literal['gpt-4o', 'gpt-4o-mini'] = 'gpt-4o-mini',
    type: Literal['web_search_preview', 'web_search_preview_2025_03_11'] = 'web_search_preview',
    search_context_size: Literal["low", "medium", "high"] = 'medium',
    user_location: UserLocation = None
) -> list[str]:
    logger.info(f"web_search called with input: {input}")
    logger.debug(f"model={model}, type={type}, search_context_size={search_context_size}, user_location={user_location}")

    try:
        client = OpenAI(api_key=openai_api_key)

        response = client.responses.create(
            model=model,
            tools=[
                {
                    "type": type,
                    "search_context_size": search_context_size,
                    "user_location": user_location.model_dump() if user_location else None
                }
            ],
            input=input
        )

        logger.info("OpenAI response successfully received.")
        return response.output_text
    except Exception as e:
        logger.exception("Error occurred during web_search execution.")
        return [f"An error occurred: {str(e)}"]

if __name__ == "__main__":
    logger.info("Running FastMCP app...")
    app.run(transport='stdio')