from pydantic import BaseModel, HttpUrl, field_serializer
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
    comentario: Optional[str] = None

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
    name_mission: Optional[str] = None
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

    @field_serializer('net')
    def serialize_dt(self, dt: datetime, _info):
        if dt is None:
            return None
        return dt.isoformat().replace("+00:00", "Z")

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


# ---- ShopProduct Schemas ----

class ShopProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[str] = None
    image: Optional[str] = None
    affiliateUrl: Optional[str] = None
    category: Optional[str] = None
    featured: bool = False
    show: bool = True

class ShopProductCreate(ShopProductBase):
    pass

class ShopProductResponse(ShopProductBase):
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

# ---- Training Schemas ----

class TrainingBase(BaseModel):
    slug: str
    name: str
    name_en: Optional[str] = None
    type: str # grade, master, phd, university
    name_file: Optional[str] = None
    description: Optional[str] = None
    description_en: Optional[str] = None
    link: Optional[str] = None
    show: bool = True

class TrainingCreate(TrainingBase):
    pass

class TrainingResponse(TrainingBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ---- YouTube Schemas ----

class YouTubeVideoBase(BaseModel):
    video_name: str
    url: str
    type: Optional[str] = None
    description: Optional[str] = None
    description_en: Optional[str] = None
    date: Optional[str] = None
    own: bool = False
    show: bool = True

class YouTubeVideoCreate(YouTubeVideoBase):
    pass

class YouTubeVideoResponse(YouTubeVideoBase):
    id: int

    class Config:
        from_attributes = True


# ---- Research & Development Schemas ----

class ResearchDevelopmentBase(BaseModel):
    name: str
    name_en: Optional[str] = None
    type: str  # researchcenter, researchmagazine, paper, conference, estateoftheart
    description: Optional[str] = None
    description_en: Optional[str] = None
    show: bool = True
    link: Optional[str] = None
    slug: str
    file: Optional[str] = None

class ResearchDevelopmentCreate(ResearchDevelopmentBase):
    pass


class ResearchDevelopmentResponse(ResearchDevelopmentBase):
    id: int
    created_date: Optional[datetime] = None
    update_date: Optional[datetime] = None

    class Config:
        from_attributes = True

# ---- Course Schemas ----

class CourseBase(BaseModel):
    namecourse: str
    chapter: Optional[str] = None
    lesson: Optional[str] = None
    slug: str
    url_youtube: Optional[str] = None
    markdown_file: Optional[str] = None
    orden_index: int = 0
    show: bool = True

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ---- Challenge & Prediction Schemas ----

class PredictionBase(BaseModel):
    nickname: str
    email: str
    prediction_value: str

class PredictionCreate(PredictionBase):
    pass

class PredictionResponse(PredictionBase):
    id: int
    challenge_id: int
    created_at: datetime

    @field_serializer('created_at')
    def serialize_dt(self, dt: datetime, _info):
        return dt.isoformat().replace("+00:00", "Z")

    class Config:
        from_attributes = True

class PredictionPublic(BaseModel):
    id: int
    nickname: str
    prediction_value: str
    created_at: datetime

    @field_serializer('created_at')
    def serialize_dt(self, dt: datetime, _info):
        return dt.isoformat().replace("+00:00", "Z")

    class Config:
        from_attributes = True

class ChallengeBase(BaseModel):
    title: str
    title_en: Optional[str] = None
    description: Optional[str] = None
    description_en: Optional[str] = None
    image_url: Optional[str] = None
    end_date: datetime
    prediction_deadline: Optional[datetime] = None
    actual_event_date: Optional[datetime] = None
    is_active: bool = True
    prize_description: Optional[str] = None
    prize_description_en: Optional[str] = None
    prize_image_url: Optional[str] = None
    type: str = "date"
    options: Optional[List[str]] = None

class ChallengeCreate(ChallengeBase):
    pass

class ChallengeResponse(ChallengeBase):
    id: int
    created_at: datetime
    participant_count: Optional[int] = 0

    @field_serializer('end_date', 'prediction_deadline', 'actual_event_date', 'created_at')
    def serialize_dt(self, dt: datetime, _info):
        if dt is None:
            return None
        return dt.isoformat().replace("+00:00", "Z")

    class Config:
        from_attributes = True
