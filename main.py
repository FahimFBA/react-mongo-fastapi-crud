from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel

app = FastAPI()

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["todo_app"]
todos_collection = db["todos"]

# Todo Model


class Todo(BaseModel):
    item: str

# Get all todos


@app.get("/todos")
async def get_todos():
    todos = list(todos_collection.find({}, {"_id": 0}))
    return todos

# Create a todo


@app.post("/todos")
async def create_todo(todo: Todo):
    todos_collection.insert_one(todo.dict())
    return {"message": "Todo has been added"}

# Update a todo


@app.put("/todos/{todo_id}")
async def update_todo(todo_id: str, todo: Todo):
    todos_collection.update_one({"_id": todo_id}, {"$set": todo.dict()})
    return {"message": "Todo has been updated"}

# Delete a todo


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str):
    todos_collection.delete_one({"_id": todo_id})
    return {"message": "Todo has been deleted"}
