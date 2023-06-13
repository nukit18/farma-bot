from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.user import User


async def add_user(user_id: int, fullname: str, sex: str, age: int, weight: int):
    try:
        user = User(user_id=user_id, fullname=fullname, sex=sex, age=age, weight=weight, active=True)
        await user.create()

    except UniqueViolationError:
        pass


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_user(id: int):
    user = await User.query.where(User.user_id == id).gino.first()
    return user


async def off_user(id: int):
    user = await User.get(id)
    await user.update(active=False).apply()


async def on_user(id: int):
    user = await User.get(id)
    await user.update(active=True).apply()