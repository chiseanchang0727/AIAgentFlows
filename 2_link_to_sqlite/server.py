import logging
from mcp.server import FastMCP
import aiosqlite

# test with `mcp dev server.py`

mcp = FastMCP("sqlite")


@mcp.resource("db://localdb")
async def link_to_sqlite():
    dbpath = 'local_db.db'
    async with aiosqlite.connect(dbpath) as conn:
        cursor = await conn.execute("SELECT * FROM users")
        columns = [column[0] for column in cursor.description]
        rows = await cursor.fetchall()
        await cursor.close()

        # Convert to list of dicts for better structure
        result = [dict(zip(columns, row)) for row in rows]
        return result
