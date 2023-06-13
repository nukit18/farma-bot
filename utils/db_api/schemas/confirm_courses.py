from sqlalchemy import Column, BigInteger, sql, Time, Boolean

from utils.db_api.db_gino import TimedBaseModel


class Confirm_course(TimedBaseModel):
    __tablename__ = 'confirm_courses'
    id_course = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    time_notify = Column(Time)
    last = Column(Boolean)

    query: sql.Select