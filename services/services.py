import asyncio

from aiohttp import ClientSession, StreamReader
from bs4 import BeautifulSoup as bs
from bs4 import ResultSet, Tag
from fake_useragent import UserAgent
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import async_session_maker
from database.db import BotDB
from model.models import Task


async def get_data(task_data, topics):
    number: Tag = task_data.find('td', {'class': 'id'}).find('a')
    link: str = 'https://codeforces.com/' + number.get('href')
    title: str = task_data.find('div', {'style': 'float: left;'}).find('a').text.strip()
    text_topics: list = [tp.text for tp in task_data.find_all('a', {'class': 'notice'})]
    task_topics: list = [tp for tp in topics if tp.title in text_topics]
    difficulty: Tag = task_data.find('span', {'title': 'Сложность'})
    if difficulty:
        difficulty = int(difficulty.text.strip())
    number_solved: Tag = task_data.find('a', {'title': 'Количество решивших задачу'})
    if number_solved:
        number_solved = int(number_solved.text[2:])
    task = Task(number=number.text.strip(), title=title, number_solved=number_solved, difficulty=difficulty,
                link=link)
    task.topics.extend(task_topics)
    return task, number.text.strip()


async def get_html_code(url: str):
    async with ClientSession() as session:
        async with session.get(url=url, headers={'User-Agent': UserAgent().random}) as response:
            page = await StreamReader.read(response.content)
            soup: bs = bs(page, 'html.parser')
            return soup


async def add_topics_in_db(topics_tag: list):
    """Добавляем все темы задач в бд"""
    topics_text = [{'title': topic.text.strip()} for topic in topics_tag]
    await BotDB.add_topic(topics_text[2:])


async def number_pages():
    """Находим количество страниц и добавляем темы в базу"""
    soup = await get_html_code('https://codeforces.com/problemset/?order=BY_SOLVED_DESC&locale=ru')
    quantity_search: list = soup.find('div', {'class': 'pagination'}).find_all('a')
    quantity_pages: str = quantity_search[-2].text
    topics_tag: list = soup.find('label', {'class': '_FilterByTagsFrame_addTagLabel'}).find_all('option')
    await add_topics_in_db(topics_tag)
    return int(quantity_pages) + 1


async def parsing_once_an_hour(number: int, topics: tuple, session: AsyncSession):
    soup = await get_html_code(f'https://codeforces.com/problemset/page/{number}?order=BY_SOLVED_DESC&locale=ru')
    tasks: ResultSet = soup.find('table', {'class': 'problems'}).find_all('tr')
    lt: list = []
    numbers: dict = dict()
    for task in tasks[1:]:
        task, number = await get_data(task, topics)
        lt.append(task)
        numbers[number] = {'difficulty': task.difficulty, 'number_solved': task.number_solved}
    await BotDB.add_or_update_task(lt, numbers, session)


async def starting_update():
    """Запускаем парсинг"""
    quantity_pages: int = await number_pages()
    topics: tuple = await BotDB.all_topics()
    tasks: list = []
    try:
        async with async_session_maker() as session:
            for i in range(1, quantity_pages+1):
                tasks.append(parsing_once_an_hour(i, topics, session))
            await asyncio.gather(*tasks)
            await session.commit()
    except Exception as e:
        await session.rollback()
        print('Ошибка: ', e)


async def info_about_tasks(tasks: list) -> str and list:
    """Находим информацию о задачах в списке"""
    info = ''
    links = []
    for task in tasks:
        info += f'Номер задачи: {task.number}\n' \
                f'Название: {task.title}\n' \
                f'Количество решивших: {task.number_solved}\n' \
                f'Сложность: {task.difficulty}\n' \
                f'Тема/ы: {", ".join([x.title for x in task.topics])}\n\n'
        links.append((task.title, task.link,))
    return info, links
