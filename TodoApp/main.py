from typing import Annotated
from fastapi import Body, Depends, FastAPI, Path, status,HTTPException
from pydantic import BaseModel, Field
from database import engine, sessionLocal
from model import Todos,Base
from sqlalchemy.orm import Session




app = FastAPI()

Base.metadata.create_all(bind=engine)

# app.include_router()

class TodoRequest(BaseModel):
    title:str = Field(min_length=5)
    description:str  = Field(min_length=5)
    priority:str  = Field()
    complete:bool = Field(default=False)



def get_db():
    db = sessionLocal()
    try:
        yield db

    finally:
        db.close()

        
db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/todos",status_code=status.HTTP_200_OK)
async def get_todosall(db: db_dependency):
    return db.query(Todos).all()


@app.get("/todos/{id}",status_code=status.HTTP_200_OK)
async def get_todos_id(db:db_dependency,id:int = Path(ge=0)):
    return db.query(Todos).filter(Todos.id == id).first()

@app.post("/todos",status_code=status.HTTP_201_CREATED)
async def new_todo(db:db_dependency,new_todo :TodoRequest):
    todo = Todos(**new_todo.model_dump())# use model dump to get request data
    db.add(todo)
    db.commit()


@app.put("/todos/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dependency,u_todo:TodoRequest,id:int = Path(ge=0)):
    u_todo = Todos(**u_todo.model_dump())
    update_todo_data = db.query(Todos).filter(Todos.id == id).first()
    if not  update_todo_data:
        return HTTPException(status_code=404,detail="Id is not found")
    update_todo_data.complete = u_todo.complete
    update_todo_data.description = u_todo.description
    update_todo_data.title = u_todo.title
    update_todo_data.priority = u_todo.priority
    db.add(update_todo_data)
    db.commit()

@app.delete("/todos/{id}",status_code=status.HTTP_200_OK)
async def update_todo(db:db_dependency,id:int = Path(ge=0)):
   
    update_todo_data = db.query(Todos).filter(Todos.id == id).delete()
    if not  update_todo_data:
        return HTTPException(status_code=404,detail="Id is not found")
    db.commit()
    

    