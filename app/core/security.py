from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def password_hash(password : str)->str:
    return pwd_context.hash(password)

def verify_password(password:str, hashed: str):
    return pwd_context.verify(password, hashed)
KEY = settings.SECRET_KEY
Algo = settings.ALGORITHM

def create_token(username:str):
    exp = datetime.utcnow()+ timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub" : username, "exp": exp}
    return jwt.encode(data,KEY, algorithm=Algo)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, KEY, algorithms=[Algo])
        username = payload.get("sub")
        if not username:
            return None
        return username
    except:
        return None
    