from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database
from typing import List

app = FastAPI(
    title="百姓网API",
    description="百姓网分类信息平台API",
    version="1.0.0"
)

# 创建帖子
@app.post("/posts/", response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db)):
    # 验证用户是否存在
    user = db.query(models.User).filter(models.User.id == post.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 验证分类是否存在
    category = db.query(models.Category).filter(models.Category.id == post.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# 获取帖子列表
@app.get("/posts/", response_model=List[schemas.Post])
async def get_posts(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).offset(skip).limit(limit).all()
    return posts

# 获取单个帖子
@app.get("/posts/{post_id}", response_model=schemas.Post)
async def get_post(post_id: int, db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="帖子不存在")
    return post

# 搜索帖子
@app.get("/posts/search/", response_model=List[schemas.Post])
async def search_posts(keyword: str, db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).filter(
        models.Post.title.contains(keyword) | models.Post.content.contains(keyword)
    ).all()
    return posts

# 创建用户
@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # 检查用户名是否已存在
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 创建新用户（明文密码）
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 获取用户列表
@app.get("/users/", response_model=List[schemas.User])
async def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

# 获取单个用户
@app.get("/users/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user

# 更新用户信息
@app.put("/users/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: int, 
    user: schemas.UserBase, 
    db: Session = Depends(database.get_db)
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 更新用户信息
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

# 删除用户
@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    db.delete(db_user)
    db.commit()
    return {"message": "用户已删除"}

# 创建分类
@app.post("/categories/", response_model=schemas.Category)
async def create_category(category: schemas.CategoryCreate, db: Session = Depends(database.get_db)):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category 