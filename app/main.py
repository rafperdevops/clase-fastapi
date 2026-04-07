from fastapi import FastAPI
from routes import students

app = FastAPI()

app.include_router(students.router)
