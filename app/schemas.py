from pydantic import BaseModel, EmailStr
from typing import Optional, List

class StudentBase(BaseModel):
    name: str
    age: int
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int

    class Config:
        orm_mode = True

class ClassroomBase(BaseModel):
    name: str
    description: Optional[str] = None

class ClassroomCreate(ClassroomBase):
    pass

class ClassroomResponse(ClassroomBase):
    id: int
    students: List[StudentResponse] = []

    class Config:
        orm_mode = True