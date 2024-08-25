from typing import Optional
from fastapi import FastAPI,Body,Path,Query,HTTPException
from pydantic import BaseModel,Field
from starlette import status

app = FastAPI()



class Book:
    id: int
    author: str
    title: str
    description: str
    rating: int

    def __init__(self, id , author, title, description ,rating):
        self.author = author
        self.id = id
        self.title  = title
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id:  Optional[int] = Field(description="Id is not needed for create method",default=None)
    author: str = Field(min_length=1)
    title: str = Field(min_length=3)
    description: str = Field(min_length=1,max_length=100)
    rating: int = Field(gt=-1, lt=6)
    model_config={
        "json_schema_extra":{
        "example":{
            "title":"A New Book",
            "Author":"kalingaRayan",
            "description":"People; Hero",
            "rating":"5"
        }
        }
    }



BOOKS = [

    Book(1,"CSE" , "Anil kubey", "Nice book" , 3),
    Book(2,"Rich dad Poor Dad" , "sooraj", "Nice book" , 3),
    Book(3,"Math" , "kps", "info book" , 5),
    Book(4,"Social" , "siva", "great book" , 1),
    Book(5,"perfect" , "ram", "rocks book" , 4),
    Book(6,"Apollo" , "ganeshan", "fant! book" , 2),
    Book(7,"HP1" , "Author 1", "Great book" , 3),
    Book(8,"HP2" , "Author 2", "Great book" , 3),
    Book(9,"Hp2" , "Author 3", "Great book" , 1),

]
        



@app.get("/books",status_code=status.HTTP_200_OK)
async def all_book1():
    return BOOKS


@app.get("/books/{id}")
async def getbyId(id:int = Path(ge=0,lt=1000)):
    booksList = []
    for book_rating in BOOKS:
        if book_rating.id == id:
            booksList.append(book_rating)
            return booksList
        raise HTTPException(status_code=404,detail="Id is not found") # status code error



@app.post('/create_book',status_code=status.HTTP_201_CREATED)
async def create_book(book_req : BookRequest):
    new_book = Book(**book_req.model_dump())
    BOOKS.append(find_book_id(new_book))
    return "New Bokk added"



@app.get("/books/")
async def get_ratings_byquery(ratings:int = Query(ge=0,lt=6)):
    booksList = []
    for book_rating in BOOKS:
        if book_rating.rating == ratings:
            booksList.append(book_rating)
    return booksList


@app.get("/books/{rating}")
async def get_ratings(rating:int = Path(ge=0)):
    booksList = []
    for book_rating in BOOKS:
        if book_rating.rating == rating:
            booksList.append(book_rating)
    return booksList



@app.put("/books",status_code=status.HTTP_204_NO_CONTENT)
async def Update_book(book_req : BookRequest):
     for i in len(BOOKS):
         if i == book_req.id:
             BOOKS[i] = book_req
             return "Updated Book"
    
     raise HTTPException(status_code=404,detail="Book not found")
    

@app.delete("/books/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def Delete_Book(id:int= Path(gt=0)):
    book_update_status = False
    for i in range(len(BOOKS)):
        if id == i:
            book_update_status=True
            BOOKS.pop(i)
            return f'Book Deleted id = {i}'
    
    if not book_update_status:
        raise HTTPException(status_code=404,detail="Book not found")



def  find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book
