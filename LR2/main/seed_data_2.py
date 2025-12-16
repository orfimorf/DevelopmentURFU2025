from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Address, Product, Order
import uuid

connect_url = "postgresql://postgres:1@localhost:5433/lr2-base"
engine = create_engine(connect_url, echo=False)
session_factory = sessionmaker(bind=engine)

with session_factory() as session:
    users = session.query(User).all()
    descriptions = [
        "Любит кофе и программирование",
        "Дизайнер из Лос-Анджелеса",
        "Инженер-строитель",
        "Учитель испанского",
        "Студент Пекинского университета"
    ]
    for i, user in enumerate(users):
        user.description = descriptions[i]
    session.commit()

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
    session.commit()

    addresses = session.query(Address).all()
    for i in range(5):
        order = Order(
            user_id=users[i].id,
            address_id=addresses[i].id,
            product_id=products[i].id,
            quantity=1,
            status="pending"
        )
        session.add(order)
    session.commit()
