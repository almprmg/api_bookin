from fastapi import APIRouter, Depends, File,  UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app import schemas, crud, database
from app.utils.security import get_current_user
from exception import APPExceptions
from app.models import Rating
router = APIRouter()

@router.post("/doctor/")
def add_rating(    
    doctor_id: int,
    rating: float,
    file: UploadFile = File(...), db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    """
    يقوم هذا المسار  بإضافة تقييم لدكتور معين.
    """
    UPLOAD_DIRECTORY = "./uploads/rating"
    
    doctor = crud.get_doctor(db, doctor_id=doctor_id)
    db_rating =  schemas.RatingCreate(doctor_id=doctor_id,rating=rating,)
    if file:
       db_rating.image_url = crud.save_image(file,UPLOAD_DIRECTORY)
    if not doctor:
        raise APPExceptions.doctor_not_found
    if crud.create_rating(db = db, db_rating = db_rating, user_id = current_user.id):
        return    JSONResponse(
        status_code=200,
        content= {"message": "تم التقيم!"} )

@router.put("/approved/{rating_id}")
def approve_rating(rating_id: int, db: Session = Depends(database.get_db)):
    """ قبول الاتقيم  الملتزم با المعاير """
    print("asdf")
    if crud.review_rating(db = db, review_id = rating_id ) :
        
        return    JSONResponse(
        status_code=200,
        content= {"message": "تم قبول التقيم!"} )  
    raise APPExceptions.rating_not_found
@router.get("/")
def get_rating(is_approved : bool  = False, db: Session = Depends(database.get_db)):
    """جلب كل التقيمات"""
    db_rating   =  crud.get_rating(db = db ,approved=is_approved )
    result = []
    for rating in db_rating:
        rating_data = {
            "id": rating.id,
            "doctor_name": rating.doctor.name,
            "doctor_image_url": rating.doctor.profileImageUrl,
            "user_name": rating.user.username,
            # "user_image_url": rating.user.profile_image_url,
            "rating": rating.rating,
            # "comment": rating.comment,
            "is_approved": rating.approved,
            "rating_image_url": rating.image_url,  # صورة التقييم
        }
        result.append(rating_data)

    if result :
        
        return   result 
    raise APPExceptions.rating_not_found


@router.delete("/delete/{rating_id}")
def approve_rating(rating_id:int,db: Session = Depends(database.get_db)):
    """ قبول الاتقيم  الملتزم با المعاير """
    print("asdf")
 
    if crud.delete_rating(db = db, rating_id = rating_id,table= Rating) :
        return    JSONResponse(
        status_code=200,
        content= {"message": "تم الحذف!"} )  
    raise APPExceptions.rating_not_found