import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re
from fastapi.openapi.models import EmailStr

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


class User:

    def __init__(self, name: str, email: str, password: str, role: str):
        self.validate(name, email, password)
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.role = role
        self.password_hash = self.hash_password(password)
        self.active = True
        self.created_at = datetime.now().strftime(DATE_FORMAT)
        self.updated_at = self.created_at

    @staticmethod
    def validate(name, email, password):
        if email in users_by_email:
            raise ValueError(f"E-Mail '{email}' ist bereits registriert.")
        if not (3 <= len(name) <= 20):
            raise ValueError("Benutzername muss zwischen 3 und 20 Zeichen lang sein.")
        if len(password) < 10 or not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password):
            raise ValueError("Passwort muss ≥10 Zeichen, Groß- und Kleinbuchstaben enthalten.")

    @staticmethod
    def hash_password(password):
        return f"hashed({password})"  # Platzhalter (bcrypt kannst du bei Bedarf einbauen)


@app.post("/users", response_model=UserResponse)
def create_user(data: UserCreate):
    try:
        user = User(data.name, data.email, data.password, data.role)
        users_by_email[user.email] = user
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            active=user.active,
            created_at=user.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

