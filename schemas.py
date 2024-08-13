from pydantic import BaseModel, EmailStr
from typing import ClassVar, Optional

# مودل إنشاء مستخدم جديد
class UserCreate(BaseModel):
    username: str
    name: str
    email: EmailStr
    password: str
    phone : str


# مودل عرض بيانات المستخدم
class User(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    phone : str

    class Config:
        orm_mode = True

# مودل التوكن المستخدم في تسجيل الدخول
class Token(BaseModel):
    access_token: str
    token_type: str

# مودل التوكن المستخدم في بيانات المستخدم
class TokenData(BaseModel):
    username: Optional[str] = None

# مودل إنشاء دكتور جديد
class DoctorCreate(BaseModel):
    name: str
    phone: str
    specialty: str
    latitude :  Optional[float] = None 
    longitude :  Optional[float] = None 
    rating: Optional[float] = None 
    experience : int
    bio : str
    profileImageUrl :   Optional[str] = None 
# مودل عرض بيانات الدكتور
class Doctor(BaseModel):
    id: int
    name: str
    phone: str
    specialty: str
    rating: Optional[float]
    experience : int
    bio : int
    profileImageUrl : str

    class Config:
        orm_mode = True

# مودل إنشاء تقييم لدكتور
class RatingCreate(BaseModel):
    doctor_id: int
    rating: float
    review: Optional[str] = None
    image_url: Optional[str] = None

# مودل عرض بيانات التقييم
class Rating(BaseModel):
    id: int
    doctor_id: int
    rating: float
    review: Optional[str]

    class Config:
        orm_mode = True

# مودل الإعلان
class AdCreate(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None  

class Ad(BaseModel):
    id: int
    title: str
    content: str
    image_url: Optional[str] = None  # مسار الصورة (اختياري)

    class Config:
        orm_mode = True

# مودل الفلاتر لجلب الدكاترة حسب الفلتر
class DoctorFilter(BaseModel):
    specialization: Optional[str] = None
    min_rating: Optional[float] = None
