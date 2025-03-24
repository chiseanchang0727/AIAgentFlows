import logging
from pydantic import AnyUrl
from mcp.server import Server
import mcp.types as types
import sqlite3


logger = logging.getLogger('mcp_sqlite_server')
logger.info("Starting MCP SQLite Server")

# @mcp.tool()
# def add(a:int, b:int) -> int:
#     return a + b

# @mcp.tool()
# def calculate_bmi(weight_kg: float, height_m: float) -> float:
#     """Calculate BMI given weight in kg and height in meters"""
#     return weight_kg / (height_m ** 2)


async def main():

    db_path = 'localdb.db'
    
    db = sqlite3.connect(db_path)

    server = Server("sqlite-manager")

    logger.debug("Connect to localdb")

    @server.list_resources()
    async def handle_list_resouce() -> list[types.Resource]:

        return [
            types.Resource(
                uri=AnyUrl("memo://insights"),
                name="Test",
                description="Test db",
                mimeType='text/plain'
            )
        ]