# from fastapi import FastAPI
# from pydantic import BaseModel
# app = FastAPI()
# @app.get("/")
# def home():
#     return {"message": "Hello World"}
# # -------------------path--parameter----------------------
# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     return {"user_id": user_id}
# #--------------------query--parameter---------------------
# @app.get("/users")
# def get_users(name: str):
#     return {"name": name}
# # --------------------post--parameter---------------------
# class User(BaseModel):
#     name: str
#     age: int

# @app.post("/users")
# def create_user(user: User):
#     return {
#         "message": "User created",
#         "user": user
#     }