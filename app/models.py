from sqlalchemy import Boolean, Column, Integer, String, DateTime, TIMESTAMP, ForeignKey, Table
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base, relationship
from .database import Base

Base = declarative_base()


class Upvote(Base):
    __tablename__ = 'upvotes'

    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'), primary_key=True)

    # relationships
    user = relationship("User", back_populates="upvotes")
    event = relationship("Event", back_populates="upvotes")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    date = Column(String, nullable=False)
    location = Column(String, nullable=False)
    link = Column(String, nullable=False)
    description = Column(String, nullable=False)
    tags = Column(ARRAY(String), nullable=False)
    published = Column(Boolean, server_default="true")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text(
        "NOW()"))
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    user = relationship('User')
    upvotes = relationship('Upvote', back_populates='event')


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text(
        "NOW()"))
    upvotes = relationship('Upvote', back_populates='user')
