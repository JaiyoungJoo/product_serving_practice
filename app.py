from fastapi import FastAPI
from enum import Enum
from typing import Optional

app = FastAPI()

BOOKS = {
    'book_1': {'title':'Title One','author':'Author One'},
    'book_2': {'title':'Title Two','author':'Author Two'},
    'book_3': {'title': 'Title Three', 'author': 'Author Three'},
    'book_4': {'title': 'Title Four', 'author': 'Author Four'},
    'book_5': {'title': 'Title Five', 'author': 'Author Five'},
}

class DirectionName(str, Enum):
    north = "North"
    south = "South"
    east = "East"
    west = "West"

@app.get("/")
async def read_book():
    return BOOKS


@app.post("/creatbooks")
async def create_book(book_title, book_author):
    current_book_id = 0

    if len(BOOKS) > 0:
        for book in BOOKS:
            x = int(book.split('_')[-1])
            if x > current_book_id:
                current_book_id = x
    BOOKS[f'book_{current_book_id + 1}'] = {'title':book_title, 'author': book_author}
    return BOOKS[f'book_{current_book_id + 1}']

@app.delete("/delete_{book_name}")
async def delete_book(book_name):
    del BOOKS[book_name]
    return f"Book {book_name} deleted."

@app.put("/{book_name}")
async def update_book(book_name: str, book_title: str, book_author: str):
    book_information = {'title':book_title, 'author':book_author}
    BOOKS[book_name] = book_information
    return book_information

@app.get("/books/{book_name}")
async def read_book(book_name: str, book_id: str):
    return f"{BOOKS[book_name+book_id]}"

@app.get("/directions/{direction_name}")
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {"Direction":direction_name, "sub":"Up"}
    if direction_name == DirectionName.south:
        return {"Direction":direction_name, "sub":"Down"}
    if direction_name == DirectionName.west:
        return {"Direction":direction_name, "sub":"Left"}
    return {"Direction":direction_name, "sub":"Right"}


## GET 방식으로 루트경로가 호출될 경우, "Hello Eric"라는 문자열"을 넘겨준다.
## 꼭 async를 붙히지 않아도 def만으로 비동기 처리 가능

# uvicorn app:app --reload