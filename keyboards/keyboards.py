from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from database.db import BotDB


async def create_difficulty_list() -> InlineKeyboardBuilder:
    """Создание инлайн-кнопок для выбора сложности"""
    difficulty_kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    list_difficulties: list = await BotDB.all_difficulties()
    difficulty_buttons: list = []
    for df in list_difficulties[:-1]:
        difficulty_buttons.append(InlineKeyboardButton(text=df, callback_data=df))
    difficulty_kb.row(*difficulty_buttons, width=3)
    difficulty_kb.row(InlineKeyboardButton(text='Без сложности', callback_data=0), width=1)
    return difficulty_kb


async def create_topic_list() -> InlineKeyboardBuilder:
    """Создание инлайн-кнопок для выбора темы задачи"""
    topic_kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    list_topic: list = await BotDB.all_topics_name()
    topics_buttons: list = []
    for tp in list_topic:
        topics_buttons.append(InlineKeyboardButton(text=tp, callback_data=tp))
    topic_kb.row(*topics_buttons, width=1)
    return topic_kb


async def starting_action() -> InlineKeyboardBuilder:
    """Кнопки для выбора первого действия после старта"""
    action: InlineKeyboardBuilder = InlineKeyboardBuilder()
    action.row(InlineKeyboardButton(text='Выбрать сложность и тему/темы', callback_data='choice'),
               InlineKeyboardButton(text='Поиск задачи по названию или номеру', callback_data='search'), width=1)
    return action


async def create_keyboard_yes_or_not() -> InlineKeyboardBuilder:
    """Кнопки да или нет для выбора доп темы"""
    keyboard_yes_or_not: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard_yes_or_not.row(InlineKeyboardButton(text='Да', callback_data='yes'),
                            InlineKeyboardButton(text='Нет', callback_data='no'))
    return keyboard_yes_or_not


async def create_keyboard_name_and_number() -> InlineKeyboardBuilder:
    """Создаём инлайн кнопки для выбора поиска по названию ил номеру задачи"""
    keyboard_name_and_number: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard_name_and_number.row(InlineKeyboardButton(text='Названию', callback_data='name'),
                                 InlineKeyboardButton(text='Номеру', callback_data='number'), width=1)
    return keyboard_name_and_number


async def create_tasks_url(links: list) -> InlineKeyboardBuilder:
    """Создаём инлайн кнопки ссылками на задачу"""
    tasks_kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    tasks_buttons: list = []
    for link in links:
        tasks_buttons.append(InlineKeyboardButton(text=link[0], url=link[1]))
    tasks_kb.row(*tasks_buttons, width=1)
    return tasks_kb
