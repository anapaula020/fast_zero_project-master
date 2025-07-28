from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from http import HTTPStatus
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import UserCreate, UserPublic, Token
from fast_zero.security import (
    create_access_token,
    get_password_hash,
    verify_password,
    get_current_user,
)

app = FastAPI()


@app.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Incorrect email or password"
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    exists = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if exists:
        detail = (
            "Username already exists"
            if exists.username == user.username
            else "Email already exists"
        )
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=detail)

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get("/users/", response_model=List[UserPublic])
def read_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return users


@app.get("/users/{user_id}", response_model=UserPublic)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Not allowed")

    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = get_password_hash(user.password)

    try:
        session.commit()
        session.refresh(db_user)
        return db_user
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Username or email already exists"
        )


@app.delete("/users/{user_id}", response_model=dict)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Not allowed")

    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    session.delete(db_user)
    session.commit()
    return {"message": "User deleted"}


@app.get("/TESTES/{teste_aplicação}", response_model=dict)
def read_root():
    return {"message": "Olá Mundo!"}
