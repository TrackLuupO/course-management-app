from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from .database import Base
from sqlalchemy.orm import relationship

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    
    # Relationships should be inside the class
    enrollments = relationship("Enrollment", back_populates="student")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    credit_units = Column(Integer, nullable=False)
    description = Column(String)
    
    # Relationships should be inside the class
    enrollments = relationship("Enrollment", back_populates="course")

class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    
    __table_args__ = (UniqueConstraint('student_id', 'course_id', name='unique_enrollment'),)
    
    # Relationships should be inside the class
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")