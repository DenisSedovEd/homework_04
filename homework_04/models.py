"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user
"""

import os

from sqlalchemy import String, Text, MetaData, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

PG_CONN_URI = (
    os.environ.get("SQLALCHEMY_PG_CONN_URI")
    or "postgresql+asyncpg://postgres:password@localhost/postgres"
)

DB_LOCAL_URL = "postgresql+asyncpg://app:password@localhost:5427/homework_04_db"

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

Session = None

async_engine = create_async_engine(
    DB_LOCAL_URL,
    echo=False,
)

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(
        String(length=32),
        unique=True,
    )
    name: Mapped[str] = mapped_column(
        String(length=32),
        unique=False,
    )
    email: Mapped[str | None] = mapped_column(
        String(length=150),
        unique=True,
        server_default="",
        default="",
    )

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
    )

    def __str__(self):
        return f"{self.username} ({self.email})"

    def __repr__(self):
        return str(self)


class Post(Base):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(
        String(length=120),
        index=True,
        unique=True,
        default="",
        server_default="",
    )
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )

    user: Mapped["User"] = relationship(
        back_populates="posts",
    )

    def __str__(self):
        return f"{self.title} ({self.user_id})"

    def __repr__(self):
        return str(self)
