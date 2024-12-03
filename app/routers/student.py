from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.bo import create_new_student, remove_student
from app.models.dao import get_student_by_id
from app.schemas.student import StudentCreate, StudentResponse

router = APIRouter(
    prefix="/students",
    tags=["students"],
)

@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return create_new_student(db, student)

@router.get("/{student_id}", response_model=StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = remove_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted"}
