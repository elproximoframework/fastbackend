from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Any, Dict
from datetime import date, datetime

# ---- Core Schemas ----

class Coordinate(BaseModel):
    lat: float
    lng: float

# ---- Company Schemas ----

class CompanyBase(BaseModel):
    name: str
    type: Optional[str] = None
    country: Optional[str] = None
    countryName: Optional[str] = None
    city: Optional[str] = None
    coordinates: Optional[Dict[str, Optional[float]]] = None
    employees: Optional[int] = None
    website: Optional[str] = None
    description: Optional[str] = None
    description_en: Optional[str] = None
    founded: Optional[int] = None
    ceo: Optional[str] = None
    sector: Optional[str] = None
    tags: Optional[List[Optional[str]]] = []
    socialLinks: Optional[Dict[str, Optional[str]]] = {}
    keyPrograms: Optional[List[Optional[str]]] = []
    fundingStage: Optional[str] = None
    totalFunding: Optional[str] = None
    stockTicker: Optional[str] = None
    otrassede: Optional[str] = None
    logo: Optional[str] = None
    slug: Optional[str] = None
    rutainformacion: Optional[str] = None
    featured_espacio: bool = False
    validated: bool = False
    company_validated: bool = False
    show: bool = True

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: int

    class Config:
        from_attributes = True

# ---- Rocket Schemas ----

class RocketBase(BaseModel):
    name: str
    manufacturer_id: Optional[int] = None
    country: Optional[str] = None
    height: Optional[float] = None
    diameter: Optional[float] = None
    stages: Optional[int] = None
    fuel: Optional[str] = None
    leoCapacity: Optional[float] = None
    gtoCapacity: Optional[float] = None
    firstFlight: Optional[date] = None
    totalLaunches: Optional[int] = None
    successRate: Optional[float] = None
    status: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    description_en: Optional[str] = None
    costPerLaunch: Optional[float] = None
    reusable: Optional[bool] = False

class RocketCreate(RocketBase):
    pass

class RocketResponse(RocketBase):
    id: int
    manufacturer: Optional[CompanyResponse] = None

    class Config:
        from_attributes = True


# ---- Satellite Schemas ----

class SatelliteBase(BaseModel):
    name: str
    noradId: Optional[str] = None
    operator_id: Optional[int] = None
    purpose: Optional[str] = None
    launchDate: Optional[date] = None
    orbitType: Optional[str] = None
    altitude: Optional[float] = None
    inclination: Optional[float] = None
    description: Optional[str] = None
    description_en: Optional[str] = None
    image: Optional[str] = None
    isFeatured: Optional[bool] = False
    funFact: Optional[str] = None
    funFact_en: Optional[str] = None
    show: bool = True

class SatelliteCreate(SatelliteBase):
    pass

class SatelliteResponse(SatelliteBase):
    id: int
    operator: Optional[CompanyResponse] = None

    class Config:
        from_attributes = True


# ---- Launch Schemas ----

class LaunchBase(BaseModel):
    name: str
    api_id: Optional[str] = None
    rocket_id: Optional[int] = None
    provider_id: Optional[int] = None
    net: Optional[datetime] = None
    status: Optional[str] = None
    mission_description: Optional[str] = None
    mission_type: Optional[str] = None
    orbit_name: Optional[str] = None
    pad_name: Optional[str] = None
    pad_location: Optional[str] = None
    celestial_body: Optional[str] = "Earth"
    webcast_live: Optional[bool] = False
    image: Optional[str] = None
    vid_urls: Optional[List[Dict[str, Any]]] = []
    info_urls: Optional[List[Dict[str, Any]]] = []
    show: bool = True

class LaunchCreate(LaunchBase):
    pass

class LaunchResponse(LaunchBase):
    id: int
    rocket: Optional[RocketResponse] = None
    provider: Optional[CompanyResponse] = None

    class Config:
        from_attributes = True


# ---- News Schemas ----

class NewsBase(BaseModel):
    title: str
    title_en: Optional[str] = None
    excerpt: Optional[str] = None
    excerpt_en: Optional[str] = None
    category: Optional[str] = None
    category_en: Optional[str] = None
    location: Optional[str] = None
    location_en: Optional[str] = None
    covered: bool = False
    date: str
    image: Optional[str] = None
    slug: str
    tags: Optional[List[Optional[str]]] = []
    tags_en: Optional[List[Optional[str]]] = []
    featured: bool = False
    linkyoutube: Optional[str] = None
    rutanoticia: Optional[str] = None
    timestart: Optional[Any] = None
    show: bool = True

