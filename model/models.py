from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.base import Base

task_topic = Table(
    'task_topic',
    Base.metadata,
    Column('task_id', ForeignKey('task.id'), primary_key=True),
    Column('topic_id', ForeignKey('topic.id'), primary_key=True),
)


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=True)
    number: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    number_solved: Mapped[str] = mapped_column(Integer, nullable=True, default=0)
    difficulty: Mapped[str] = mapped_column(Integer, nullable=True)
    link: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    topics: Mapped[list['Topic']] = relationship(secondary=task_topic)

    def __repr__(self):
        return f'Task(id={self.id}, title={self.title}, number={self.number})'


class Topic(Base):
    __tablename__ = 'topic'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(250), nullable=True, unique=True)

    def __repr__(self):
        return f'Topic(id={self.id}, title={self.title})'


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    tg_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)

    def __repr__(self):
        return f'User(id={self.id}, title={self.tg_id})'
