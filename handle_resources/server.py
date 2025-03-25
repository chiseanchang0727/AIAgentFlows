from mcp.server import Server, FastMCP
from datetime import datetime
import mcp.types as types
mcp = FastMCP(
    name="resources-test",
    version="1.0.0",
    
)


@mcp.resource("hello://World")
def get_hello_msg() -> str:
    return "Hello, World!"



@mcp.resource("timereport://current")
def get_current_time() -> str:
    return f"Current time is: {datetime.now().strftime('%Y-%m-%d %H:%M')}"



# @mcp.resource("list://rescoures")
# def list_rescources() -> dict:
#     return {
#         "resources": [
#             {
#                 "uri": "hello://World",
#                 "name": "hello msg.",
#                 "mimeType": "text/plain"
#             },
#             {
#                 "uri": "timereport://current",
#                 "name": "report current time",
#                 "mimeType": "text/plain"
#             }
#         ]
#     }



@mcp.list_resources()
def list_resources() -> list[types.Resource]:
    return [
        types.Resource({
            "uri": "hello://World",
            "name": "hello msg.",
            "mimeType": "text/plain"
        })
    ]

