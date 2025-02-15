from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    category_id: int
    price: Optional[Decimal] = None

class PostCreate(PostBase):
    user_id: int
    status: Optional[int] = 1
    views: Optional[int] = 0

class Post(PostBase):
    id: int
    user_id: int
    status: int
    views: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 