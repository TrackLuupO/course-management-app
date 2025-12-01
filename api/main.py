from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os
from groq import Groq
import logging

from .database import SessionLocal, engine, Base, get_db
from .models import Student, Course, Enrollment
from .schemas import StudentCreate, StudentOut, CourseCreate, CourseOut, EnrollCreate, TipsRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Error creating database tables: {e}")

app = FastAPI(
    title="Course Enrollment API",
    description="A comprehensive API for managing students, courses, and enrollments",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Course Enrollment API is running!",
        "version": "1.0.0",
        "endpoints": {
            "students": "/students",
            "courses": "/courses",
            "enrollments": "/enroll",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running successfully"}

@app.post("/students/", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating student: {student.name} ({student.email})")

        existing_student = db.query(Student).filter(Student.email == student.email).first()
        if existing_student:
            logger.warning(f"Student with email {student.email} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student with this email already exists"
            )

        db_student = Student(**student.model_dump())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)

        logger.info(f"Student created successfully with ID: {db_student.id}")
        return db_student

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating student: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create student: {str(e)}"
        )

@app.get("/students/", response_model=list[StudentOut])
def get_students(db: Session = Depends(get_db)):
    try:
        students = db.query(Student).all()
        logger.info(f"Retrieved {len(students)} students")
        return students
    except Exception as e:
        logger.error(f"Error retrieving students: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve students"
        )

@app.get("/students/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            logger.warning(f"Student with ID {student_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        return student
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving student {student_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve student"
        )

@app.post("/courses/", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating course: {course.title} ({course.code})")

        existing_course = db.query(Course).filter(Course.code == course.code).first()
        if existing_course:
            logger.warning(f"Course with code {course.code} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Course with this code already exists"
            )

        db_course = Course(**course.model_dump())
        db.add(db_course)
        db.commit()
        db.refresh(db_course)

        logger.info(f"Course created successfully with ID: {db_course.id}")
        return db_course

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating course: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create course: {str(e)}"
        )

@app.get("/courses/", response_model=list[CourseOut])
def get_courses(db: Session = Depends(get_db)):
    try:
        courses = db.query(Course).all()
        logger.info(f"Retrieved {len(courses)} courses")
        return courses
    except Exception as e:
        logger.error(f"Error retrieving courses: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve courses"
        )

@app.get("/courses/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    try:
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            logger.warning(f"Course with ID {course_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        return course
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving course {course_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve course"
        )

@app.post("/enroll/", status_code=status.HTTP_201_CREATED)
def enroll(enroll: EnrollCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Enrolling student {enroll.student_id} in course {enroll.course_id}")

        student = db.query(Student).filter(Student.id == enroll.student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )

        course = db.query(Course).filter(Course.id == enroll.course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )

        existing_enrollment = db.query(Enrollment).filter(
            Enrollment.student_id == enroll.student_id,
            Enrollment.course_id == enroll.course_id
        ).first()

        if existing_enrollment:
            logger.warning(f"Student {enroll.student_id} already enrolled in course {enroll.course_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student already enrolled in this course"
            )

        db_enroll = Enrollment(**enroll.model_dump())
        db.add(db_enroll)
        db.commit()

        logger.info(f"Enrollment successful: student {enroll.student_id} in course {enroll.course_id}")
        return {
            "message": "Enrolled successfully",
            "student_id": enroll.student_id,
            "course_id": enroll.course_id
        }

    except IntegrityError:
        db.rollback()
        logger.error("Integrity error during enrollment")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student already enrolled in this course"
        )
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error during enrollment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to enroll student: {str(e)}"
        )

@app.get("/enrollments/")
def get_enrollments(db: Session = Depends(get_db)):
    try:
        enrollments = db.query(Enrollment).all()
        return enrollments
    except Exception as e:
        logger.error(f"Error retrieving enrollments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve enrollments"
        )

@app.get("/students/{student_id}/courses/", response_model=list[CourseOut])
def student_courses(student_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Fetching courses for student {student_id}")

        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            logger.warning(f"Student with ID {student_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )

        courses = db.query(Course).join(Enrollment).filter(Enrollment.student_id == student_id).all()
        logger.info(f"Found {len(courses)} courses for student {student_id}")
        return courses

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching student courses: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch student courses"
        )

@app.get("/courses/{course_id}/students/", response_model=list[StudentOut])
def course_students(course_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Fetching students for course {course_id}")

        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            logger.warning(f"Course with ID {course_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )

        students = db.query(Student).join(Enrollment).filter(Enrollment.course_id == course_id).all()
        logger.info(f"Found {len(students)} students for course {course_id}")
        return students

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching course students: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch course students"
        )

@app.post("/genai/study-tips")
def study_tips(request: TipsRequest):
    api_key = os.getenv("GROQ_API_KEY")
    print(f"API Key present: {bool(api_key)}")

    if not api_key:
        print("GROQ_API_KEY not found in environment variables")
        # Return mock data
        mock_tips = [
            f"Study {request.course_title} for {request.credit_units} hours weekly",
            "Create flashcards for key concepts",
            "Practice with past exam papers",
            "Join online forums related to the subject",
            "Set specific weekly learning goals"
        ]
        return {"tips": mock_tips}

    try:
        client = Groq(api_key=api_key)
        prompt = f"Generate 3-5 practical study tips for a {request.credit_units}-credit course called '{request.course_title}'. Focus on time management, study techniques, and resource utilization. Keep tips concise and actionable."

        print(f"Sending request to Groq API for course: {request.course_title}")

        # Updated model list with currently working models
        available_models = [
            "llama-3.1-8b-instant",  # This works perfectly
            "llama-3.1-70b-versatile",
            "mixtral-8x7b-32768",
            "gemma-7b-it"
        ]

        # Use the first model
        model_to_use = available_models[0]
        print(f"Using model: {model_to_use}")

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=model_to_use,
            temperature=0.7,
            max_tokens=300,
            top_p=1,
            stream=False,
        )

        response_content = chat_completion.choices[0].message.content
        print(f"Groq API Response: {response_content}")

        # Better tip parsing
        tips = []
        lines = response_content.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and len(line) > 10:  # Only include substantial lines
                # Remove numbering and bullet points
                clean_tip = line.lstrip('123456789.-*• ').strip()
                if clean_tip:
                    tips.append(clean_tip)

        # Ensure we have at least 3 tips
        if len(tips) < 3:
            tips.extend([
                f"Review {request.course_title} materials weekly",
                "Practice with real-world examples",
                "Form study groups for better understanding"
            ])

        return {"tips": tips[:5]}  # Return max 5 tips

    except Exception as e:
        print(f"Detailed Groq API error: {str(e)}")
        print(f"Error type: {type(e).__name__}")

        # Check if it's a specific Groq error
        if hasattr(e, 'status_code'):
            print(f"Status code: {e.status_code}")
        if hasattr(e, 'body'):
            print(f"Error body: {e.body}")

        fallback_tips = [
            f"Allocate {credit_hours} hours per week for {request.course_title}",
            "Create a study schedule and stick to it consistently",
            "Break complex topics into smaller, manageable sections",
            "Use active recall by testing yourself without notes",
            "Create visual aids like mind maps and diagrams",
            "Form study groups to discuss difficult concepts",
            "Practice with past exams and timed exercises",
            "Teach the material to someone else to reinforce learning",
            "Use multiple resources - textbooks, videos, and online tutorials",
            "Review notes within 24 hours of each study session"
        ]

        # Return 5 high-quality, relevant tips
        import random
        selected_tips = random.sample(fallback_tips, min(5, len(fallback_tips)))
        print(f"Using fallback tips for {request.course_title}")
        return {"tips": selected_tips}

@app.get("/debug/endpoints")
def list_endpoints():
    url_list = []
    for route in app.routes:
        if hasattr(route, "methods"):
            url_list.append({
                "path": route.path,
                "methods": list(route.methods)
            })
    return url_list

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)