from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from BO.class_bo import ClassBO
from schemas import ClassroomCreate, ClassroomResponse, StudentResponse
from db.database import get_db

class_routes = APIRouter()

@class_routes.post("/classrooms/", response_model=ClassroomResponse)
def create_classroom(classroom: ClassroomCreate, db: Session = Depends(get_db)):
    """
    Endpoint tạo lớp học với các kiểm tra nghiệp vụ
    """
    return ClassBO.create_classroom(db=db, classroom=classroom)

@class_routes.get("/classrooms/{classroom_id}", response_model=ClassroomResponse)
def read_classroom(classroom_id: int, db: Session = Depends(get_db)):
    """
    Endpoint lấy thông tin lớp học với các kiểm tra nghiệp vụ
    """
    return ClassBO.get_classroom_by_id(db, classroom_id=classroom_id)