import os
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from database import Base

from models import Ad, User ,Doctor,Rating
import schemas 
from utils.security import hash_password
from utils.validators import validate_is_he, validate_unique_email, validate_unique_username
import shutil
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    validate_unique_username(db=db,username=user.username)
    validate_unique_email(db=db,email=user.email)
    db_user = User(username=user.username,phone=user.phone, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(user_id: int, db: Session, updated_user, token_id):
    validate_is_he(user_id, token_id)

    validate_unique_username(db=db, username = updated_user.username,id=user_id )

    validate_unique_email(db=db, email = updated_user.email, id=user_id)
    user =  __get_table(db=db,table=User,id=user_id)
    if user:
        user.username = updated_user.username
        user.password = hash_password(updated_user.password)
        user.email = updated_user.email
        db.commit()
        db.refresh(user)
       

        return True
    return False
    
def delete_acount(user_id: int,token_id:int,table :Base  ,  db: Session):

    validate_is_he(user_id,token_id)
    user = __get_table(db=db,table=table,id=user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
    

def get_user_by_username(db: Session, username: str):
    """
    هذه الدالة تسترجع مستخدم من قاعدة البيانات بناءً على اسم المستخدم.
    """
    return db.query(User).filter(User.username == username).first()



def create_doctor(db: Session, doctor: schemas.DoctorCreate):
    db_doctor = Doctor(name=doctor.name,phone=doctor.phone,specialty=doctor.specialty,experience=doctor.experience,bio=doctor.bio)
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


def get_doctors(db: Session,specialty:str):
    print(specialty)
    if specialty:
        doctors = db.query(Doctor).filter(Doctor.specialty == specialty).all()
    else:
        doctors = db.query(Doctor).all()
    return doctors


def get_doctor(db: Session,doctor_id:str):
    
    return __get_table(db=db,table=Doctor,id=doctor_id)

def __get_table(db:Session,table : Base ,id ):
    row = db.query(table).filter(table.id == id).first()
    return row

def create_rating(db: Session, db_rating: schemas.RatingCreate, user_id: int):
    """
    تقوم هذه الدالة بإنشاء تقييم جديد لدكتور معين وتحديث متوسط التقييمات.
    """
    # إنشاء التقييم الجديد
    db_rating = Rating(
        doctor_id=db_rating.doctor_id,
        user_id=user_id,
        rating=db_rating.rating,
       image_url =db_rating.image_url,
    )

    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

    # # حساب وتحديث متوسط التقييمات للدكتور
    # update_doctor_average_rating(db, rating.doctor_id)

    # return db_rating



def get_rating(db: Session, doctor_id: int = None,approved : bool = False):
    """  نقويم هذه الدالة بارجاع التقيمات لدكتور محدد او الكل """
    if doctor_id ==None :
        return db.query(Rating).all()
    return db.query(Rating).filter(Rating.doctor_id == doctor_id, Rating.approved == approved).all()
    



def review_rating(db :Session, review_id):

    rating  =  __get_table(db=db,table=Rating,id=review_id)
        
    rating.approved = True

    db.commit()
    db.refresh(rating)
    update_doctor_average_rating(db=db,doctor_id=rating.doctor_id)
    return True


def update_doctor_average_rating(db: Session, doctor_id: int):
    """
    تقوم هذه الدالة بحساب وتحديث متوسط التقييمات للدكتور.
    """

    doctor = get_doctor(db=db,doctor_id=doctor_id)

    if doctor:

        # db.query(func.avg(Rating.rating).label('average')).filter(Rating.doctor_id == doctor_id)
        total_ratings = db.query(Rating).filter().count()
        sum_ratings = db.query(Rating).filter(Rating.doctor_id == doctor_id).with_entities(func.sum(Rating.rating)).scalar()

        doctor.rating = sum_ratings / total_ratings if total_ratings > 0 else 0.0
        db.commit()
        db.refresh(doctor)

        return True
    return False





def save_image(file,path):
    if not os.path.exists(path):
        os.makedirs(path)
        # حفظ الصورة في المجلد المحدد
    file_location = f"{path}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        return file_location[1:]


def create_ad(db: Session, ad: schemas.AdCreate) -> Ad:
    """
    تقوم هذه الدالة بإنشاء إعلان جديد في قاعدة البيانات.
    """
    db_ad = Ad(
        title=ad.title,
        content=ad.content,
        image_url=ad.image_url  # يمكن تعيين الصورة لاحقًا
    )

    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)

    return db_ad



def get_ads(db: Session):
  
    return db.query(Ad).all()


def delete_rating(rating_id: int,table :Base  ,  db: Session):


    user = __get_table(db=db,table=table,id=rating_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
   