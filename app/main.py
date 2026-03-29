from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas
from .database import engine, get_db
import os

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Space API",
    description="API for Space portal with Companies, Rockets, Satellites, and Launches",
    version="1.0.0",
)

# Enable CORS for the frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, replace "*" with your frontend's actual URL (e.g., "https://my-space-frontend.up.railway.app")
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve news markdown files
news_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "news")
if not os.path.exists(news_dir):
    os.makedirs(news_dir)
app.mount("/api/v1/news_content", StaticFiles(directory=news_dir), name="news")

# Serve news images
news_images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "news_images")
if not os.path.exists(news_images_dir):
    os.makedirs(news_images_dir)
app.mount("/api/v1/news_images", StaticFiles(directory=news_images_dir), name="news_images")

# Serve company logos
company_logos_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "company_logos")
if not os.path.exists(company_logos_dir):
    os.makedirs(company_logos_dir)
app.mount("/api/v1/company_logos", StaticFiles(directory=company_logos_dir), name="company_logos")

# Serve rocket images
rocket_images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "rocket_images")
if not os.path.exists(rocket_images_dir):
    os.makedirs(rocket_images_dir)
app.mount("/api/v1/rocket_images", StaticFiles(directory=rocket_images_dir), name="rocket_images")

# Serve satellite images
satellite_images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "satellite_images")
if not os.path.exists(satellite_images_dir):
    os.makedirs(satellite_images_dir)
app.mount("/api/v1/satellite_images", StaticFiles(directory=satellite_images_dir), name="satellite_images")

# ---- Health Check ----

@app.get("/api/v1/health")
def health_check():
    return {
        "status": "online",
        "message": "Backend is correctly deployed on Railway!",
        "version": "1.0.0"
    }

# ---- Companies ----

@app.get("/api/v1/companies", response_model=List[schemas.CompanyResponse])
def get_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    companies = db.query(models.Company).filter(models.Company.show == True).offset(skip).limit(limit).all()
    return companies

@app.get("/api/v1/companies/{company_id}", response_model=schemas.CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

# ---- Rockets ----

@app.get("/api/v1/rockets", response_model=List[schemas.RocketResponse])
def get_rockets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rockets = db.query(models.Rocket).offset(skip).limit(limit).all()
    return rockets

@app.get("/api/v1/rockets/{rocket_id}", response_model=schemas.RocketResponse)
def get_rocket(rocket_id: int, db: Session = Depends(get_db)):
    rocket = db.query(models.Rocket).filter(models.Rocket.id == rocket_id).first()
    if rocket is None:
        raise HTTPException(status_code=404, detail="Rocket not found")
    return rocket

# ---- Satellites ----

@app.get("/api/v1/satellites", response_model=List[schemas.SatelliteResponse])
def get_satellites(
    search: Optional[str] = None, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    query = db.query(models.Satellite).filter(models.Satellite.show == True)
    if search:
        query = query.filter(models.Satellite.name.ilike(f"%{search}%"))
    satellites = query.offset(skip).limit(limit).all()
    return satellites

@app.get("/api/v1/satellites/{satellite_id}", response_model=schemas.SatelliteResponse)
def get_satellite(satellite_id: int, db: Session = Depends(get_db)):
    satellite = db.query(models.Satellite).filter(models.Satellite.id == satellite_id).first()
    if satellite is None:
        raise HTTPException(status_code=404, detail="Satellite not found")
    return satellite

# ---- Launches ----

@app.get("/api/v1/launches", response_model=List[schemas.LaunchResponse])
def get_launches(
    status: Optional[str] = Query(None, description="Filter by status (e.g. upcoming, past)"),
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    query = db.query(models.Launch).filter(models.Launch.show == True)
    
    # Note: the definition of 'upcoming' vs 'past' could depend on the 'net' date or exact status strings
    if status == 'upcoming':
        # Simple example: you might filter by net >= current_date or status matching Go
        query = query.filter(models.Launch.status.ilike("%upcoming%") | models.Launch.status.ilike("%Go%"))
    elif status == 'past':
        query = query.filter(models.Launch.status.ilike("%past%") | models.Launch.status.ilike("%Success%"))
    elif status:
        query = query.filter(models.Launch.status.ilike(f"%{status}%"))

    launches = query.offset(skip).limit(limit).all()
    return launches

@app.get("/api/v1/launches/{launch_id}", response_model=schemas.LaunchResponse)
def get_launch(launch_id: int, db: Session = Depends(get_db)):
    launch = db.query(models.Launch).filter(models.Launch.id == launch_id).first()
    if launch is None:
        raise HTTPException(status_code=404, detail="Launch not found")
    return launch


# ---- News ----

@app.get("/api/v1/news", response_model=List[schemas.NewsResponse])
def get_news(
    category: Optional[str] = None,
    featured: Optional[bool] = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    query = db.query(models.News).filter(models.News.show == True)
    
    if category:
        # Search in both category and category_en
        query = query.filter(
            (models.News.category.ilike(f"%{category}%")) | 
            (models.News.category_en.ilike(f"%{category}%"))
        )
    
    if featured is not None:
        query = query.filter(models.News.featured == featured)
        
    # Sort by date descending (latest first)
    news_items = query.order_by(models.News.date.desc()).offset(skip).limit(limit).all()
    return news_items

@app.get("/api/v1/news/featured", response_model=schemas.NewsResponse)
def get_featured_news(db: Session = Depends(get_db)):
    setting = db.query(models.AppSetting).filter(models.AppSetting.key == "featured_news_id").first()
    if not setting:
        raise HTTPException(status_code=404, detail="Featured news ID not set in settings")
    
    try:
        news_id = int(setting.value)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid featured news ID in settings")

    news_item = db.query(models.News).filter(models.News.id == news_id).first()
    if not news_item:
        raise HTTPException(status_code=404, detail="Featured news item not found")
    
    return news_item

@app.get("/api/v1/news/{slug}", response_model=schemas.NewsResponse)
def get_news_item(slug: str, db: Session = Depends(get_db)):
    news_item = db.query(models.News).filter(models.News.slug == slug).first()
    if news_item is None:
        # Try to find by ID if slug not found and is numeric
        if slug.isdigit():
            news_item = db.query(models.News).filter(models.News.id == int(slug)).first()
            
    if news_item is None:
        raise HTTPException(status_code=404, detail="News item not found")
    return news_item


# ---- Settings ----

@app.get("/api/v1/settings", response_model=List[schemas.AppSettingResponse])
def get_settings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    settings = db.query(models.AppSetting).offset(skip).limit(limit).all()
    return settings

@app.get("/api/v1/settings/{key}", response_model=schemas.AppSettingResponse)
def get_setting(key: str, db: Session = Depends(get_db)):
    setting = db.query(models.AppSetting).filter(models.AppSetting.key == key).first()
    if setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting

@app.put("/api/v1/settings/{key}", response_model=schemas.AppSettingResponse)
def update_setting(key: str, setting_update: schemas.AppSettingCreate, db: Session = Depends(get_db)):
    db_setting = db.query(models.AppSetting).filter(models.AppSetting.key == key).first()
    if db_setting is None:
        # Optionally create if not exists
        db_setting = models.AppSetting(**setting_update.dict())
        db.add(db_setting)
    else:
        for var, value in vars(setting_update).items():
            setattr(db_setting, var, value) if value is not None else None
    
    db.commit()
    db.refresh(db_setting)
    return db_setting
