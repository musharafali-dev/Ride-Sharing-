import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def reset():
    conn = await asyncpg.connect("postgresql://postgres:postgres@localhost:5433/postgres")
    
    await conn.execute("""
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = 'ridesharing'
        AND pid <> pg_backend_pid();
    """)
    
    await conn.execute("DROP DATABASE IF EXISTS ridesharing")
    await conn.execute("CREATE DATABASE ridesharing")
    
    await conn.close()
    print("Database recreated!")

if __name__ == "__main__":
    asyncio.run(reset())
