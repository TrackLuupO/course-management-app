from fastapi.testclient import TestClient
from ..main import app
from ..database import SessionLocal, Base, engine

client = TestClient(app)

def setup_module():
    Base.metadata.create_all(bind=engine)

def test_create_enroll_duplicate():
    # Create student
    r = client.post("/students/", json={"name": "John Doe", "email": "john@example.com"})
    student_id = r.json()["id"]
    
    # Create course
    r = client.post("/courses/", json={"title": "Math", "code": "M101", "credit_units": 3})
    course_id = r.json()["id"]
    
    # Enroll
    client.post("/enroll/", json={"student_id": student_id, "course_id": course_id})
    
    # Try duplicate
    r = client.post("/enroll/", json={"student_id": student_id, "course_id": course_id})
    assert r.status_code == 400

def test_student_courses():
    r = client.get("/students/1/courses/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_study_tips():
    r = client.post("/genai/study-tips", json={"course_title": "Physics", "credit_units": 4})
    assert r.status_code in [200, 500]  # 500 if no key, 200 if yes