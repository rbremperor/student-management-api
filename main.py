from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from itertools import count

app = FastAPI()

# In-memory database (for demonstration)
fake_students_db = {}

# Initialize a counter for auto-incrementing IDs
id_counter = count(1)  # Start from 1 and increment for each new student


# Pydantic model for input validation
class Student(BaseModel):
    name: str
    age: int
    major: str


# Create a new student (POST)
@app.post("/students/", response_model=Student)
async def add_student(student: Student):
    student_id = str(next(id_counter))  # Generate the next ID in the sequence
    student_data = student.dict()  # Convert Pydantic model to dict
    student_data['id'] = student_id  # Add the generated ID to the dictionary
    fake_students_db[student_id] = student_data  # Store the student in the fake DB with the ID
    return student_data  # Return the student data including the ID


# Get all students (GET)
@app.get("/students/", response_model=List[Student])
async def get_students():
    return list(fake_students_db.values())


# Get a student by ID (GET)
@app.get("/students/{student_id}", response_model=Student)
async def get_student(student_id: str):
    student = fake_students_db.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# Update a student (PUT)
@app.put("/students/{student_id}", response_model=Student)
async def update_student(student_id: str, student: Student):
    if student_id not in fake_students_db:
        raise HTTPException(status_code=404, detail="Student not found")

    # Update the student data
    updated_data = student.dict()  # Convert Pydantic model to dict
    updated_data['id'] = student_id  # Keep the existing ID in the updated data
    fake_students_db[student_id] = updated_data  # Update the student in the fake DB
    return updated_data  # Return the updated student data


# Delete a student (DELETE)
@app.delete("/students/{student_id}")
async def delete_student(student_id: str):
    if student_id not in fake_students_db:
        raise HTTPException(status_code=404, detail="Student not found")

    del fake_students_db[student_id]  # Delete the student from the fake DB
    return {"message": "Student deleted successfully"}
