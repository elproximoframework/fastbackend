from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, timezone

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    type = Column(String) # startup, corporate, agency, academia, investor, non_profit, other
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
    otrassede = Column(String)
    logo = Column(String)
    slug = Column(String, index=True, unique=True)
    rutainformacion = Column(String, nullable=True)
    featured_espacio = Column(Boolean, default=False)
    validated = Column(Boolean, default=False)
    company_validated = Column(Boolean, default=False)
    show = Column(Boolean, default=True)
    comentario = Column(String, nullable=True) # Team internal comments

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
    show = Column(Boolean, default=True)

    operator = relationship("Company", back_populates="satellites")


class Launch(Base):
    __tablename__ = "launches"

    id = Column(Integer, primary_key=True, index=True)
    api_id = Column(String, unique=True, index=True) # ID from Space Devs API
    name = Column(String, index=True, nullable=False)
    name_mission = Column(String, nullable=True)  # Nombre de la misión (parte derecha del '|')

    rocket_id = Column(Integer, ForeignKey("rockets.id"))
    provider_id = Column(Integer, ForeignKey("companies.id"))
    net = Column(DateTime(timezone=True)) # Next Estimated Time (TIMESTAMP WITH TIME ZONE)
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
    show = Column(Boolean, default=True)

    rocket = relationship("Rocket", back_populates="launches")
    provider = relationship("Company", back_populates="launches")


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    title_en = Column(String, index=True)
    excerpt = Column(String)
    excerpt_en = Column(String)
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
    show = Column(Boolean, default=True)


class NewsSpaceX(Base):
    __tablename__ = "newsspacex"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    title_en = Column(String, index=True)
    excerpt = Column(String)
    excerpt_en = Column(String)
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
    show = Column(Boolean, default=True)


class SpaceXInventory(Base):
    __tablename__ = "spacex_inventory"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    title_en = Column(String, index=True)
    excerpt = Column(String)
    excerpt_en = Column(String)
    category = Column(String, index=True) # Starship, Super Heavy, Raptor, Test, Lanzamientos
    category_en = Column(String, index=True)
    location = Column(String) # Starbase, Florida
    location_en = Column(String)
    version = Column(String)
    datestartfabrication = Column(String, nullable=True)
    datesfinishfabrication = Column(String, nullable=True)
    state = Column(String) # desechado, destruido, retirado, en fabricación, en testing, activo, reutilizado
    state_en = Column(String)
    datelaunch = Column(String, nullable=True)
    resultlaunch = Column(String, nullable=True)
    resultlaunch_en = Column(String, nullable=True)
    covered = Column(Boolean, default=False)
    date = Column(String) # ISO format string for sorting/display
    image = Column(String)
    slug = Column(String, index=True, unique=True)
    tags = Column(JSON) # List of strings
    tags_en = Column(JSON) # List of strings
    featured = Column(Boolean, default=False)
    linkyoutube = Column(String, nullable=True)
    rutainformacion = Column(String, nullable=True)
    timestart = Column(Integer, nullable=True)
    show = Column(Boolean, default=True)
    # Extended fields for Starship program structured data
    serial_number = Column(String, nullable=True)   # e.g. "SN15", "B7", "R3-SN1"
    block = Column(String, nullable=True)           # e.g. "Block 1", "Block 2", "Block 3"
    specs = Column(JSON, nullable=True)             # Dict with technical parameters (thrust, Isp, mass, etc.)
    flight_data = Column(JSON, nullable=True)       # Dict with IFT flight outcome per stage
    milestones = Column(JSON, nullable=True)        # List of {date, event} dicts


class AppSetting(Base):
    __tablename__ = "app_settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)
    value = Column(String, nullable=False)
    type = Column(String, default="string")
    description = Column(String, nullable=True)


# ============================================================
# AUTH MODELS
# ============================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)

    # Roles y suscripción
    role = Column(String, default="free")                   # "free", "premium", "admin"
    subscription_status = Column(String, default="inactive") # "active", "inactive", "trial"
    subscription_expires_at = Column(DateTime(timezone=True), nullable=True)
    subscription_plan = Column(String, nullable=True)         # "monthly", "annual"

    # Proveedor de autenticación
    auth_provider = Column(String, default="magic_link")    # "magic_link", "google", "password"
    google_id = Column(String, unique=True, nullable=True)
    hashed_password = Column(String, nullable=True)         # Solo si usa password

    # Estado
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    # Relaciones
    magic_tokens = relationship("MagicLinkToken", back_populates="user")
    refresh_tokens = relationship("RefreshToken", back_populates="user")


