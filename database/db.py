from sqlalchemy import Select, select
from sqlalchemy.dialects.postgresql import Insert, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.connection import async_session_maker
from model.models import Task, Topic, User, task_topic


class BotDB:

    @staticmethod
    async def check_user_in_db(user_id: int) -> None:
        """Проверяем есть ли пользователь в базе, если нет то добавляем"""
        async with async_session_maker() as session:
            stmt: Insert = insert(User).values({'tg_id': user_id}).on_conflict_do_nothing(index_elements=['tg_id'])
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def all_difficulties():
        """Отдаёт список всех доступных сложностей"""
        async with async_session_maker() as session:
            query: Select = select(Task.difficulty).distinct().order_by(Task.difficulty)
            result = await session.scalars(query)
        return result.all()

    @staticmethod
    async def all_topics_name():
        """Отдаёт список всех доступных тем"""
        async with async_session_maker() as session:
            query: Select = select(Topic.title).order_by(Topic.title)
            result = await session.scalars(query)
        return result.all()

    @staticmethod
    async def all_topics():
        """Отдаёт список объектов тем"""
        async with async_session_maker() as session:
            query: Select = select(Topic)
            result = await session.scalars(query)
        return result.all()

    @staticmethod
    async def search_name_task_in_db(name: str) -> list:
        """Ищем задачу по названию или номеру"""
        async with async_session_maker() as session:
            query: Select = select(Task).filter((Task.title == name) | (Task.number == name)).options(
                selectinload(Task.topics).load_only(Topic.title))
            result = await session.scalars(query)
        return result.all()

    @staticmethod
    async def list_tasks(parameters: dict, tg_id: int) -> list:
        """Ищет задачи по выбранным параметрам и отдаёт список из 10 найденных"""
        difficulty: str = parameters['difficulty']
        async with async_session_maker() as session:
            query: Select = select(Task).join(task_topic).join_from(task_topic, Topic).filter(
                Task.difficulty == int(difficulty),
                Topic.title.in_((parameters.values()))).options(
                selectinload(Task.topics)).limit(10)
            result = await session.scalars(query)
        return result.all()

    @staticmethod
    async def add_or_update_task(tasks: list, numbers: dict, session: AsyncSession):
        """Добавляем данные и обновляет данные задач в бд"""
        query_task: Select = select(Task).where(Task.number.in_(numbers))
        result_select = await session.scalars(query_task)
        query_task_number: Select = select(Task.number).where(Task.number.in_(numbers))
        result_number = await session.scalars(query_task_number)
        ui = set(result_number.all())
        prom: set = set(numbers.keys()) - ui
        t = [x for x in tasks if x.number in prom]
        if t:
            session.add_all(t)
        for x in result_select.all():
            x.difficulty = numbers[x.number]['difficulty']
            x.number_solved = numbers[x.number]['number_solved']

    @staticmethod
    async def add_task(tasks: list):
        async with async_session_maker() as session:
            session.add_all(tasks)
            await session.commit()

    @staticmethod
    async def add_topic(topics: list):
        """Добавляем темы в бд"""
        async with async_session_maker() as session:
            stmt: Insert = insert(Topic).values(topics).on_conflict_do_nothing(index_elements=['title'])
            await session.execute(stmt)
            await session.commit()
