from sqlalchemy.orm import Session
from typing import List, Optional
import re

from db.models import Student
from schemas import StudentCreate, StudentResponse
from DAO.student_dao import StudentDAO
from DAO.class_dao import ClassDAO
from fastapi import HTTPException

class StudentBO:
    @staticmethod
    def validate_student_creation(student: StudentCreate) -> bool:
        """
        Kiểm tra tính hợp lệ của thông tin sinh viên khi tạo
        """
        if not student.name or len(student.name.strip()) < 2:
            raise HTTPException(
                status_code=400, 
                detail="Tên sinh viên phải từ 2 ký tự trở lên"
            )
        if student.age < 16 or student.age > 100:
            raise HTTPException(
                status_code=400, 
                detail="Tuổi sinh viên không hợp lệ (16-100)"
            )
        if not StudentBO._validate_email(student.email):
            raise HTTPException(
                status_code=400, 
                detail="Định dạng email không hợp lệ"
            )

        return True

    @staticmethod
    def _validate_email(email: str) -> bool:
        """
        Kiểm tra định dạng email
        """
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    @staticmethod
    def create_student(db: Session, student: StudentCreate) -> StudentResponse:
        """
        Xử lý logic nghiệp vụ trước khi tạo sinh viên
        """
        StudentBO.validate_student_creation(student)
        
        existing_student = db.query(Student).filter(
            Student.email == student.email
        ).first()
        
        if existing_student:
            raise HTTPException(
                status_code=400, 
                detail="Email đã được sử dụng"
            )
        if student.classroom_id:
            classroom = ClassDAO.get_classroom_by_id(db, student.classroom_id)
            if not classroom:
                raise HTTPException(
                    status_code=404, 
                    detail="Lớp học không tồn tại"
                )
        return StudentDAO.create_student(db, student)

    @staticmethod
    def get_student_by_id(db: Session, student_id: int) -> Optional[StudentResponse]:
        """
        Xử lý logic nghiệp vụ khi lấy thông tin sinh viên
        """
        if student_id <= 0:
            raise HTTPException(
                status_code=400, 
                detail="ID sinh viên không hợp lệ"
            )
        student = StudentDAO.get_student_by_id(db, student_id)
        if student is None:
            raise HTTPException(
                status_code=404, 
                detail="Không tìm thấy sinh viên"
            )
        
        return student

    @staticmethod
    def add_student_to_classroom(db: Session, student_id: int, classroom_id: int) -> StudentResponse:
        """
        Xử lý logic thêm sinh viên vào lớp học
        """
        if student_id <= 0 or classroom_id <= 0:
            raise HTTPException(
                status_code=400, 
                detail="ID sinh viên hoặc lớp học không hợp lệ"
            )
        student = StudentDAO.get_student_by_id(db, student_id)
        if not student:
            raise HTTPException(
                status_code=404, 
                detail="Sinh viên không tồn tại"
            )
        classroom = ClassDAO.get_classroom_by_id(db, classroom_id)
        if not classroom:
            raise HTTPException(
                status_code=404, 
                detail="Lớp học không tồn tại"
            )
        if student.classroom_id:
            raise HTTPException(
                status_code=400, 
                detail="Sinh viên đã thuộc một lớp học khác"
            )
        return StudentDAO.add_student_to_classroom(db, student_id, classroom_id)

    @staticmethod
    def get_all_students(db: Session, skip: int = 0, limit: int = 100) -> List[StudentResponse]:
        """
        Lấy danh sách sinh viên với các điều kiện phân trang
        """
        if skip < 0 or limit <= 0:
            raise HTTPException(
                status_code=400, 
                detail="Giá trị skip và limit không hợp lệ"
            )
        
        return StudentDAO.get_all_students(db, skip, limit)