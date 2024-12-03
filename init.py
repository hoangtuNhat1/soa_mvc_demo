from app.database import Base, engine
from app.models.bean import Student, Classroom
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

session = Session(bind=engine)

classroom1 = Classroom(name="Class A", description="This is Class A")
classroom2 = Classroom(name="Class B", description="This is Class B")

student1 = Student(name="Alice", age=20, email="alice@example.com", classroom=classroom1)
student2 = Student(name="Bob", age=22, email="bob@example.com", classroom=classroom1)
student3 = Student(name="Charlie", age=19, email="charlie@example.com", classroom=classroom2)

session.add_all([classroom1, classroom2, student1, student2, student3])
session.commit()

session.close()