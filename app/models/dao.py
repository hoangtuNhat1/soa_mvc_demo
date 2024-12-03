from sqlalchemy.orm import Session
from app.models.bean import Student

def get_student_by_id(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def create_student(db: Session, student: Student):
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

def delete_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student:
        db.delete(student)
        db.commit()
