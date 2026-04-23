from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.student_model import Student, StudentResponse
from app.controllers.student_controller import StudentController
from app.database import get_db

router = APIRouter(prefix="/students", tags=["Estudiantes"])


@router.get("/", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return StudentController.get_all(db)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return StudentController.get_by_id(student_id, db)


@router.post("/", response_model=StudentResponse)
def create_student(student: Student, db: Session = Depends(get_db)):
    return StudentController.create(student, db)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, updated_data: Student, db: Session = Depends(get_db)):
    return StudentController.update(student_id, updated_data, db)


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    return StudentController.delete(student_id, db)