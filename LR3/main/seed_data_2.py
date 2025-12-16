import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from models import User, Address, Product, Order


async def seed_additional_data():
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:1@localhost:5433/lr3-db")
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()

        descriptions = [
            "Любит кофе и программирование",
            "Дизайнер из Лос-Анджелеса",
            "Инженер-строитель",
            "Учитель испанского",
            "Студент Пекинского университета"
        ]

        for i, user in enumerate(users):
            if i < len(descriptions):
                user.description = descriptions[i]

        await session.commit()

        products_data = [
            {"name": "Клавиатура", "price": 599.99, "description": "Клава с подсветкой"},
            {"name": "Книга", "price": 889.50, "description": "Крутая книга"},
            {"name": "Наушники", "price": 3499.00, "description": "Шумоподавление"},
            {"name": "Футболка с берсерком", "price": 1122.00, "description": "Хлопок, размер XL"},
            {"name": "Мышка", "price": 12999.00, "description": "Крутая"},
        ]

        products = []
        for data in products_data:
            product = Product(name=data["name"], price=data["price"], description=data["description"])
            session.add(product)
            products.append(product)

        await session.commit()

        addresses_result = await session.execute(select(Address))
        addresses = addresses_result.scalars().all()

        for i in range(5):
            if i < len(users) and i < len(addresses) and i < len(products):
                order = Order(
                    user_id=users[i].id,
                    address_id=addresses[i].id,
                    product_id=products[i].id,
                    quantity=1,
                    status="pending"
                )
                session.add(order)

        await session.commit()
        print("Дополнительные данные добавлены!")


if __name__ == "__main__":
    asyncio.run(seed_additional_data())