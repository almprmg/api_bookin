from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pytest import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base ,get_db
from router import users
from router import doctors
from router import rating
from router import ads
from . import crud
from . import schemas
# , doctors, ads, ratings, filters
DATABASE_URL = "sqlite:///./test.db"  # يمكنك تغيير هذا إلى قاعدة بيانات أخرى

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# إنشاء الجداول في قاعدة البيانات
Base.metadata.create_all(bind=engine)

app = FastAPI()




# تهيئة التطبيق الرئيسي
app = FastAPI()

# إنشاء الجداول في قاعدة البيانات
Base.metadata.create_all(bind=engine)

# إعدادات CORS للسماح بالطلبات من مصادر معينة
origins = [
    "http://localhost",
    "http://localhost:8000",
    # أضف المزيد من الأصول هنا حسب الحاجة
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تضمين التوجيهات (routers)
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(doctors.router, prefix="/doctors", tags=["Doctors"])
app.include_router(ads.router, prefix="/ads", tags=["Ads"])
app.include_router(rating.router, prefix="/rating", tags=["Rating"])
# app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])




#  مسار القوالب (Templates)
templates = Jinja2Templates(directory="templates")


app.mount("/static", StaticFiles(directory="static"), name="static")
# نهيئة الملفات الصور 
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# إدارة الأطباء
@app.get("/admin/doctors")
async def manage_doctors(request: Request,specialty:str = None, db: Session = Depends(get_db)):
    doctors = crud.get_doctors(db,specialty)
    return templates.TemplateResponse("doctors.html", {"request": request, "doctors": doctors})

@app.get("/admin/doctors/new")
async def add_doctor(request: Request):

    return templates.TemplateResponse("new_doctor.html", {"request": request})


# إدارة التقييمات
@app.get("/admin/reviews")
async def manage_reviews(request: Request, db: Session = Depends(get_db)):
    reviews = crud.get_rating(db)
    return templates.TemplateResponse("reviews.html", {"request": request, "reviews": reviews})

# الصفحة الرئيسية للوحة التحكم

@app.get("/",response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    return  templates.TemplateResponse("dashboard.html", {"request": request})
