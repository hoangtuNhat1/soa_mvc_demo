from sqlalchemy.orm import Session
from typing import Optional
from db.models import Classroom
from schemas import ClassroomCreate, ClassroomResponse
from DAO.class_dao import ClassDAO
from fastapi import HTTPException

class ClassBO:
    @staticmethod
    def validate_classroom_creation(classroom: ClassroomCreate) -> bool:
        """
        Kiểm tra tính hợp lệ của thông tin lớp học khi tạo
        """
        if not classroom.name or len(classroom.name.strip()) == 0:
            raise HTTPException(
                status_code=400, 
                detail="Tên lớp học không được để trống"
            )
        if len(classroom.name) < 3 or len(classroom.name) > 50:
            raise HTTPException(
                status_code=400, 
                detail="Tên lớp học phải từ 3-50 ký tự"
            )
        
        return True
    
    @staticmethod
    def create_classroom(db: Session, classroom: ClassroomCreate) -> ClassroomResponse:
        """
        Xử lý logic nghiệp vụ trước khi tạo lớp học
        """
        ClassBO.validate_classroom_creation(classroom)
        
        existing_classroom = db.query(Classroom).filter(
            Classroom.name == classroom.name
        ).first()
        
        if existing_classroom:
            raise HTTPException(
                status_code=400, 
                detail="Tên lớp học đã tồn tại"
            )
        return ClassDAO.create_classroom(db, classroom)
    
    @staticmethod
    def get_classroom_by_id(db: Session, classroom_id: int) -> Optional[ClassroomResponse]:
        """
        Xử lý logic nghiệp vụ khi lấy thông tin lớp học
        """
        if classroom_id <= 0:
            raise HTTPException(
                status_code=400, 
                detail="ID lớp học không hợp lệ"
            )
        classroom = ClassDAO.get_classroom_by_id(db, classroom_id)
        if classroom is None:
            raise HTTPException(
                status_code=404, 
                detail="Không tìm thấy lớp học"
            )
        
        return classroom