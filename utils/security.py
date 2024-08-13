from passlib.context import CryptContext
from datetime import datetime, timedelta
import  jwt
from jwt.exceptions import  PyJWTError

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session
from app import crud, database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# إنشاء سياق للتجزئة
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    تقوم هذه الدالة بتجزئة كلمة المرور باستخدام Bcrypt.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    تقوم هذه الدالة بالتحقق من أن كلمة المرور المدخلة تتطابق مع كلمة المرور المجزأة المخزنة.
    """
    return pwd_context.verify(plain_password, hashed_password)



SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except PyJWTError:
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = verify_access_token(token, credentials_exception)
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user
