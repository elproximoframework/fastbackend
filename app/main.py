from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone
from . import models, schemas
from .database import engine, get_db
from .routes.auth_router import router as auth_router
from .routes.media import router as media_router
from .routes.training import router as training_router
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
import sentry_sdk
# FastAPIIntegration is auto-detected in recent SDK versions
import os
import uvicorn

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Initialize Sentry
load_dotenv()
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    send_default_pii=True
)

app = FastAPI(
    title="Space API",
    description="API for Space portal",
    version="1.0.0",
)

# --- 1. CONFIGURACIÓN DE CORS (DEBE SER LO PRIMERO) ---
# Definimos los orígenes exactos permitidos
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "https://elproximoframework.com",
    "https://www.elproximoframework.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# --- 2. REGISTRO DE ROUTERS ---
app.include_router(auth_router)
app.include_router(media_router)
app.include_router(training_router)

# --- 3. LOG DE RUTAS PARA DEBUG ---
@app.on_event("startup")
async def list_routes():
    print("--- RUTAS REGISTRADAS ---")
    for route in app.routes:
        if hasattr(route, "methods"):
            print(f"{route.methods} {route.path}")
    print("-------------------------")

# --- 4. RATE LIMITER ---
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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

# Serve SpaceX news markdown files
newsspacex_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "newsspacex")
if not os.path.exists(newsspacex_dir):
    os.makedirs(newsspacex_dir)
app.mount("/api/v1/newsspacex_content", StaticFiles(directory=newsspacex_dir), name="newsspacex")

# Serve SpaceX news images
newsspacex_images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "newsspacex_images")
if not os.path.exists(newsspacex_images_dir):
    os.makedirs(newsspacex_images_dir)
app.mount("/api/v1/newsspacex_images", StaticFiles(directory=newsspacex_images_dir), name="newsspacex_images")

# Serve SpaceX inventory markdown files
inventory_docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "inventory_docs")
if not os.path.exists(inventory_docs_dir):
    os.makedirs(inventory_docs_dir)
app.mount("/api/v1/inventory_content", StaticFiles(directory=inventory_docs_dir), name="inventory_docs")

# Serve SpaceX inventory images
inventory_images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "inventory_images")
if not os.path.exists(inventory_images_dir):
    os.makedirs(inventory_images_dir)
