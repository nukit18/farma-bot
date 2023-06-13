from sqlalchemy import Column, BigInteger, String, sql, Integer, Time, Date
from sqlalchemy.dialects import postgresql

from utils.db_api.db_gino import TimedBaseModel


class Course(TimedBaseModel):
    __tablename__ = 'courses'
    id_course = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    name_medicine = Column(String(100))
    dose = Column(String(100))
    times = Column(postgresql.ARRAY(Time))
    duration = Column(Date)

    query: sql.Select