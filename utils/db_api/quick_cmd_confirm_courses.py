from asyncpg import UniqueViolationError
from datetime import date, timedelta, datetime

from utils.db_api.db_gino import db
from utils.db_api.schemas.confirm_courses import Confirm_course


async def add_confirm_course(id_course: int, user_id: int, delta_time_notify: int, last: bool = False):
    try:
        confirm_course = Confirm_course(id_course=id_course, user_id=user_id, time_notify=datetime.now() + timedelta(minutes=delta_time_notify),
                                        last=last)
        await confirm_course.create()

    except UniqueViolationError:
        pass


async def select_all_confirm_courses():
    confirm_courses = await Confirm_course.query.gino.all()
    return confirm_courses


async def select_confirm_course(id_course: int):
    confirm_course = await Confirm_course.query.where(Confirm_course.id_course == id_course).gino.first()
    return confirm_course


async def update_time(id_course: int, delta_time_notify: int):
    confirm_course = await Confirm_course.get(id_course)
    old_time_notify = str(confirm_course.time_notify).split(":")
    time_notify = datetime.strptime(old_time_notify[0]+":"+old_time_notify[1], "%H:%M")
    print(time_notify + timedelta(minutes=delta_time_notify))
    await confirm_course.update(time_notify=time_notify + timedelta(minutes=delta_time_notify)).apply()


async def delete_confirm_course(id_course: int):
    confirm_course = await Confirm_course.get(id_course)
    await confirm_course.delete()


async def delete_all_courses_user(user_id: int):
    courses = await Confirm_course.query.where(Confirm_course.user_id == user_id).gino.all()
    for course in courses:
        await delete_confirm_course(course.id_course)

