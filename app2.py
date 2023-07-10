# https://zambbon.tistory.com/entry/FastAPI-BaseModel-%EC%83%9D%EC%84%B1-13

from fastapi import FastAPI, HTTPException, Request, Form, Header
from starlette.responses import JSONResponse
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

app = FastAPI()

class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: Optional[str] = Field(
        None,
        title='Description of the Book',
        max_length=100,
        min_length=1
    )

class NegativeNumberException(Exception):
    def __init__(self, books_to_return: int):
        self.books_to_return = books_to_return

class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1) #최소길이가 1
    author: str = Field(min_length=1, max_length=100) #최소길이는 1, 최대길이는 100
    description: Optional[str] = Field(title="Description of the book",
                           max_length=100,
                            min_length=1)
    rating: int = Field(gt=-1, lt=101) #-1보다는 크고 101보다는 작다 (0~100사이)
    class Config:
        schema_extra = {
            "example":{
                "id" : "637d1b93-0174-48e7-8959-e17530b6c690",
                "title" : "Computer Science Pro",
                "author" : "Codingwithroby",
                "description" : "A very nice description of a book",
                "rating" : 75
            }
        }

def create_books_no_api():
    book_1 = Book(id="637d1b93-0174-48e7-8959-e17530b6c690",
                  title="Title 1",
                  author="Author 1",
                  description="Description 1",
                  rating=60)
    book_2 = Book(id="637d1b93-0174-48e7-8959-e17530b6c690",
                  title="Title 2",
                  author="Author 2",
                  description="Description 2",
                  rating=60)
    book_3 = Book(id="637d1b93-0174-48e7-8959-e17530b6c690",
                  title="Title 3",
                  author="Author 3",
                  description="Description 3",
                  rating=60)
    book_4 = Book(id="637d1b93-0174-48e7-8959-e17530b6c690",
                  title="Title 4",
                  author="Author 4",
                  description="Description 4",
                  rating=60)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)

def raise_item_cannot_he_found_exception():
    return HTTPException(status_code=404,
                         detail="Book not found",
                         headers={"X-Header_Error":"Nothing to be seen at the UUID"})

BOOKS = []
# @app.get("/")
# async def read_all_books():
#     if len(BOOKS) < 1:
#         create_books_no_api()
#     return BOOKS

# @app.get("/")
# async def read_all_books():
#     return BOOKS


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):

    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)

    if len(BOOKS) < 1:
        create_books_no_api()

    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i - 1])
            i += 1
        return new_books
    return BOOKS

@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)
    return book

@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0
    for BOOK in BOOKS:
        counter += 1
        if BOOK.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]
        
@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0

    for BOOK in BOOKS:
        counter += 1
        if BOOK.id == book_id:
            del BOOKS[counter - 1]
            return f'ID:{book_id} deleted'
    raise raise_item_cannot_he_found_exception()

@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request, exception: NegativeNumberException):

    return JSONResponse(
        status_code=418,
        content={"message":f"Hey, why do you want {exception.books_to_return}"
                           f"books? you need to read more!"})

@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id:UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_he_found_exception()

@app.post("/books/login")
async def book_login(username: str = Form(...), password: str = Form(...)):
    return {"username":username, "password":password}

@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"Random-Header": random_header}