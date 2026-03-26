from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Any, Dict
from datetime import date

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
    coordinates: Optional[Dict[str, float]] = None
    employees: Optional[int] = None
    website: Optional[str] = None
    description: Optional[str] = None
    description_en: Optional[str] = None
    founded: Optional[int] = None
    ceo: Optional[str] = None
    sector: Optional[str] = None
    tags: Optional[List[str]] = []
    socialLinks: Optional[Dict[str, str]] = {}
    keyPrograms: Optional[List[str]] = []
    fundingStage: Optional[str] = None
    totalFunding: Optional[str] = None
    stockTicker: Optional[str] = None

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

class SatelliteCreate(SatelliteBase):
    pass

class SatelliteResponse(SatelliteBase):
    id: int

    class Config:
        from_attributes = True


# ---- Launch Schemas ----

class LaunchBase(BaseModel):
    name: str
    rocket_id: Optional[int] = None
    provider_id: Optional[int] = None
    net: Optional[date] = None
    status: Optional[str] = None
    mission_description: Optional[str] = None
    mission_type: Optional[str] = None
    orbit_name: Optional[str] = None
    pad_name: Optional[str] = None
    pad_location: Optional[str] = None
    webcast_live: Optional[bool] = False
    image: Optional[str] = None

class LaunchCreate(LaunchBase):
    pass

class LaunchResponse(LaunchBase):
    id: int

    class Config:
        from_attributes = True
