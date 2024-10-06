from sqlalchemy import ForeignKey, CheckConstraint, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from typing import List
from datetime import datetime
from src.model.meta import Base
from sqlalchemy import JSON

class Recipe(Base):
    __tablename__ = 'recipe'
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)
    recipe_title: Mapped[str]
    ingredients: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    likes: Mapped[int] = mapped_column(default=0)
    dislikes: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='recipes')

    __table_args__ = (
        CheckConstraint('length(recipe_title) < 1000', name='recipe_title_length'),
        CheckConstraint('likes >= 0', name='likes_non_negative'),
        CheckConstraint('dislikes >= 0', name='dislikes_non_negative')
    )
class User(Base):
    __tablename__ = 'user'
    user_id: Mapped[str] = mapped_column(primary_key=True, index=True)
    registered: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    recipes: Mapped[List[Recipe]] = relationship('Recipe', back_populates='user', cascade='all, delete-orphan')