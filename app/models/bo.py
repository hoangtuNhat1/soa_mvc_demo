from sqlalchemy.orm import Session
from app.models.bean import Student
from app.models.dao import get_student_by_id, create_student, delete_student
from app.schemas.student import StudentCreate

def create_new_student(db: Session, student_data: StudentCreate):
    new_student = Student(
        name=student_data.name,
        age=student_data.age,
        email=student_data.email,
    )
    return create_student(db, new_student)

def remove_student(db: Session, student_id: int):
    student = get_student_by_id(db, student_id)
    if not student:
        return None
    delete_student(db, student_id)
    return student
