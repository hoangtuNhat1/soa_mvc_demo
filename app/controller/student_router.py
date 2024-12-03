from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from BO.student_bo import StudentBO
from schemas import StudentCreate, StudentResponse
from db.database import get_db

student_routes = APIRouter()

@student_routes.post("/students/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """
    Endpoint tạo sinh viên với các kiểm tra nghiệp vụ
    """
    return StudentBO.create_student(db=db, student=student)

@student_routes.get("/students/", response_model=List[StudentResponse])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Endpoint lấy danh sách sinh viên với phân trang
    """
    return StudentBO.get_all_students(db, skip=skip, limit=limit)

@student_routes.get("/students/{student_id}", response_model=StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    """
    Endpoint lấy thông tin sinh viên theo ID
    """
    return StudentBO.get_student_by_id(db, student_id=student_id)

@student_routes.post("/students/{student_id}/add-to-classroom/{classroom_id}", response_model=StudentResponse)
def add_student_to_classroom(
    student_id: int,
    classroom_id: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint thêm sinh viên vào lớp học với các kiểm tra nghiệp vụ
    """
    return StudentBO.add_student_to_classroom(db, student_id, classroom_id)