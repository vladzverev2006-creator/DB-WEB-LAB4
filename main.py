from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Book Library API")

# Схема для валидации входящих данных (без id)
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, description="Название книги")
    author: str = Field(..., min_length=1, description="Автор книги")
    year: int = Field(..., gt=0, le=2100, description="Год издания")

# Схема возвращаемой книги (содержит сгенерированный id)
class Book(BookBase):
    id: int

# Хранилище в оперативной памяти и счетчик идентификаторов
books: list[Book] = []
next_id: int = 1


@app.get("/books", response_model=list[Book], summary="Получить все книги")
def get_all_books():
    return books


@app.get("/books/{book_id}", response_model=Book, summary="Получить книгу по ID")
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Книга с ID {book_id} не найдена"
    )


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED, summary="Добавить новую книгу")
def create_book(book_in: BookBase):
    global next_id
    new_book = Book(id=next_id, **book_in.model_dump())
    books.append(new_book)
    next_id += 1
    return new_book


@app.put("/books/{book_id}", response_model=Book, summary="Обновить книгу по ID")
def update_book(book_id: int, book_in: BookBase):
    for index, book in enumerate(books):
        if book.id == book_id:
            updated_book = Book(id=book_id, **book_in.model_dump())
            books[index] = updated_book
            return updated_book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Книга с ID {book_id} не найдена"
    )


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить книгу по ID")
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book.id == book_id:
            books.pop(index)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Книга с ID {book_id} не найдена"
    )
