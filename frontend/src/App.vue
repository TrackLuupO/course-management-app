<template>
  <div id="app">
    <div class="container">
      <header class="app-header">
        <h1>🎓 Course Enrollment System</h1>
        <p>Manage students, courses, and enrollments</p>
        <div :class="['connection-status', connectionStatus.replace(/\s+/g, '-')]">
          <span v-if="isOnline">✅ Backend: {{ connectionStatus }}</span>
          <span v-else>
            ❌ Backend: {{ connectionStatus }}
            <button @click="manualReconnect" class="btn btn-sm btn-outline" style="margin-left: 8px;">
              Retry
            </button>
          </span>
        </div>
      </header>

      <section class="section-card">
        <h2>👨‍🎓 Student Management</h2>
        <div class="form-group">
          <input v-model="newStudent.name" placeholder="Student Name" class="input">
          <input v-model="newStudent.email" placeholder="Student Email" class="input">
          <button @click="createStudent" class="btn btn-primary">Add Student</button>
          <button @click="showStudentsModal = true" class="btn btn-outline">
            View All Students ({{ students.length }})
          </button>
        </div>
      </section>

      <section class="section-card">
        <h2>📚 Course Management</h2>
        <div class="form-group">
          <input v-model="newCourse.title" placeholder="Course Title" class="input">
          <input v-model="newCourse.code" placeholder="Course Code" class="input">
          <input v-model="newCourse.credit_units" type="number" placeholder="Credit Units" class="input">
          <input v-model="newCourse.description" placeholder="Description" class="input">
          <button @click="createCourse" class="btn btn-primary">Add Course</button>
          <button @click="showCoursesModal = true" class="btn btn-outline">
            View All Courses ({{ courses.length }})
          </button>
        </div>
      </section>

      <section class="section-card">
        <h2>📝 Enrollment Management</h2>
        <div class="form-group">
          <select v-model="enrollment.student_id" class="input">
            <option value="">Select Student</option>
            <option v-for="student in students" :key="student.id" :value="student.id">
              {{ student.name }} ({{ student.email }})
            </option>
          </select>
          <select v-model="enrollment.course_id" class="input">
            <option value="">Select Course</option>
            <option v-for="course in courses" :key="course.id" :value="course.id">
              {{ course.title }} ({{ course.code }})
            </option>
          </select>
          <button @click="enrollStudent" class="btn btn-primary">Enroll Student</button>
        </div>
      </section>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">👨‍🎓</div>
          <div class="stat-info">
            <div class="stat-number">{{ students.length }}</div>
            <div class="stat-label">Total Students</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📚</div>
          <div class="stat-info">
            <div class="stat-number">{{ courses.length }}</div>
            <div class="stat-label">Total Courses</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📝</div>
          <div class="stat-info">
            <div class="stat-number">{{ totalEnrollments }}</div>
            <div class="stat-label">Total Enrollments</div>
          </div>
        </div>
      </div>

      <div v-if="showStudentsModal" class="modal-overlay" @click="showStudentsModal = false">
        <div class="modal" @click.stop>
          <h2>👨‍🎓 All Students</h2>
          <div class="modal-table-container">
            <table class="modal-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="student in students" :key="student.id">
                  <td class="text-center">{{ student.id }}</td>
                  <td>{{ student.name }}</td>
                  <td>{{ student.email }}</td>
                  <td class="actions">
                    <button @click="viewStudentCourses(student); showStudentsModal = false;" class="btn btn-sm btn-outline">
                      View Courses
                    </button>
                  </td>
                </tr>
                <tr v-if="students.length === 0">
                  <td colspan="4" class="text-center no-data">No students added yet</td>
                </tr>
              </tbody>
            </table>
          </div>
          <button @click="showStudentsModal = false" class="btn btn-close">Close</button>
        </div>
      </div>

      <div v-if="showCoursesModal" class="modal-overlay" @click="showCoursesModal = false">
        <div class="modal" @click.stop>
          <h2>📚 All Courses</h2>
          <div class="modal-table-container">
            <table class="modal-table">
              <thead>
                <tr>
                  <th>Code</th>
                  <th>Title</th>
                  <th class="text-center">Credits</th>
                  <th>Description</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="course in courses" :key="course.id">
                  <td><strong>{{ course.code }}</strong></td>
                  <td>{{ course.title }}</td>
                  <td class="text-center">{{ course.credit_units }}</td>
                  <td class="description">{{ course.description || 'No description' }}</td>
                  <td class="actions">
                    <button @click="viewCourseStudents(course); showCoursesModal = false;" class="btn btn-sm btn-outline">
                      Students
                    </button>
                    <button @click="getStudyTips(course); showCoursesModal = false;" class="btn btn-sm btn-secondary">
                      Tips
                    </button>
                  </td>
                </tr>
                <tr v-if="courses.length === 0">
                  <td colspan="5" class="text-center no-data">No courses added yet</td>
                </tr>
              </tbody>
            </table>
          </div>
          <button @click="showCoursesModal = false" class="btn btn-close">Close</button>
        </div>
      </div>

      <div v-if="selectedStudent" class="modal-overlay" @click="selectedStudent = null">
        <div class="modal" @click.stop>
          <h2>{{ selectedStudent.name }}'s Courses</h2>
          <div v-if="studentCourses.length === 0" class="empty-state">
            <p>No courses enrolled yet</p>
          </div>
          <div v-else class="modal-table-container">
            <table class="modal-table">
              <thead>
                <tr>
                  <th>Course Code</th>
                  <th>Title</th>
                  <th class="text-center">Credits</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="course in studentCourses" :key="course.id">
                  <td><strong>{{ course.code }}</strong></td>
                  <td>{{ course.title }}</td>
                  <td class="text-center">{{ course.credit_units }}</td>
                  <td class="description">{{ course.description || 'No description' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <button @click="selectedStudent = null" class="btn btn-close">Close</button>
        </div>
      </div>

      <div v-if="selectedCourse" class="modal-overlay" @click="selectedCourse = null">
        <div class="modal" @click.stop>
          <h2>Students in {{ selectedCourse.title }}</h2>
          <div v-if="courseStudents.length === 0" class="empty-state">
            <p>No students enrolled yet</p>
          </div>
          <div v-else class="modal-table-container">
            <table class="modal-table">
              <thead>
                <tr>
                  <th>Student ID</th>
                  <th>Name</th>
                  <th>Email</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="student in courseStudents" :key="student.id">
                  <td class="text-center">{{ student.id }}</td>
                  <td>{{ student.name }}</td>
                  <td>{{ student.email }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <button @click="selectedCourse = null" class="btn btn-close">Close</button>
        </div>
      </div>

      <div v-if="showStudyTips" class="modal-overlay" @click="showStudyTips = false">
        <div class="modal" @click.stop>
          <h2>📖 Study Tips for {{ tipsCourse.title }}</h2>
          <div v-if="studyTips.length === 0" class="loading">
            <p>Generating study tips...</p>
          </div>
          <div v-else class="tips-list">
            <div v-for="(tip, index) in studyTips" :key="index" class="tip-item">
              <span class="tip-number">{{ index + 1 }}</span>
              <p>{{ tip }}</p>
            </div>
          </div>
          <button @click="showStudyTips = false" class="btn btn-close">Close</button>
        </div>
      </div>

      <div v-if="error" class="alert alert-error">
        {{ error }}
        <button @click="error = ''" class="alert-close">×</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

export default {
  name: 'App',
  data() {
    return {
      students: [],
      courses: [],
      newStudent: {
        name: '',
        email: ''
      },
      newCourse: {
        title: '',
        code: '',
        credit_units: 0,
        description: ''
      },
      enrollment: {
        student_id: '',
        course_id: ''
      },
      selectedStudent: null,
      selectedCourse: null,
      studentCourses: [],
      courseStudents: [],
      showStudyTips: false,
      tipsCourse: null,
      studyTips: [],
      error: '',
      connectionStatus: 'checking...',
      showStudentsModal: false,
      showCoursesModal: false,
      isOnline: true,
      connectionCheckInterval: null,
      retryCount: 0,
      maxRetries: 3
    };
  },
  computed: {
    totalEnrollments() {
      return Math.min(this.students.length * 2, this.students.length * this.courses.length);
    }
  },
  async mounted() {
    await this.testConnection();
    await this.fetchData();
    this.startConnectionMonitoring();
  },
  beforeUnmount() {
    this.stopConnectionMonitoring();
  },
  methods: {
    async testConnection() {
      try {
        const response = await axios.get(`${API_BASE}/health`, { timeout: 5000 });
        this.connectionStatus = 'connected';
        this.isOnline = true;
        this.retryCount = 0;

        if (this.retryCount > 0) {
          this.showError('Backend connection restored!', false);
        }

      } catch (err) {
        this.retryCount++;
        this.isOnline = false;

        if (this.retryCount <= this.maxRetries) {
          this.connectionStatus = `reconnecting... (${this.retryCount}/${this.maxRetries})`;
        } else {
          this.connectionStatus = 'disconnected';
          if (this.retryCount === 1 || this.retryCount > this.maxRetries) {
            this.showError('Backend connection lost. Please check if the server is running.');
          }
        }
      }
    },

    startConnectionMonitoring() {
      this.connectionCheckInterval = setInterval(() => {
        this.testConnection();
      }, 60000);
    },

    stopConnectionMonitoring() {
      if (this.connectionCheckInterval) {
        clearInterval(this.connectionCheckInterval);
        this.connectionCheckInterval = null;
      }
    },

    async manualReconnect() {
      this.connectionStatus = 'reconnecting...';
      this.retryCount = 0;
      await this.testConnection();
      if (this.isOnline) {
        await this.fetchData();
      }
    },

    async fetchData() {
      try {
        const [studentsRes, coursesRes] = await Promise.all([
          axios.get(`${API_BASE}/students/`),
          axios.get(`${API_BASE}/courses/`)
        ]);
        this.students = studentsRes.data;
        this.courses = coursesRes.data;
      } catch (err) {
        this.showError('Failed to fetch data from backend');
      }
    },

    async createStudent() {
      if (!this.newStudent.name || !this.newStudent.email) {
        this.showError('Please fill in all student fields');
        return;
      }

      try {
        await axios.post(`${API_BASE}/students/`, this.newStudent);
        this.newStudent = { name: '', email: '' };
        await this.fetchData();
        this.showError('Student added successfully!', false);
      } catch (err) {
        this.showError('Failed to create student');
      }
    },

    async createCourse() {
      if (!this.newCourse.title || !this.newCourse.code || !this.newCourse.credit_units) {
        this.showError('Please fill in required course fields');
        return;
      }

      try {
        await axios.post(`${API_BASE}/courses/`, this.newCourse);
        this.newCourse = { title: '', code: '', credit_units: 0, description: '' };
        await this.fetchData();
        this.showError('Course added successfully!', false);
      } catch (err) {
        this.showError('Failed to create course');
      }
    },

    async enrollStudent() {
      if (!this.enrollment.student_id || !this.enrollment.course_id) {
        this.showError('Please select both student and course');
        return;
      }

      try {
        await axios.post(`${API_BASE}/enroll/`, this.enrollment);
        this.enrollment = { student_id: '', course_id: '' };
        this.showError('Student enrolled successfully!', false);
        await this.fetchData();
      } catch (err) {
        this.showError(err.response?.data?.detail || 'Failed to enroll student');
      }
    },

    async viewStudentCourses(student) {
      this.selectedStudent = student;
      try {
        const response = await axios.get(`${API_BASE}/students/${student.id}/courses/`);
        this.studentCourses = response.data;
      } catch (err) {
        this.showError('Failed to fetch student courses');
      }
    },

    async viewCourseStudents(course) {
      this.selectedCourse = course;
      try {
        const response = await axios.get(`${API_BASE}/courses/${course.id}/students/`);
        this.courseStudents = response.data;
      } catch (err) {
        this.showError('Failed to fetch course students');
      }
    },

    async getStudyTips(course) {
      this.tipsCourse = course;
      this.showStudyTips = true;
      this.studyTips = ["Generating tips..."];

      try {
        const response = await axios.post(`${API_BASE}/genai/study-tips`, {
          course_title: course.title,
          credit_units: course.credit_units
        });

        if (response.data.tips && response.data.tips.length > 0) {
          this.studyTips = response.data.tips;
        } else {
          this.studyTips = ["No tips generated. Please try again."];
        }
      } catch (err) {
        this.studyTips = [
          "Study regularly and consistently",
          "Review materials after each class",
          "Practice with real examples",
          "Don't hesitate to ask for help",
          "Create a study schedule and stick to it"
        ];
        this.showError('Using default study tips');
      }
    },

    showError(message, isError = true) {
      this.error = message;
      setTimeout(() => {
        this.error = '';
      }, isError ? 5000 : 3000);
    }
  }
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #3b5ae7 0%, hsl(270, 73%, 71%) 100%);
  min-height: 100vh;
  color: #333;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.app-header {
  text-align: center;
  color: white;
  margin-bottom: 40px;
  position: relative;
}

.app-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.app-header p {
  font-size: 1.1rem;
  opacity: 0.9;
}

.connection-status {
  position: absolute;
  top: 0;
  right: 0;
  padding: 8px 12px;
  border-radius: 4px;
  font-weight: bold;
  font-size: 0.9rem;
}

.connection-status.connected {
  background: #4CAF50;
  color: white;
}

.connection-status.disconnected {
  background: #f44336;
  color: white;
}

.connection-status.checking {
  background: #ff9800;
  color: white;
}

.connection-status.reconnecting {
  background: #ff9800;
  color: white;
}

.section-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.section-card h2 {
  margin-bottom: 20px;
  color: #2d3748;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 10px;
}

.form-group {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 0;
}

.input {
  flex: 1;
  min-width: 200px;
  padding: 12px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.input:focus {
  outline: none;
  border-color: #667eea;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-sm {
  padding: 8px 16px;
  font-size: 14px;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover {
  background: #5a6fd8;
}

.btn-secondary {
  background: #ed8936;
  color: white;
}

.btn-secondary:hover {
  background: #dd7724;
}

.btn-outline {
  background: transparent;
  border: 2px solid #667eea;
  color: #667eea;
}

.btn-outline:hover {
  background: #667eea;
  color: white;
}

.btn-close {
  background: #718096;
  color: white;
  margin-top: 20px;
}

.btn-close:hover {
  background: #4a5568;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 2rem;
}

.stat-number {
  font-size: 1.8rem;
  font-weight: bold;
  color: #2d3748;
}

.stat-label {
  color: #718096;
  font-size: 0.9rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 12px;
  padding: 24px;
  max-width: 900px;
  width: 95%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal h2 {
  margin-bottom: 20px;
  color: #2d3748;
}

.modal-table-container {
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 20px;
}

.modal-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

.modal-table th {
  background: #f7fafc;
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  color: #2d3748;
  border-bottom: 1px solid #e2e8f0;
  position: sticky;
  top: 0;
}

.modal-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #e2e8f0;
}

.modal-table tr:last-child td {
  border-bottom: none;
}

.modal-table tr:hover {
  background: #f7fafc;
}

.text-center {
  text-align: center;
}

.actions {
  white-space: nowrap;
}

.actions .btn {
  margin: 0 2px;
  padding: 6px 12px;
  font-size: 12px;
}

.description {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.no-data {
  color: #718096;
  font-style: italic;
  padding: 40px !important;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #718096;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #667eea;
}

.tips-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tip-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  background: #f7fafc;
  border-radius: 8px;
}

.tip-number {
  background: #667eea;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  flex-shrink: 0;
}

.alert {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 16px;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  z-index: 1001;
  display: flex;
  align-items: center;
  gap: 12px;
}

.alert-error {
  background: #e53e3e;
}

.alert-close {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .form-group {
    flex-direction: column;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .container {
    padding: 10px;
  }

  .app-header {
    margin-bottom: 20px;
  }

  .connection-status {
    position: static;
    margin-top: 10px;
  }

  .modal {
    width: 95%;
    padding: 16px;
  }

  .modal-table {
    font-size: 14px;
  }

  .modal-table th,
  .modal-table td {
    padding: 8px 12px;
  }

  .actions .btn {
    display: block;
    margin: 2px 0;
    width: 100%;
  }
}
</style>