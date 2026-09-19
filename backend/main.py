from fastapi import FastAPI
from router.books import book
from router.user import user
app = FastAPI()
app.include_router(book)
app.include_router(user, prefix="/users")