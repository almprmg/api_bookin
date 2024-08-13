from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app import schemas, crud, database
import shutil
import os

from exception import APPExceptions

router = APIRouter()

UPLOAD_DIRECTORY = "./uploads/ads"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@router.post("/add/")
async def create_ad(
    title: str,
    content: str,
    file: UploadFile = File(...), 
    db: Session = Depends(database.get_db)
):

    UPLOAD_DIRECTORY = "./uploads/ads"

    ad_data = schemas.AdCreate(title=title, content=content)
    if file:
       ad_data.image_url = crud.save_image(file,UPLOAD_DIRECTORY)
    ad = crud.create_ad(db=db, ad=ad_data)
    if ad:
        return ad
    raise APPExceptions.field_add_ads



@router.get("/", response_model=list[schemas.Ad])
def read_ads( db: Session = Depends(database.get_db)):
    """
    تقوم هذه الدالة بجلب قائمة من الإعلانات.
    

    :return: قائمة من الإعلانات
    """
    ads = crud.get_ads(db=db)
    if ads is None:
        raise APPExceptions.ads_not_found
    return ads

