from datetime import datetime
from pydantic import BaseModel, EmailStr
from fastapi import Query
from fastapi.params import Body, Optional
from typing import List, Dict


class EventBase(BaseModel):
    title: str
    date: str  # accepting date as a string
    link: str
    location: str
    description: Optional[str] = None
    tags: List[str] = Query([None])
    published: bool = True


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    title: Optional[str] = None
    date: Optional[str] = None
    link: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    published: Optional[bool] = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Event(EventBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Upvote(BaseModel):
    event_id: int


class EventOut(BaseModel):
    Event: Event
    upvotes: int

    class Config:
        orm_mode = True
