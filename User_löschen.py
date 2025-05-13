from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Dict
from datetime import datetime 
import bcrypt 


app = FastAPI()
user_db: Dict[str, "User"] = {}


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    name:str
    email: EmailStr 


class User:

    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password_hash = self.hash_password(password)
        self.created_at = datetime.now().isoformat()

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


@app.post("/users", response_model=UserResponse)
def create_user(data: UserCreate):
    email = data.email.lower()
    if email in user_db:
        raise HTTPException(status_code=400, detail="E-Mail bereits registriert")

    user = User(data.name, email, data.password)
    user_db[email] = user
    return{"name": user.name, "email": user.email}


@app.get("/users/{email}", response_model=UserResponse)
def get_user(email:str):
    email = email.lower()
    if email not in user_db:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    
    user = user_db[email]
    return{"name": user.name, "email": user.email}


@app.delete("/users/{email}")
def delete_user(email: str):
    email = email.lower()
    if email not in user_db:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    
    del user_db[email]
    return{"message": f"Benutzer {email} wurde erfolgreich gelöscht."}

