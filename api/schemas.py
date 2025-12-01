from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    email: str

class StudentOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class CourseCreate(BaseModel):
    title: str
    code: str
    credit_units: int
    description: str | None = None

class CourseOut(BaseModel):
    id: int
    title: str
    code: str
    credit_units: int
    description: str | None

    class Config:
        from_attributes = True

class EnrollCreate(BaseModel):
    student_id: int
    course_id: int

class TipsRequest(BaseModel):
    course_title: str
    credit_units: int