# Домашняя работа "Асинхронная работа с БД и подключение API"

### После подключения БД необходимо проинициализировать асинхронный Alembic и применить миграции:




```bash

alembic init -t async alembic
alembic upgrade head
```


### Для проверки работы асинхронного взаимодействия с БД были написаны небольшие функции в фале main.py:

```python

async def get_user(
    session: AsyncSession,
    user_id: int,
) -> User:
    statement = select(User).where(User.id == user_id)
    result = await session.execute(statement)
    return result.scalar_one()


async def get_all_post_for_user(
    session: AsyncSession,
    user: User,
) -> Sequence[Post]:
    statement = select(Post).where(Post.user_id == user.id)
    result = await session.scalars(statement)
    return result.all()


```