from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user, get_user_by_email

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=UserResponse)
async def signup(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # socho: pehle check karo email already exist toh nahi karta
    # agar karta hai, HTTPException raise karo (400/409)
    # nahi toh create_user() call karo, return karo
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registerd")
    new_user = await create_user(db, user_data)
    return new_user

from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import verify_password, create_token

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # Step 1: form_data.username se user dhoondo (note: form mein field ka naam "username" hota hai, 
    # even though tum email use kar rahe ho)
    user = await get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Step 2: agar user nahi mila -> raise HTTPException(401, "Invalid credentials")
    # Step 3: verify_password(form_data.password, user.password_hash) check karo
    pwd= verify_password(form_data.password, user.password_hash)
    if not pwd:
        raise HTTPException(401, "Invalid credentials") 
    # Step 4: agar match nahi -> raise HTTPException(401, "Invalid credentials")  
    # Step 5: create_token(user.email) call karo, token banao
    token = create_token(user.email)
    # Step 6: return {"access_token": token, "token_type": "bearer"}
    return {"access_token": token, "token_type": "bearer"}