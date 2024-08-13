
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models import Doctor
from exception import APPExceptions
from sqlalchemy.orm import Session
import crud
import database, schemas
router = APIRouter()


@router.post("/add/",  response_model=schemas.Doctor)
def add_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(database.get_db)):
    """اضافة دكتور جديد"""
    crud.create_doctor(db=db,doctor= doctor)
    return  JSONResponse(
        status_code=200,
        content= {"message": "تمت إضافة الطبيب بنجاح!", "doctor": jsonable_encoder(doctor)} )  



@router.delete("/delete/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(database.get_db)):
    """ حذف دكتور"""
    if crud.delete_acount(doctor_id,doctor_id,Doctor,db) :
        return {"message": "تم حذف الطبيب بنجاح!"}
    raise APPExceptions.doctor_not_found


@router.get("/get/all/")
def get_doctors(specialty: str = None, db: Session = Depends(database.get_db),):
    """
  جلب الدكاترة مع أو بدون فلتر"""
    print(specialty)
    doctors =crud.get_doctors(db=db,specialty=specialty)
    if doctors:
        return doctors
    return None
@router.get("/get/{doctor_id}")
def get_doctors(doctor_id: int, db: Session = Depends(database.get_db),):
    """
  جلب الدكاترة مع أو بدون فلتر"""
    doctors =crud.get_doctor(db=db,doctor_id=doctor_id)
    if doctors:
        return doctors
    raise  APPExceptions.doctor_not_found
