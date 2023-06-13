from sqlalchemy import Column, BigInteger, String, sql, Integer, Boolean

from utils.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    fullname = Column(String(100))
    sex = Column(String(100))
    age = Column(Integer)
    weight = Column(Integer)
    active = Column(Boolean)

    query: sql.Select