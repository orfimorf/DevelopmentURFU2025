from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Address
import uuid

connect_url = "postgresql://postgres:1@localhost:5433/lr2-base"

engine = create_engine(connect_url, echo=True)

session_factory = sessionmaker(bind=engine)

with session_factory() as session:
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

    session.commit()

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

    session.commit()