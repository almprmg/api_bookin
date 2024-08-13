from fastapi import HTTPException
from fastapi import status


class APPExceptions:
    not_correct_pass_user = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="اسم المستخدم أو كلمة المرور غير صحيحة",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_not_found = HTTPException(status_code=404, detail="لم يتم العثور على المستخدم..")

    found_email  =HTTPException(status_code=400, detail="البريد الإلكتروني مستخدم بالفعل")
    found_username  = HTTPException(status_code=400, detail="اسم المستخدم مستخدم بالفعل") 
    field_id  = HTTPException(status_code=400, detail="الحساب غير صحيح (id)") 


    #doctor
    doctor_not_found  = HTTPException(status_code=404, detail="لم يتم العثور على الطبيب.")
    field_add_ads  = HTTPException(status_code=404, detail="فشل اضافة اعلان")
    ads_not_found  = HTTPException(status_code=404, detail="لم يتم العثور على الإعلانات")
    rating_not_found  = HTTPException(status_code=404, detail="التقيم غير موجود")