app.mount("/api/v1/inventory_images", StaticFiles(directory=inventory_images_dir), name="inventory_images")

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
@limiter.limit("30/minute")
def get_companies(request: Request, skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    companies = db.query(models.Company).filter(models.Company.show == True).offset(skip).limit(limit).all()
    return companies

@app.get("/api/v1/companies/{slug}", response_model=schemas.CompanyResponse)
@limiter.limit("60/minute")
def get_company(request: Request, slug: str, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.slug == slug).first()
    if company is None:
        if slug.isdigit():
            company = db.query(models.Company).filter(models.Company.id == int(slug)).first()
            
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

# ---- Rockets ----

@app.get("/api/v1/rockets", response_model=List[schemas.RocketResponse])
@limiter.limit("30/minute")
def get_rockets(request: Request, skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    rockets = db.query(models.Rocket).offset(skip).limit(limit).all()
    return rockets

@app.get("/api/v1/rockets/{rocket_id}", response_model=schemas.RocketResponse)
@limiter.limit("60/minute")
def get_rocket(request: Request, rocket_id: int, db: Session = Depends(get_db)):
    rocket = db.query(models.Rocket).filter(models.Rocket.id == rocket_id).first()
    if rocket is None:
        raise HTTPException(status_code=404, detail="Rocket not found")
    return rocket

# ---- Satellites ----

@app.get("/api/v1/satellites", response_model=List[schemas.SatelliteResponse])
@limiter.limit("20/minute")
def get_satellites(
    request: Request,
    search: Optional[str] = None, 
    skip: int = 0, 
    limit: int = 1000, 
    db: Session = Depends(get_db)
):
    query = db.query(models.Satellite).filter(models.Satellite.show == True)
    if search:
        query = query.filter(models.Satellite.name.ilike(f"%{search}%"))
    satellites = query.offset(skip).limit(limit).all()
    return satellites

@app.get("/api/v1/satellites/{satellite_id}", response_model=schemas.SatelliteResponse)
@limiter.limit("60/minute")
def get_satellite(request: Request, satellite_id: int, db: Session = Depends(get_db)):
    satellite = db.query(models.Satellite).filter(models.Satellite.id == satellite_id).first()
    if satellite is None:
        raise HTTPException(status_code=404, detail="Satellite not found")
    return satellite

# ---- Launches ----

@app.get("/api/v1/launches", response_model=List[schemas.LaunchResponse])
@limiter.limit("30/minute")
def get_launches(
    request: Request,
    status: Optional[str] = Query(None, description="Filter by status (e.g. upcoming, past)"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date (ISO format)"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date (ISO format)"),
    skip: int = 0, 
    limit: int = 1000, 
    db: Session = Depends(get_db)
):
    query = db.query(models.Launch).filter(models.Launch.show == True)
    
    # Date range filtering
    if start_date:
        query = query.filter(models.Launch.net >= start_date)
    if end_date:
        query = query.filter(models.Launch.net <= end_date)
    
    # Status filtering
    if status == 'upcoming':
        now = datetime.now(timezone.utc)
        query = query.filter(
            (models.Launch.status.ilike("%upcoming%") | models.Launch.status.ilike("%Go%")) &
            (models.Launch.net >= now)
        )
    elif status == 'past':
        query = query.filter(models.Launch.status.ilike("%past%") | models.Launch.status.ilike("%Success%"))
    elif status:
        query = query.filter(models.Launch.status.ilike(f"%{status}%"))

    # Always sort by date for consistency
    launches = query.order_by(models.Launch.net.asc()).offset(skip).limit(limit).all()
    return launches

@app.get("/api/v1/launches/{launch_id}", response_model=schemas.LaunchResponse)
@limiter.limit("60/minute")
def get_launch(request: Request, launch_id: int, db: Session = Depends(get_db)):
    launch = db.query(models.Launch).filter(models.Launch.id == launch_id).first()
    if launch is None:
        raise HTTPException(status_code=404, detail="Launch not found")
    return launch


# ---- News ----

@app.get("/api/v1/news", response_model=List[schemas.NewsResponse])
@limiter.limit("30/minute")
def get_news(
    request: Request,
    category: Optional[str] = None,
    featured: Optional[bool] = None,
    skip: int = 0, 
    limit: int = 1000, 
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
@limiter.limit("60/minute")
def get_featured_news(request: Request, db: Session = Depends(get_db)):
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
@limiter.limit("60/minute")
def get_news_item(request: Request, slug: str, db: Session = Depends(get_db)):
    news_item = db.query(models.News).filter(models.News.slug == slug).first()
    if news_item is None:
        # Try to find by ID if slug not found and is numeric
        if slug.isdigit():
            news_item = db.query(models.News).filter(models.News.id == int(slug)).first()
            
    if news_item is None:
        raise HTTPException(status_code=404, detail="News item not found")
    return news_item


# ---- NewsSpaceX ----

@app.get("/api/v1/newsspacex", response_model=List[schemas.NewsSpaceXResponse])
@limiter.limit("30/minute")
def get_news_spacex(
    request: Request,
    category: Optional[str] = None,
    featured: Optional[bool] = None,
    skip: int = 0, 
    limit: int = 1000, 
    db: Session = Depends(get_db)
):
    query = db.query(models.NewsSpaceX).filter(models.NewsSpaceX.show == True)
    
    if category:
        query = query.filter(
            (models.NewsSpaceX.category.ilike(f"%{category}%")) | 
            (models.NewsSpaceX.category_en.ilike(f"%{category}%"))
        )
    
    if featured is not None:
        query = query.filter(models.NewsSpaceX.featured == featured)
        
    news_items = query.order_by(models.NewsSpaceX.date.desc()).offset(skip).limit(limit).all()
    return news_items

@app.get("/api/v1/newsspacex/featured", response_model=schemas.NewsSpaceXResponse)
@limiter.limit("60/minute")
def get_featured_news_spacex(request: Request, db: Session = Depends(get_db)):
    setting = db.query(models.AppSetting).filter(models.AppSetting.key == "featured_news_spacex_id").first()
    if not setting:
        # Fallback to the latest featured news if setting not found
        news_item = db.query(models.NewsSpaceX).filter(models.NewsSpaceX.featured == True).order_by(models.NewsSpaceX.date.desc()).first()
        if not news_item:
            raise HTTPException(status_code=404, detail="No featured SpaceX news found")
        return news_item
    
    try:
        news_id = int(setting.value)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid featured news ID in settings")

    news_item = db.query(models.NewsSpaceX).filter(models.NewsSpaceX.id == news_id).first()
    if not news_item:
        raise HTTPException(status_code=404, detail="Featured SpaceX news item not found")
    
    return news_item

@app.get("/api/v1/newsspacex/{slug}", response_model=schemas.NewsSpaceXResponse)
@limiter.limit("60/minute")
def get_news_spacex_item(request: Request, slug: str, db: Session = Depends(get_db)):
    news_item = db.query(models.NewsSpaceX).filter(models.NewsSpaceX.slug == slug).first()
    if news_item is None:
        if slug.isdigit():
            news_item = db.query(models.NewsSpaceX).filter(models.NewsSpaceX.id == int(slug)).first()
            
    if news_item is None:
        raise HTTPException(status_code=404, detail="SpaceX news item not found")
    return news_item


# ---- SpaceXInventory ----

@app.get("/api/v1/spacex-inventory", response_model=List[schemas.SpaceXInventoryResponse])
@limiter.limit("30/minute")
def get_spacex_inventory(
    request: Request,
    category: Optional[str] = None,
    location: Optional[str] = None,
    state: Optional[str] = None,
    block: Optional[str] = None,
    featured: Optional[bool] = None,
    skip: int = 0, 
    limit: int = 1000, 
    db: Session = Depends(get_db)
):
    query = db.query(models.SpaceXInventory).filter(models.SpaceXInventory.show == True)
    
    if category:
        query = query.filter(
            (models.SpaceXInventory.category.ilike(f"%{category}%")) | 
            (models.SpaceXInventory.category_en.ilike(f"%{category}%"))
        )
    
    if location:
        query = query.filter(
            (models.SpaceXInventory.location.ilike(f"%{location}%")) | 
            (models.SpaceXInventory.location_en.ilike(f"%{location}%"))
        )

    if state:
        query = query.filter(
            (models.SpaceXInventory.state.ilike(f"%{state}%")) | 
            (models.SpaceXInventory.state_en.ilike(f"%{state}%"))
        )

    if block:
        query = query.filter(models.SpaceXInventory.block.ilike(f"%{block}%"))
    
    if featured is not None:
        query = query.filter(models.SpaceXInventory.featured == featured)
        
    items = query.order_by(models.SpaceXInventory.date.desc()).offset(skip).limit(limit).all()
    return items

@app.get("/api/v1/spacex-inventory/{slug}", response_model=schemas.SpaceXInventoryResponse)
@limiter.limit("60/minute")
def get_spacex_inventory_item(request: Request, slug: str, db: Session = Depends(get_db)):
    item = db.query(models.SpaceXInventory).filter(models.SpaceXInventory.slug == slug).first()
    if item is None:
        if slug.isdigit():
            item = db.query(models.SpaceXInventory).filter(models.SpaceXInventory.id == int(slug)).first()
            
    if item is None:
        raise HTTPException(status_code=404, detail="SpaceX inventory item not found")
    return item


# ---- Settings ----

@app.get("/api/v1/settings", response_model=List[schemas.AppSettingResponse])
@limiter.limit("10/minute")
def get_settings(request: Request, skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    settings = db.query(models.AppSetting).offset(skip).limit(limit).all()
    return settings

@app.get("/api/v1/settings/{key}", response_model=schemas.AppSettingResponse)
@limiter.limit("10/minute")
def get_setting(request: Request, key: str, db: Session = Depends(get_db)):
    setting = db.query(models.AppSetting).filter(models.AppSetting.key == key).first()
    if setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting

# ---- Stats ----

@app.get("/api/v1/stats", response_model=schemas.StatsResponse)
@limiter.limit("60/minute")
def get_stats(request: Request, db: Session = Depends(get_db)):
    """Get general statistics for the portal"""
    return {
        "news_count": db.query(models.News).count(),
        "newsspacex_count": db.query(models.NewsSpaceX).count(),
        "companies_count": db.query(models.Company).count(),
        "rockets_count": db.query(models.Rocket).count(),
        "launches_count": db.query(models.Launch).count(),
        "satellites_count": db.query(models.Satellite).count(),
        "spacex_inventory_count": db.query(models.SpaceXInventory).count()
    }

@app.get("/api/v1/sentry-debug")
def trigger_error():
    """Endpoint to verify Sentry connection"""
    division_by_zero = 1 / 0
    return {"message": "This should not be reached"}
