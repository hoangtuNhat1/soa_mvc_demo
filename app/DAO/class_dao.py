from sqlalchemy.orm import Session
from db.models import Classroom
from schemas import ClassroomCreate

class ClassDAO:
    @staticmethod
    def create_classroom(db: Session, classroom: ClassroomCreate):
        """
        Thực hiện tạo lớp học trong database
        """
        db_classroom = Classroom(**classroom.dict())
        db.add(db_classroom)
        db.commit()
        db.refresh(db_classroom)
        return db_classroom
    
    @staticmethod
    def get_classroom_by_id(db: Session, classroom_id: int):
        """
        Truy vấn lớp học theo ID
        """
        return db.query(Classroom).filter(Classroom.id == classroom_id).first()