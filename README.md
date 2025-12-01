# course-management-system

Complete Course Management System: FastAPI backend + Vue.js frontend with student/course management, enrollment system, AI study tips, and real-time monitoring

---

https://img.shields.io/badge/Status-Production_Ready-brightgreen 

https://img.shields.io/badge/FastAPI-0.104.1-009688 

https://img.shields.io/badge/Vue.js-3.3-4FC08D 

https://img.shields.io/badge/Python-3.12-3776AB

---

# ✨ Features

## 🎯 Core Functionality
* Student Management: Add, view, and manage student profiles

* Course Management: Create and organize academic courses with credit units

* Enrollment System: Enroll students in courses with duplicate prevention

* Relationship Views:

  - View all courses for a specific student

  - View all students enrolled in a specific course

* Real-time Connection Monitoring: Live backend status indicator


## 🤖 AI-Powered Features
* Smart Study Tips: AI-generated study recommendations for each course

* Context-Aware: Tips tailored to course credit units and subject matter

* Fallback System: High-quality curated tips when AI is unavailable

## 📊 User Interface
* Modern Dashboard: Clean, responsive design with gradient background

* Modal-Based Workflow: Organized data presentation in collapsible modals

* Real-time Statistics: Live counters for students, courses, and enrollments

* Table Views: Compact data presentation for large datasets



## 🏗️ Architecture

### Backend (FastAPI)
```
course-management-system/

├── api/
│   ├── main.py              
│   ├── database.py          
│   ├── models.py            
│   ├── schemas.py          
│   └── tests/
│   │    ├── init.py
│   │    └── test_main.py
├── enrollment.db            
└── .env                    
```


### Frontend (Vue.js)
```
frontend/
│    ├── src/
│    │   ├── App.vue 
│    │   ├── main.js
│    │   └── style.css
├── README.md
├── index.html            
├── package.json
└── vite.config.js
```

## 🚀 Getting Started
### Prerequisites
* Python 3.12+

* Node.js 18+

* Groq API Key (for AI features) - Get Free Key


## Installation
1. Clone the Repository

```
bash
git clone https://github.com/yourusername/course-enrollment-system.git
cd course-enrollment-system
```

2. Backend Setup

```bash
cd api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

3. Frontend Setup

```bash
cd frontend
npm install
```

## Running the Application

1. Start Backend Server
```bash
cd api
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

2. Start Frontend Development Server
```bash
cd frontend
npm run dev
```

3. Access the Application

* Frontend: http://localhost:5173 0r http://localhost:5174
  
* Backend API: http://localhost:8000

* API Documentation: http://localhost:8000/docs


## 📚 API Endpoints

### Students
* ```POST /students/``` - Create a new student

* ```GET /students/``` - Get all students

* ```GET /students/{id}``` - Get student by ID

* ```GET /students/{id}/courses/``` - Get courses for a student

### Courses
* ```POST /courses/``` - Create a new course

* ```GET /courses/``` - Get all courses

* ```GET /courses/{id}``` - Get course by ID

* ```GET /courses/{id}/students/``` - Get students enrolled in a course

### Enrollments
* ```POST /enroll/``` - Enroll student in course

* ```GET /enrollments/``` - Get all enrollments

### AI Features
* ```POST /genai/study-tips``` - Generate study tips for a course

### Health & Debug
* ```GET /``` - Welcome message

* ```GET /health``` - Health check

* ```GET /debug/endpoints``` - List all API endpoints


## 🛠️ Technology Stack
### Backend
* FastAPI - Modern, fast web framework for APIs

* SQLAlchemy - SQL toolkit and ORM

* SQLite - Lightweight database (production-ready with proper configuration)

* Pydantic - Data validation and settings management

* Groq SDK - AI inference for study tips generation

* Uvicorn - ASGI server for FastAPI


### Frontend
* Vue.js 3 - Progressive JavaScript framework

* Vite - Next-generation frontend tooling

* Axios - Promise-based HTTP client

* CSS3 - Modern styling with Flexbox and Grid

### Development Tools
* Python-dotenv - Environment variable management

* CORS Middleware - Cross-origin resource sharing

* Logging - Comprehensive application logging


## 🔧 Configuration

Environment Variables
Create a ```.env``` file in the ```api``` directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Database
The application uses SQLite with automatic table creation. The database file ```enrollment.db``` is created automatically on first run.

### CORS Configuration
Configured for development with multiple allowed origins. Update in main.py for production deployment.

## 📱 Usage Guide
### Adding Students
1. Navigate to "Student Management" section

2. Enter student name and email

3. Click "Add Student"

4. View all students in the modal table view

### Creating Courses
1. Navigate to "Course Management" section

2. Enter course details (title, code, credit units, description)

3. Click "Add Course"

4. View all courses in the modal table view


### Managing Enrollments
1. Select a student from the dropdown

2. Select a course from the dropdown

3. Click "Enroll Student"

4. View enrollments through student/course modals

### Generating Study Tips
1. Click "Tips" button next to any course

2. View AI-generated study recommendations

3. Tips are tailored to course credit units and subject


## 🔒 Security Considerations
* Input validation with Pydantic schemas

* SQL injection protection via SQLAlchemy ORM

* CORS configured for specific origins

* Environment variables for sensitive data

* Comprehensive error handling without exposing internals

## 📈 Performance
* FastAPI: High-performance async framework

* SQLite: Fast read operations suitable for moderate loads

* Vue.js: Optimized reactive updates

* Loading Modal: Modal-based content loading

## 🤝 Contributing
* Fork the repository

* Create a feature branch ```(git checkout -b feature/amazing-feature)```

* Commit changes ```(git commit -m 'Add amazing feature')```

* Push to branch ```(git push origin feature/amazing-feature)```

* Open a Pull Request


## 📄 License
This project is licensed under the ```MIT License``` - see the LICENSE file for details.

--- 
Built with ❤️ for academic institutions and educational technology
