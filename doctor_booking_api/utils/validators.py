from sqlalchemy.orm import Session
from app import models
from exception import APPExceptions

def validate_unique_username(db: Session, username: str,id=None):
    """
    تقوم هذه الدالة بالتحقق من أن اسم المستخدم فريد وغير موجود في قاعدة البيانات.
    """
    user = db.query(models.User).filter(models.User.username == username).first()

    check_view_exciton(user=user,
                       id=id,
                       exception = APPExceptions.found_username)
   

def validate_unique_email(db: Session, email: str,id=None):
    """
    تقوم هذه الدالة بالتحقق من أن البريد الإلكتروني فريد وغير موجود في قاعدة البيانات.
    """

    user = db.query(models.User).filter(models.User.email == email).first()
    check_view_exciton(user=user,
                       id=id,
                       exception= APPExceptions.found_email)



def validate_is_he(user_id: int, token_id):
    """
   نتحقق من انه نفس الامستخدم الذي يريد حذف حسابه
    """
  
    if user_id != token_id :
        raise APPExceptions.file_id



def check_view_exciton(user,id,exception):
    if user:
        if id != user.id: raise exception