class MagicLinkToken(Base):
    __tablename__ = "magic_link_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    token = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    purpose = Column(String, default="login")               # "login", "email_verify"
    used = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="magic_tokens")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String(500), unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    revoked = Column(Boolean, default=False)

    user = relationship("User", back_populates="refresh_tokens")


class MediaSource(Base):
    __tablename__ = "media_sources"

    # === Identificación ===
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)

    # === Clasificación ===
    category = Column(String, index=True, nullable=False) # 'portal', 'youtube', 'revista', 'podcast', etc.
    subcategory = Column(String)                          # 'divulgacion', 'industria', 'tecnico', etc.
    language = Column(String, index=True, default='en')   # 'es', 'en', 'multi'
    country = Column(String, index=True)                  # 'US', 'ES', etc.
    country_name = Column(String)

    # === Información Principal ===
    name = Column(String, nullable=False)
    description = Column(String)                         # TEXT
    description_en = Column(String)                      # TEXT
    tagline = Column(String)
    tagline_en = Column(String)

    # === Calificación ===
    rating = Column(Integer, default=3)                  # SMALLINT (1-5 estrellas)
    recommended = Column(Boolean, default=False)
    difficulty = Column(String, default='general')        # 'general', 'intermedio', 'avanzado', 'experto'

    # === Links ===
    website = Column(String)
    youtube_url = Column(String)
    youtube_handle = Column(String)
    twitter_url = Column(String)
    instagram_url = Column(String)
    linkedin_url = Column(String)
    spotify_url = Column(String)
    apple_podcasts_url = Column(String)
    rss_feed_url = Column(String)
    newsletter_url = Column(String)

    # === Metadatos de contenido ===
    content_format = Column(JSON)                        # List of strings
    topics = Column(JSON)                                # List of strings
    is_free = Column(Boolean, default=True)
    paywall = Column(Boolean, default=False)

    # === Control ===
    featured = Column(Boolean, index=True, default=False)
    show = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class Training(Base):
    __tablename__ = "training"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    name_en = Column(String)
    type = Column(String) # grade, master, phd, university
    name_file = Column(String) # markdown path/filename
    description = Column(String)
    description_en = Column(String)
    link = Column(String) # website link (mainly for universities)
    show = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class YouTubeVideo(Base):
    __tablename__ = "youtube"

    id = Column(Integer, primary_key=True, index=True)
    video_name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    type = Column(String)
    description = Column(String)
    description_en = Column(String)
    date = Column(String)
    own = Column(Boolean, default=False)
    show = Column(Boolean, default=True)



class ResearchDevelopment(Base):
    __tablename__ = "researchdevelopment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    name_en = Column(String)
    type = Column(String) # researchcenter, researchmagazine, paper, conference, estateoftheart
    description = Column(String)
    description_en = Column(String)
    show = Column(Boolean, default=True)
    link = Column(String)
    slug = Column(String, unique=True, index=True, nullable=False)
    file = Column(String) # markdown path/filename
    created_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    update_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True)
    namecourse = Column(String, index=True, nullable=False)
    chapter = Column(String)
    lesson = Column(String)
    slug = Column(String, unique=True, index=True, nullable=False)
    url_youtube = Column(String)
    markdown_file = Column(String) # Cloudinary URL
    orden_index = Column(Integer, default=0, index=True)
    show = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    title_en = Column(String, index=True)
    description = Column(String)
    description_en = Column(String)
    image_url = Column(String, nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=False)
    prediction_deadline = Column(DateTime(timezone=True), nullable=True)
    actual_event_date = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    prize_description = Column(String, nullable=True)
    prize_description_en = Column(String, nullable=True)
    prize_image_url = Column(String, nullable=True)
    type = Column(String, default="date") # 'date', 'choice', 'coordinate'
    options = Column(JSON, nullable=True) # For 'choice' type challenges
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    predictions = relationship("Prediction", back_populates="challenge")


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    nickname = Column(String, nullable=False)
    email = Column(String, index=True, nullable=False)
    prediction_value = Column(String, nullable=False) # Store the date or choice as string
    verification_code = Column(String, nullable=True) # Unique code sent by email
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    challenge = relationship("Challenge", back_populates="predictions")
