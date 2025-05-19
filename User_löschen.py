from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime 
import bcrypt 
import re
import uuid
from typing import Optional   

app = FastAPI()
users_by_email = {}
DATE_FORMAT = "%d.%m.%Y %H:%M:%S"


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str


class UserResponse(BaseModel):
    id: str
    name: str 
    email: EmailStr
    role: str
    active: bool
    created_at: str
    deleted_at: Optional[str] = None  


class User:

    def __init__(self, name: str, email: str, password: str, role: str):
        self.validate(name, email, password)
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.role = role 
        self.active = True 
        self.created_at = datetime.now().strftime(DATE_FORMAT)
        self.password_hash = self.hash_password(password)
        self.deleted_at = None 

    @staticmethod
    def validate(name, email, password):
        if email in users_by_email:
            raise ValueError(f"E-Mail '{email}' ist bereits registriert.")
        if not (3 <= len(name) <= 20):
            raise ValueError("Benutzername muss zwischen 3 und 20 Zeichen lang sein.")
        if len(password) < 10 or not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password):
            raise ValueError("Passwort muss ≥10 Zeichen, Groß- und Kleinbuchstaben enthalten.")

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


@app.post("/users", response_model=UserResponse)
def create_user(data: UserCreate):
    email = data.email.lower()
    if email in users_by_email:
        raise HTTPException(status_code=400, detail="E-Mail bereits registriert")

    user = User(data.name, email, data.password, data.role)
    users_by_email[email] = user
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        active=user.active,
        created_at=user.created_at,
        deleted_at=user.deleted_at,
    )


@app.get("/users/{email}", response_model=UserResponse)
def get_user(email:str):
    email = email.lower()
    if email not in users_by_email:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    
    user = users_by_email[email]
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        active=user.active,
        created_at=user.created_at,
        deleted_at=user.deleted_at,
    )


@app.delete("/users/{email}", response_model=UserResponse)
def delete_user(email: str):
    email = email.lower()
    if email not in users_by_email:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    
    user = users_by_email[email]
    user.active = False
    user.deleted_at = datetime.now().strftime(DATE_FORMAT)
    
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        active=user.active,
        created_at=user.created_at,
        deleted_at=user.deleted_at
    )
