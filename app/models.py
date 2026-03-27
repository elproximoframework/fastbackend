from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    type = Column(String) # startup, agency, contractor, university
    country = Column(String)
    countryName = Column(String)
    city = Column(String)
    coordinates = Column(JSON) # e.g. {"lat": 28.5, "lng": -80.6}
    employees = Column(Integer)
    website = Column(String)
    description = Column(String)
    description_en = Column(String)
    founded = Column(Integer)
    ceo = Column(String)
    sector = Column(String)
    tags = Column(JSON) # List of strings
    socialLinks = Column(JSON) # e.g. {"twitter": "...", "linkedin": "..."}
    keyPrograms = Column(JSON) # List of strings
    fundingStage = Column(String)
    totalFunding = Column(String)
    stockTicker = Column(String)

    rockets = relationship("Rocket", back_populates="manufacturer")
    satellites = relationship("Satellite", back_populates="operator")
    launches = relationship("Launch", back_populates="provider")


class Rocket(Base):
    __tablename__ = "rockets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    manufacturer_id = Column(Integer, ForeignKey("companies.id"))
    country = Column(String)
    height = Column(Float)
    diameter = Column(Float)
    stages = Column(Integer)
    fuel = Column(String)
    leoCapacity = Column(Float)
    gtoCapacity = Column(Float)
    firstFlight = Column(Date)
    totalLaunches = Column(Integer)
    successRate = Column(Float)
    status = Column(String) # active, development, retired, cancelled
    image = Column(String)
    description = Column(String)
    description_en = Column(String)
    costPerLaunch = Column(Float)
    reusable = Column(Boolean)

    manufacturer = relationship("Company", back_populates="rockets")
    launches = relationship("Launch", back_populates="rocket")


class Satellite(Base):
    __tablename__ = "satellites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    noradId = Column(String, index=True)
    operator_id = Column(Integer, ForeignKey("companies.id"))
    purpose = Column(String)
    launchDate = Column(Date)
    orbitType = Column(String)
    altitude = Column(Float)
    inclination = Column(Float)
    description = Column(String)
    description_en = Column(String)
    image = Column(String)
    isFeatured = Column(Boolean, default=False)
    funFact = Column(String)
    funFact_en = Column(String)

    operator = relationship("Company", back_populates="satellites")


class Launch(Base):
    __tablename__ = "launches"

    id = Column(Integer, primary_key=True, index=True)
    api_id = Column(String, unique=True, index=True) # ID from Space Devs API
    name = Column(String, index=True, nullable=False)
    rocket_id = Column(Integer, ForeignKey("rockets.id"))
    provider_id = Column(Integer, ForeignKey("companies.id"))
    net = Column(DateTime) # Next Estimated Time (TIMESTAMP)
    status = Column(String) # e.g. Go for Launch, TBD, Success, Failure
    mission_description = Column(String)
    mission_type = Column(String)
    orbit_name = Column(String)
    pad_name = Column(String)
    pad_location = Column(String)
    celestial_body = Column(String, default="Earth")
    webcast_live = Column(Boolean, default=False)
    image = Column(String)
    vid_urls = Column(JSON) # Webcast links
    info_urls = Column(JSON) # Mission details

    rocket = relationship("Rocket", back_populates="launches")
    provider = relationship("Company", back_populates="launches")


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    title_en = Column(String, index=True)
    excerpt = Column(String)
    excerpt_en = Column(String)
    body = Column(String)
    body_en = Column(String)
    category = Column(String, index=True)
    category_en = Column(String, index=True)
    location = Column(String)
    location_en = Column(String)
    covered = Column(Boolean, default=False)
    date = Column(String) # ISO format string as in mock
    image = Column(String)
    slug = Column(String, index=True, unique=True)
    tags = Column(JSON) # List of strings in ES
    tags_en = Column(JSON) # List of strings in EN
    featured = Column(Boolean, default=False)
    linkyoutube = Column(String, nullable=True)
    rutanoticia = Column(String, nullable=True)
    timestart = Column(Integer, nullable=True)
