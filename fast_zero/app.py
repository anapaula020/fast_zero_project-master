from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from fast_zero.schemas import Message, UserDB, UserPublic, UserSchema

app = FastAPI()

# Banco de dados simulado: lista de UserDB (inclui senha, mas não expõe)
database = []


@app.get(
    "/",
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def read_root():
    return {"message": "Olá Mundo!"}


@app.post(
    "/users/",
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
)
def create_user(user: UserSchema):
    # Cria usuário com id sequencial
    user_with_id = UserDB(
        **user.model_dump(),
        id=len(database) + 1,
    )
    database.append(user_with_id)
    # Retorna UserPublic (sem senha)
    return UserPublic(
        id=user_with_id.id,
        username=user_with_id.username,
        email=user_with_id.email,
    )


@app.put(
    "/users/{user_id}",
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
)
def update_user(user_id: int, user: UserSchema):
    for index, existing_user in enumerate(database):
        if existing_user.id == user_id:
            updated_user = UserDB(
                **user.model_dump(),
                id=user_id,
            )
            database[index] = updated_user
            return UserPublic(
                id=updated_user.id,
                username=updated_user.username,
                email=updated_user.email,
            )
    raise HTTPException(
        status_code=404,
        detail="User not found",
    )


@app.delete(
    "/users/{user_id}",
    status_code=HTTPStatus.OK,
)
def delete_user(user_id: int):
    for index, existing_user in enumerate(database):
        if existing_user.id == user_id:
            del database[index]
            return {"message": "User deleted"}
    raise HTTPException(
        status_code=404,
        detail="User not found",
    )
