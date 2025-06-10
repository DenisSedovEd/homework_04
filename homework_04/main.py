"""
Домашнее задание №4
Асинхронная работа с сетью и бд

доработайте функцию main, по вызову которой будет выполняться полный цикл программы
(добавьте туда выполнение асинхронной функции async_main):
- создание таблиц (инициализация)
- загрузка пользователей и постов
    - загрузка пользователей и постов должна выполняться конкурентно (параллельно)
      при помощи asyncio.gather (https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)
- добавление пользователей и постов в базу данных
  (используйте полученные из запроса данные, передайте их в функцию для добавления в БД)
- закрытие соединения с БД
"""

import asyncio
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from jsonplaceholder_requests import *
from models import Base, async_engine, async_session, User, Post


async def create_users(
    session: AsyncSession,
    users: list[dict],
) -> list[User]:
    result = []
    for user in users:
        user_for_add = User(
            id=user["id"],
            username=user["username"],
            name=user["name"],
            email=user["email"],
        )

        session.add(user_for_add)
        await session.commit()
        result.append(user_for_add)
    return result


async def crete_posts(
    session: AsyncSession,
    posts: list[dict],
) -> list[Post]:
    result = []
    for post in posts:
        session.add(
            Post(
                id=post["id"],
                title=post["title"],
                body=post["body"],
                user_id=post["userId"],
            )
        )
        await session.commit()
        result.append(Post())
    return result


async def get_user(
    session: AsyncSession,
    user_id: int,
) -> User:
    """
    Func for chek db
    :param session: async session
    :param user_id: user_id for search User
    :return: User object
    """
    statement = select(User).where(User.id == user_id)
    result = await session.execute(statement)
    return result.scalar_one()


async def get_all_post_for_user(
    session: AsyncSession,
    user: User,
) -> Sequence[Post]:
    """
    Func for chek db.
    :param session: async session
    :param user: User
    :return: All posts for User
    """
    statement = select(Post).where(Post.user_id == user.id)
    result = await session.scalars(statement)
    return result.all()


async def async_main():

    users_data: list[dict]
    posts_data: list[dict]

    users_data, posts_data = await asyncio.gather(
        fetch_json(USERS_DATA_URL),
        fetch_json(POSTS_DATA_URL),
    )

    # Base.metadata.create_all(async_engine)

    async with async_session() as session:
        await create_users(session, users_data)
        await crete_posts(session, posts_data)
    #     user_by_id = await get_user(session, 1)
    #     result = await get_all_post_for_user(session, user_by_id)
    #
    # print(result)


def main():

    asyncio.run(async_main())


if __name__ == "__main__":
    main()
