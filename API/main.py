from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import sqlite3

# ==================== NEW DAY 7 ====================
# Password hashing
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
# ====================================================


# ==================== NEW DAY 7 ====================
# JWT + Bearer Authentication

import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends

# Secret key used to sign JWT tokens
# In a real application, keep this in an environment variable.
SECRET_KEY = "my-super-secret-key"

# Algorithm used to sign the JWT
ALGORITHM = "HS256"

# Token lifetime
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Tells FastAPI to expect:
# Authorization: Bearer <token>
security = HTTPBearer()
# ====================================================


app = FastAPI()


# ---------------- DATABASE + TABLE ----------------

connection = sqlite3.connect("users.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
)
""")

# ==================== NEW DAY 7 ====================
# Create authentication table
cursor.execute("""
CREATE TABLE IF NOT EXISTS auth_users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
)
""")
# ====================================================

connection.commit()
connection.close()


# ---------------- HOME ----------------

@app.get("/")
def home():
    return {"message": "Hello World"}


# ---------------- GET USERS ----------------

@app.get("/users")
def get_users():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    connection.close()

    return users


# ---------------- POST USER ----------------

class User(BaseModel):
    name: str
    age: int = Field(gt=0)


@app.post("/users")
def create_user(user: User):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO users (name, age) VALUES (?, ?)",
        (user.name, user.age)
    )

    connection.commit()
    connection.close()

    return {"message": "User created"}


# ---------------- UPDATE USER ----------------

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE users SET name = ?, age = ? WHERE id = ?",
        (user.name, user.age, user_id)
    )

    rows_updated = cursor.rowcount

    connection.commit()
    connection.close()

    print("Rows updated:", rows_updated)

    if rows_updated == 0:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User updated",
        "rows_updated": rows_updated
    }


# ---------------- DELETE USER ----------------

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )

    rows_deleted = cursor.rowcount

    connection.commit()
    connection.close()

    print("Rows deleted:", rows_deleted)

    if rows_deleted == 0:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted",
        "rows_deleted": rows_deleted
    }


# ---------------- GET USER BY ID ----------------

@app.get("/users/{user_id}")
def get_user(user_id: int):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    connection.close()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# =========================================================
# ==================== DAY 7 START ========================
# ==================== REGISTER ===========================
# =========================================================


# ==================== NEW DAY 7 ====================
# Data we expect when someone registers

class RegisterUser(BaseModel):
    username: str
    password: str
# ====================================================


# ==================== NEW DAY 7 ====================
# REGISTER ENDPOINT
#
# Client sends:
#
# {
#     "username": "utkarsh",
#     "password": "mypassword"
# }
#
# We hash the password BEFORE storing it.
# ====================================================

@app.post("/register")
def register_user(user: RegisterUser):

    # ---------- NEW DAY 7 ----------
    # Hash the password
    hashed_password = password_hash.hash(user.password)
    # --------------------------------

    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    try:

        # ---------- NEW DAY 7 ----------
        # Store username + HASHED password
        cursor.execute(
            """
            INSERT INTO auth_users (username, password_hash)
            VALUES (?, ?)
            """,
            (user.username, hashed_password)
        )
        # --------------------------------

        connection.commit()

    except sqlite3.IntegrityError:

        # ---------- NEW DAY 7 ----------
        # Username already exists
        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )
        # --------------------------------

    connection.close()

    return {
        "message": "User registered successfully"
    }


# =========================================================
# ==================== LOGIN ===============================
# =========================================================


# ==================== NEW DAY 7 ====================
# Data we expect when someone logs in

class LoginUser(BaseModel):
    username: str
    password: str
# ====================================================


# ==================== NEW DAY 7 ====================
# LOGIN ENDPOINT
#
# Client sends:
#
# {
#     "username": "utkarsh",
#     "password": "mypassword"
# }
#
# We:
# 1. Find username
# 2. Get password hash
# 3. Verify password
# 4. Create JWT
# ====================================================

@app.post("/login")
def login_user(user: LoginUser):

    # ---------- NEW DAY 7 ----------
    # Connect to database
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    # Find username
    cursor.execute(
        "SELECT * FROM auth_users WHERE username = ?",
        (user.username,)
    )

    stored_user = cursor.fetchone()

    connection.close()
    # --------------------------------


    # ---------- NEW DAY 7 ----------
    # Username doesn't exist

    if stored_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    # --------------------------------


    # ---------- NEW DAY 7 ----------
    # Get password hash

    stored_password_hash = stored_user[2]
    # --------------------------------


    # ---------- NEW DAY 7 ----------
    # Verify password

    password_correct = password_hash.verify(
        user.password,
        stored_password_hash
    )
    # --------------------------------


    # ---------- NEW DAY 7 ----------
    # Password incorrect

    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    # --------------------------------


    # =====================================================
    # ==================== JWT =============================
    # =====================================================

    # ---------- NEW DAY 7 ----------
    # Set expiration time

    expiration_time = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    # --------------------------------


    # ---------- NEW DAY 7 ----------
    # Data stored inside JWT

    token_data = {
        "sub": user.username,
        "exp": expiration_time
    }
    # --------------------------------


    # ---------- NEW DAY 7 ----------
    # Create JWT token

    access_token = jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    # --------------------------------


    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }


# =========================================================
# ==================== JWT VERIFICATION ====================
# =========================================================


# ==================== NEW DAY 7 ====================
# This function checks whether the JWT is valid.
#
# It will be used by protected endpoints.
# ====================================================

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    # ---------- NEW DAY 7 ----------
    # Get token from:
    #
    # Authorization: Bearer <token>

    token = credentials.credentials
    # --------------------------------


    try:

        # ---------- NEW DAY 7 ----------
        # Decode and verify JWT

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        # --------------------------------


        # ---------- NEW DAY 7 ----------
        # Get username from JWT

        username = payload.get("sub")
        # --------------------------------


        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return username

    except jwt.ExpiredSignatureError:

        # ---------- NEW DAY 7 ----------
        # Token has expired

        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
        # --------------------------------

    except jwt.InvalidTokenError:

        # ---------- NEW DAY 7 ----------
        # Token is invalid

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
        # --------------------------------


# =========================================================
# ==================== PROTECTED ENDPOINT ==================
# =========================================================


# ==================== NEW DAY 7 ====================
# PROTECTED ENDPOINT
#
# You must provide a valid JWT to access this endpoint.
#
# Swagger:
#
# Authorize 
#     ↓
# Bearer token
#     ↓
# GET /protected
# ====================================================

@app.get("/protected")
def protected_route(username: str = Depends(verify_token)):

    return {
        "message": "You accessed a protected endpoint",
        "username": username
    }

# =========================================================
# ==================== END DAY 7 ==========================
# =========================================================