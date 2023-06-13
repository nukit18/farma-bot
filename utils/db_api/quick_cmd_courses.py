from asyncpg import UniqueViolationError
from datetime import date, timedelta

from utils.db_api.db_gino import db
from utils.db_api.schemas.course import Course


async def add_course(user_id: int, name_medicine: str, dose: str, times: [], duration: int):
    try:
        course = Course(user_id=user_id, name_medicine=name_medicine, dose=dose, times=times, duration=date.today() + timedelta(days=duration))
        await course.create()

    except UniqueViolationError:
        pass


async def select_all_courses():
    courses = await Course.query.gino.all()
    return courses


async def select_courses_user(user_id: int):
    courses = await Course.query.where(Course.user_id == user_id).gino.all()
    return courses


async def select_course(id: int):
    course = await Course.query.where(Course.id == id).gino.first()
    return course


async def select_courses_user_count(user_id: int):
    courses = await Course.query.where(Course.user_id == user_id).gino.all()
    return len(courses)


async def delete_course(id_course: int):
    course = await Course.get(id_course)
    await course.delete()


async def delete_all_courses_user(user_id: int):
    courses = await Course.query.where(Course.user_id == user_id).gino.all()
    for course in courses:
        await delete_course(course.id_course)


