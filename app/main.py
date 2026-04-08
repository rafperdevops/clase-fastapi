# Importación de FastAPI
from fastapi import FastAPI

# Importación del router de estudiantes
# students.py contiene todas las rutas relacionadas con estudiantes
from routes import students

# Importación de engine y Base para crear las tablas
# engine: conexión a la base de datos SQLite
# Base: clase base para los modelos ORM
from database import engine, Base

# create_all(): crea todas las tablas definidas en los modelos
# Se ejecuta al iniciar la app y crea el archivo 'students.db' si no existe
Base.metadata.create_all(bind=engine)

# Instancia principal de FastAPI
app = FastAPI()

# Registro del router de estudiantes
# Todas las rutas de students.py estarán disponibles en /students
app.include_router(students.router)