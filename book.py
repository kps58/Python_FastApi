from fastapi import FastAPI, Body

app = FastAPI()



BOOKS = [
{'title':'Title One ', 'author':"One" , "category":"Science" },
{'title':'Title two ', 'author':"Two" , "category":"Social" },
{'title':'Title three ', 'author':"three" , "category":"Math" },
{'title':'Title four ', 'author':"four" , "category":"Englisg+h" },
{'title':'Title five ', 'author':"five" , "category":"lang" },
{'title':'Title six ', 'author':"  six" , "category":"Arts" }
]


@app.get("/books/{author}")
async def read_book(author:str, category:str):
     book_selected = {}
     for book in BOOKS:
          if book.get("author").casefold() ==  author and \
               book.get("category").casefold() == category:
               return book
          
     return "Not Found in book list"

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books_name/{name}")
async def read_name(name:str):
     book_name   = {}
     for book in BOOKS:
          if(book['category'].casefold() == name.casefold()):
               book_name = book
     return {"Name"  : book_name}


@app.post("/books/create_book")
async def Add_book(New_book=Body()):
     BOOKS.append(New_book)
     return "Added New Book"

@app.delete("/books/delete")
async def delete_book(book=Body()):
     for books in BOOKS:
          if book.get("author").casefold() == books.get("author").casefold():
               BOOKS.pop(book)
               return "Bokk is Deleted"
          
     return "Book of author name is not found"

     


