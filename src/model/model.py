from sqlalchemy import ForeignKey, CheckConstraint, Integer, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from typing import List
from datetime import datetime

class Base(DeclarativeBase):
    pass

class UUIDMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

class Recipe(Base, UUIDMixin):
    __tablename__ = 'recipe'
    recipe_title: Mapped[str]
    ingredients: Mapped[List[str]] = mapped_column(nullable=False)
    likes: Mapped[int] = mapped_column(default=0)
    dislikes: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'), nullable=False)

    user = relationship('User', back_populates='recipes')

    __table_args__ = (
        CheckConstraint('length(recipe_title) < 1000', name='recipe_title_length'),
        CheckConstraint('likes >= 0', name='likes_non_negative'),
        CheckConstraint('dislikes >= 0', name='dislikes_non_negative')
    )
class User(Base, UUIDMixin):
    __tablename__ = 'user'
    username: Mapped[str]
    registered: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    recipes: Mapped[List[Recipe]] = relationship('Recipe', back_populates='user', cascade='all, delete-orphan')