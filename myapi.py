from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

# Request Body
students = {
    1: {
        "name": "John Doe",
        "age": 25,
        "grade": "A",
        "year": "12 years",
    }
}

# Request Body of The Post Method
class Student(BaseModel):
    name: str
    age: int
    grade: str
    year: str

# Request Body of The Put Method
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None
    year: Optional[str] = None

# GET Request with no parameters
@app.get("/")
def index():
    return {"name": "Hello, World!"}

# Path Parameters
@app.get("/get-student/{student_id}")
def get_students(student_id: int = Path(..., description="The ID of the student you want to see", gt=0, lt=3)):
    if student_id in students:
        return students[student_id]
    return {"error": "Student ID not found"}

# Query Parameters
@app.get("/get-by-name")
def get_students(name: Optional[str] = None):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not Found"}

# Combining Path and Query Parameters
@app.get("/get-by-name/{student_id}")
def get_students(*, student_id: int, name: Optional[str] = None, test: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not Found"}

# POST Request
@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Students already exist"}
    
    students[student_id] = student
    return students[student_id]

# Put Method
@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}

    if student.name != None:
        students[student_id].name = student.name
    if student.age != None:
        students[student_id].age = student.age
    if student.grade != None:
        students[student_id].grade = student.grade
    if student.year != None:
        students[student_id].year = student.year

    return students[student_id]

# DELETE Methods for students
@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}

    del students[student_id]
    return {"Message": "Student deleted successfully"}
