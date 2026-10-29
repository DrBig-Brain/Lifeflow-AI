from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt 
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials= Depends(bearer_scheme)) -> str:
    token = credentials.credentials
    payload = decode_acces_token(token)
    if payload is None:
        raise HTTPException(status_code = 401, detail="Invalid or expire token")
    return payload["sub"]


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
def verify_password(plain:str ,hashed:str) -> bool:
    return pwd_context.verify(plain, hashed)
def create_access_token(data:dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

def decode_acces_token(token:str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
    except JWTError:
        return None