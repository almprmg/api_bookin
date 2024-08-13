from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table,Text,Boolean
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel


# جدول الأطباء
class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, unique=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    specialty = Column(String, index=True)
    rating = Column(Float, nullable=True)
    reviewCount = Column(Integer, nullable=True)
    patientCount = Column(Integer, nullable=True)
    experience = Column(Integer, nullable=True)
    bio = Column(String, nullable=True)
    profileImageUrl = Column(String, nullable=True)
    ratings = relationship("Rating", back_populates="doctor")

# جدول المستخدمين
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String)
    phone = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True, index=True, nullable=True)

    ratings = relationship("Rating", back_populates="user")

# جدول التقييمات
class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Float, nullable=False)
    image_url = Column(String, nullable=False)
    approved = Column(Boolean, default=False)

    doctor = relationship("Doctor", back_populates="ratings")
    user = relationship("User", back_populates="ratings")

# جدول الإعلانات
class Ad(Base):
    __tablename__ = "ads"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    image_url = Column(String, nullable=True)  # حقل لتخزين مسار الصورة

# جدول الفلاتر
class Filter(Base):
    __tablename__ = "filters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # اسم الفلتر (مثلاً، التخصص)
    value = Column(String, index=True)  # قيمة الفلتر (مثلاً، "قلب")


class Token(BaseModel):
    access_token: str
    token_type: str
