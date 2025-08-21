import json
import sqlite3
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

DB_NAME = "recipes.db"
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cuisine TEXT,
    title TEXT,
    rating REAL,
    prep_time INTEGER,
    cook_time INTEGER,
    total_time INTEGER,
    description TEXT,
    nutrients TEXT,
    serves TEXT
);
""")

def load_data():
    with open("US_recipes.json", "r") as f:
        data = json.load(f)

    for _, recipe in data.items():
        def clean_num(x):
            return None if (x is None or str(x).lower() == "nan") else x

        cuisine = recipe.get("cuisine")
        title = recipe.get("title")
        rating = clean_num(recipe.get("rating"))
        prep_time = clean_num(recipe.get("prep_time"))
        cook_time = clean_num(recipe.get("cook_time"))
        total_time = clean_num(recipe.get("total_time"))
        description = recipe.get("description")
        nutrients = json.dumps(recipe.get("nutrients"))
        serves = recipe.get("serves")

        cursor.execute("""
            INSERT INTO recipes (cuisine, title, rating, prep_time, cook_time, total_time, description, nutrients, serves)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (cuisine, title, rating, prep_time, cook_time, total_time, description, nutrients, serves))

    conn.commit()

# Uncomment this on first run to load data
# load_data()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/recipes")
def get_recipes(page: int = 1, limit: int = 10):
    offset = (page - 1) * limit
    cursor.execute("SELECT COUNT(*) FROM recipes")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT id, title, cuisine, rating, prep_time, cook_time, total_time, description, nutrients, serves
        FROM recipes
        ORDER BY rating DESC
        LIMIT ? OFFSET ?
    """, (limit, offset))
    rows = cursor.fetchall()

    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "title": row[1],
            "cuisine": row[2],
            "rating": row[3],
            "prep_time": row[4],
            "cook_time": row[5],
            "total_time": row[6],
            "description": row[7],
            "nutrients": json.loads(row[8]),
            "serves": row[9]
        })

    return {"page": page, "limit": limit, "total": total, "data": data}

@app.get("/api/recipes/search")
def search_recipes(
    title: Optional[str] = None,
    cuisine: Optional[str] = None,
    rating: Optional[float] = Query(None, description=">= rating"),
    total_time: Optional[int] = Query(None, description="<= total time"),
    calories: Optional[int] = Query(None, description="<= calories")
):
    query = "SELECT id, title, cuisine, rating, prep_time, cook_time, total_time, description, nutrients, serves FROM recipes WHERE 1=1"
    params = []

    if title:
        query += " AND title LIKE ?"
        params.append(f"%{title}%")
    if cuisine:
        query += " AND cuisine = ?"
        params.append(cuisine)
    if rating:
        query += " AND rating >= ?"
        params.append(rating)
    if total_time:
        query += " AND total_time <= ?"
        params.append(total_time)

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()

    data = []
    for row in rows:
        nutrients = json.loads(row[8]) if row[8] else {}
        if calories:
            cal_val = int(nutrients.get("calories", "0").split()[0]) if nutrients.get("calories") else 0
            if cal_val > calories:
                continue
        data.append({
            "id": row[0],
            "title": row[1],
            "cuisine": row[2],
            "rating": row[3],
            "prep_time": row[4],
            "cook_time": row[5],
            "total_time": row[6],
            "description": row[7],
            "nutrients": nutrients,
            "serves": row[9]
        })

    return {"data": data}
