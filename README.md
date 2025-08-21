# 🍽️ US Recipes Dashboard

This project is a submission for the **Securin Assessment**.  
It provides a FastAPI backend with a SQLite database and a React frontend to browse, search, and filter recipes.

---

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/securin-assessment.git
cd securin-assessment
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\\Scripts\\activate    # (Windows)
pip install -r requirements.txt
```

#### Initialize Database
```bash
sqlite3 recipes.db < schema.sql
```

#### Load Data
- Place `US_recipes.json` inside the backend folder.
- Open `main.py` and **uncomment** `load_data()` once.
- Run the server once, data will load, then comment it back.

#### Run Backend
```bash
uvicorn main:app --reload --port 8000
```
Backend will run at: **http://localhost:8000**

---

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend will run at: **http://localhost:5173**

---

## 🔗 API Endpoints

### Get Recipes (Paginated, Sorted by Rating)
```
GET http://localhost:8000/api/recipes?page=1&limit=15
```

### Search Recipes
```
GET http://localhost:8000/api/recipes/search?title=chicken&cuisine=Indian&rating=4&total_time=60&calories=400
```

---

## 📊 Testing APIs

You can test APIs using **curl** or **Postman**.

Example:
```bash
curl "http://localhost:8000/api/recipes?page=1&limit=10"
curl "http://localhost:8000/api/recipes/search?cuisine=Italian&rating=4.5"
```

---

## ✅ Features Implemented
- SQLite database schema & script included.
- Backend API with pagination, sorting, search.
- React frontend with:
  - Pagination (15/25/50 per page)
  - Filters (title, cuisine, rating, calories, total time)
  - Drawer with full recipe details
  - Expandable prep/cook times
  - Nutrients table

---

## 📦 Future Improvements
- Dockerfile & docker-compose for full-stack containerization.
- Switch SQLite → PostgreSQL in production.
- Add unit tests with pytest & httpx.
