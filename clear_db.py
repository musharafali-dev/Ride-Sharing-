import asyncio
import dotenv
from sqlalchemy import text
from app.infrastructure.database.session import async_session_maker

async def clear_db():
    async with async_session_maker() as session:
        await session.execute(text('DROP SCHEMA public CASCADE; CREATE SCHEMA public;'))
        await session.commit()
        print("Database truncated!")

if __name__ == "__main__":
    dotenv.load_dotenv()
    asyncio.run(clear_db())
