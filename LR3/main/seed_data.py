import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models import User, Address, Product, Order
import uuid


async def seed_initial_data():
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:1@localhost:5433/lr3-db")
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        from sqlalchemy import select
        result = await session.execute(select(User))
        existing_users = result.scalars().all()

        if existing_users:
            print(f"В базе уже есть {len(existing_users)} пользователей")
            return

        users_data = [
            {"username": "ilya", "email": "ilyae@example.com"},
            {"username": "misha", "email": "misha@example.com"},
            {"username": "lildi", "email": "lildin@example.com"},
            {"username": "artem", "email": "artem@example.com"},
            {"username": "slava", "email": "slava@example.com"},
        ]

        users = []
        for data in users_data:
            user = User(username=data["username"], email=data["email"])
            session.add(user)
            users.append(user)

        await session.commit()

        addresses_data = [
            {"user_id": users[0].id, "street": "10 street", "city": "Revda", "country": "RU"},
            {"user_id": users[1].id, "street": "20 street", "city": "Los Angeles", "country": "USA"},
            {"user_id": users[2].id, "street": "30 street", "city": "Chicago", "country": "USA"},
            {"user_id": users[3].id, "street": "40 street", "city": "Madrid", "country": "Spain"},
            {"user_id": users[4].id, "street": "50 street", "city": "Beijing", "country": "China"},
        ]

        for data in addresses_data:
            address = Address(
                user_id=data["user_id"],
                street=data["street"],
                city=data["city"],
                country=data["country"]
            )
            session.add(address)

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed_initial_data())