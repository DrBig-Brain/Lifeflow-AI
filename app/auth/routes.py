from fastapi import APIRouter, HTTPException
from app.auth.model import RegisterRequest, LoginRequest, TokenResponse
from app.auth.database import users_collection
from app.auth.utils import hash_password, verify_password, create_access_token

router = APIRouter(prefix = "/auth", tags = ["auth"])

@router.post("/register")
async def register(request: RegisterRequest):

    existing = await users_collection.find_one({"username":request.username})
    if existing:
        raise HTTPException(status_code = 400, detail="Username already taken")

    existing_mail = await users_collection.find_one({"email": request.email})
    if existing_mail:
        raise HTTPException(status_code= 400, detail="Email already registered")

    await users_collection.insert_one({
        "username":request.username,
        "email":request.email,
        "password":hash_password(request.password),
    })
    return {"message":f"User {request.username} registered successfully"}

@router.post("/login",  response_model = TokenResponse)
async def login(request: LoginRequest):
    user= await users_collection.find_one({"username":request.username})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not verify_password(request.password, user["password"]):
        raise HTTPException(status_code = 401, detail="Invalid username or password")

    token = create_access_token({"sub":request.username})

    return TokenResponse(
        access_token = token,
        username = request.username
    )