class NewsCreate(NewsBase):
    pass

class NewsResponse(NewsBase):
    id: int

    class Config:
        from_attributes = True


# ---- NewsSpaceX Schemas ----

class NewsSpaceXBase(BaseModel):
    title: str
    title_en: Optional[str] = None
    excerpt: Optional[str] = None
    excerpt_en: Optional[str] = None
    category: Optional[str] = None
    category_en: Optional[str] = None
    location: Optional[str] = None
    location_en: Optional[str] = None
    covered: bool = False
    date: str
    image: Optional[str] = None
    slug: str
    tags: Optional[List[Optional[str]]] = []
    tags_en: Optional[List[Optional[str]]] = []
    featured: bool = False
    linkyoutube: Optional[str] = None
    rutanoticia: Optional[str] = None
    timestart: Optional[Any] = None
    show: bool = True

class NewsSpaceXCreate(NewsSpaceXBase):
    pass

class NewsSpaceXResponse(NewsSpaceXBase):
    id: int

    class Config:
        from_attributes = True


# ---- SpaceXInventory Schemas ----

class SpaceXInventoryBase(BaseModel):
    title: str
    title_en: Optional[str] = None
    excerpt: Optional[str] = None
    excerpt_en: Optional[str] = None
    category: Optional[str] = None
    category_en: Optional[str] = None
    location: Optional[str] = None
    location_en: Optional[str] = None
    version: Optional[str] = None
    datestartfabrication: Optional[str] = None
    datesfinishfabrication: Optional[str] = None
    state: Optional[str] = None
    state_en: Optional[str] = None
    datelaunch: Optional[str] = None
    resultlaunch: Optional[str] = None
    resultlaunch_en: Optional[str] = None
    covered: bool = False
    date: str
    image: Optional[str] = None
    slug: str
    tags: Optional[List[Optional[str]]] = []
    tags_en: Optional[List[Optional[str]]] = []
    featured: bool = False
    linkyoutube: Optional[str] = None
    rutainformacion: Optional[str] = None
    timestart: Optional[Any] = None
    show: bool = True
    # Extended fields for Starship program structured data
    serial_number: Optional[str] = None
    block: Optional[str] = None
    specs: Optional[Dict[str, Any]] = None
    flight_data: Optional[Dict[str, Any]] = None
    milestones: Optional[List[Dict[str, Any]]] = None

class SpaceXInventoryCreate(SpaceXInventoryBase):
    pass

class SpaceXInventoryResponse(SpaceXInventoryBase):
    id: int

    class Config:
        from_attributes = True


# ---- Setting Schemas ----

class AppSettingBase(BaseModel):
    key: str
    value: str
    type: Optional[str] = "string"
    description: Optional[str] = None

class AppSettingCreate(AppSettingBase):
    pass

class AppSettingResponse(AppSettingBase):
    id: int

    class Config:
        from_attributes = True
# ---- Stats Schemas ----

class StatsResponse(BaseModel):
    news_count: int
    newsspacex_count: int
    companies_count: int
    rockets_count: int
    launches_count: int
    satellites_count: int
    spacex_inventory_count: int


# ---- Media Hub Schemas ----

class MediaSourceBase(BaseModel):
    slug: str
    category: str
    subcategory: Optional[str] = None
    language: str = "en"
    country: Optional[str] = None
    country_name: Optional[str] = None
    name: str
    description: Optional[str] = None
    description_en: Optional[str] = None
    tagline: Optional[str] = None
    tagline_en: Optional[str] = None
    rating: int = 3
    recommended: bool = False
    difficulty: str = "general"
    website: Optional[str] = None
    youtube_url: Optional[str] = None
    youtube_handle: Optional[str] = None
    twitter_url: Optional[str] = None
    instagram_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    spotify_url: Optional[str] = None
    apple_podcasts_url: Optional[str] = None
    rss_feed_url: Optional[str] = None
    newsletter_url: Optional[str] = None
    content_format: Optional[List[str]] = []
    topics: Optional[List[str]] = []
    is_free: bool = True
    paywall: bool = False
    featured: bool = False
    show: bool = True

class MediaSourceCreate(MediaSourceBase):
    pass

class MediaSourceResponse(MediaSourceBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CategoryCount(BaseModel):
    category: str
    count: int
