
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from app.models import User
from sqlalchemy.orm import Session
from app import schemas, crud, database
from app.utils.security import create_access_token, get_current_user, verify_password
from exception import APPExceptions
router = APIRouter()

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(db: Session = Depends(database.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    print()
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise APPExceptions.not_correct_pass_user

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    
    return crud.create_user(db=db, user=user)


@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    print(current_user)
    return current_user


@router.delete("/delete/{user_id}")
async  def delete_user(user_id: int, db: Session = Depends(database.get_db),current_user: schemas.User = Depends(get_current_user)):
    """حذف حساب المستخدم """
  
    if crud.delete_acount(user_id,current_user.id,User,db):
        return {"message": "تم حذف المستخدم بنجاح!"}
    raise APPExceptions.user_not_found



@router.put("/update/{user_id}",response_model= schemas.UserCreate)
async  def update_user(user_id: int, updated_user: schemas.UserCreate, db: Session = Depends(database.get_db),current_user: schemas.User = Depends(get_current_user)):
    
    """ تعديل بيانات الحساب"""
    
  
    if crud.update_user(db=db,user_id=user_id,phone=updated_user.phone,updated_user=updated_user,token_id=current_user.id):
        updated_user_json = jsonable_encoder(updated_user)
        return  JSONResponse(
        status_code=200,
        content= {"message": "تم تحديث المستخدم بنجاح!","user": updated_user_json} )
    raise APPExceptions.user_not_found
