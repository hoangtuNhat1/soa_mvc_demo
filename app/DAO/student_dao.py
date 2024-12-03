from sqlalchemy.orm import Session
from db.models import Student, Classroom
from schemas import StudentCreate
from fastapi import HTTPException
class StudentDAO:
    @staticmethod
    def create_student(db: Session, student: StudentCreate):
        db_student = Student(**student.dict())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    
    @staticmethod
    def get_student_by_id(db: Session, student_id: int):
        return db.query(Student).filter(Student.id == student_id).first()
    
    @staticmethod
    def get_all_students(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Student).offset(skip).limit(limit).all()
    
    @staticmethod
    def add_student_to_classroom(db: Session, student_id: int, classroom_id: int):
        student = db.query(Student).filter(Student.id == student_id).first()
        classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()

        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        if not classroom:
            raise HTTPException(status_code=404, detail="Classroom not found")

        student.classroom_id = classroom_id
        db.commit()
        db.refresh(student)
        return student