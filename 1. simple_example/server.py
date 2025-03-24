from mcp.server.fastmcp import FastMCP


mcp = FastMCP(name="Simple Example.")


@mcp.tool()
def add(a:int, b:int) -> int:
    return a + b

@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    return weight_kg / (height_m ** 2)