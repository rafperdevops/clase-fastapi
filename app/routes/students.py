from fastapi import APIRouter
from models.student_model import Student, StudentResponse
from controllers.student_controller import StudentController

router = APIRouter(prefix="/students", tags=["Estudiantes"])

@router.get("/", response_model=list[StudentResponse])
def get_students():
    return StudentController.get_all()

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int):
    return StudentController.get_by_id(student_id)

@router.post("/", response_model=StudentResponse)
def create_student(student: Student):
    return StudentController.create(student)

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, updated_data: Student):
    return StudentController.update(student_id, updated_data)

@router.delete("/{student_id}")
def delete_student(student_id: int):
    return StudentController.delete(student_id)
