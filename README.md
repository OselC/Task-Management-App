# 🗂️ Task Management System

A full-stack **Task Management System** built with **Flask (Backend)** and **Vue.js + Vite (Frontend)**.  
This application allows users to authenticate using JWT and perform CRUD operations on tasks.

---

## 🚀 Tech Stack

### Backend
- Python
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- PostgreSQL
- Psycopg2
- Flask-CORS

### Frontend
- Vue 3
- Vite
- Axios
- Vue Router
- CSS

---

## 🔐 Authentication

- Authentication uses **JWT (JSON Web Token)**
- Token is generated on login and stored in `localStorage`
- Protected routes require a valid JWT in the request header

---

## 📡 API Endpoints

### Auth
| Method | Endpoint | Description |
|------|---------|-------------|
| POST | `/api/auth/login` | User login |

### Tasks
| Method | Endpoint | Description |
|------|---------|-------------|
| GET | `/api/tasks` | Get all tasks |
| POST | `/api/tasks` | Create a new task |

---

## 🛠️ Backend Setup

### 1️⃣ Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2️⃣ Configure PostgreSQL
create database:
```sql
CREATE DATABASE taskdb;
```

### 3️⃣ Run backend server
```bash
python run.py
```

Backend runs on:
```cpp
http://127.0.0.1:5000
```

## 🎨 Frontend Setup
### 1️⃣ Install dependencies
```bash
cd frontend
npm install
```

### 2️⃣ Run frontend
```bash
npm run dev
```

Frontend runs on:
```arduino
http://localhost:5173
```

### 🧪 Default Login Credentials
```makefile
Username: admin
Password: admin123
```
