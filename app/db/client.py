from motor.motor_asyncio import AsyncIOMotorClient
from app.core.settings import MONGO_URL, MONGO_MAX_CONNECTIONS

class Database:
    client: AsyncIOMotorClient = None


db = Database()


async def get_db() -> AsyncIOMotorClient:
    print("GET DB", db.client)
    if not db.client:
        print("CONNECT")
        await db_connect()
    return db.client


async def db_connect():
    """
    Connect to MONGO DB
    """
    print("DB CONNECT")
    db.client = AsyncIOMotorClient(MONGO_URL,
                                   maxPoolSize=MONGO_MAX_CONNECTIONS)
    print(f"Connected to mongo at {MONGO_URL}")


async def db_close():
    """
    Close MongoDB Connection
    """
    db.client.close()
    print("Closed connection with MongoDB")