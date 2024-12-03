from fastapi import FastAPI
from controller.api_router import student_routes, class_routes
from db.database import init_db

app = FastAPI(title="Student Management API")

app.include_router(student_routes, tags=["students"])
app.include_router(class_routes, tags=["classrooms"])

@app.on_event("startup")
def startup_event():
    init_db()
@app.get("/")
def read_root():
    return {"message": "Welcome to Student Management API"}