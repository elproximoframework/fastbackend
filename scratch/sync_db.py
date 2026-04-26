from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

# Add parent dir to sys.path to import models if needed, 
# but here I will redefine them to be self-contained and safe.

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)

class ForumCategory(Base):
    __tablename__ = "forum_categories"
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(100), nullable=False)
    slug        = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(300), nullable=True)
    icon        = Column(String(10), nullable=True)
    color       = Column(String(20), default="#22d3ee")
    order       = Column(Integer, default=0)
    is_active   = Column(Boolean, default=True)
    created_at  = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ForumThread(Base):
    __tablename__ = "forum_threads"
    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(200), nullable=False, index=True)
    slug        = Column(String(220), unique=True, index=True, nullable=False)
    content     = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("forum_categories.id"), nullable=False)
    author_id   = Column(Integer, ForeignKey("users.id"), nullable=False)
    views       = Column(Integer, default=0)
    is_pinned   = Column(Boolean, default=False)
    is_locked   = Column(Boolean, default=False)
    created_at  = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at  = Column(DateTime(timezone=True))

class ForumPost(Base):
    __tablename__ = "forum_posts"
    id        = Column(Integer, primary_key=True, index=True)
    content   = Column(String, nullable=False)
    thread_id = Column(Integer, ForeignKey("forum_threads.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True))

class ForumPostLike(Base):
    __tablename__ = "forum_post_likes"
    id        = Column(Integer, primary_key=True, index=True)
    post_id   = Column(Integer, ForeignKey("forum_posts.id"), nullable=False)
    user_id   = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    __table_args__ = (UniqueConstraint("post_id", "user_id", name="uq_post_like"),)

LOCAL_DB_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_DB_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def sync():
    print("Connecting to local database...")
    local_engine = create_engine(LOCAL_DB_URL)
    LocalSession = sessionmaker(bind=local_engine)
    local_session = LocalSession()

    print("Connecting to remote database...")
    remote_engine = create_engine(REMOTE_DB_URL)
    RemoteSession = sessionmaker(bind=remote_engine)
    remote_session = RemoteSession()

    print("Creating tables on remote if they don't exist...")
    try:
        # Create all tables defined in this file (ForumCategory, etc.)
        Base.metadata.create_all(remote_engine)
        print("Forum tables confirmed/created on remote.")
    except Exception as e:
        print(f"Error creating tables: {e}")

    print("Fetching data from local forum_categories...")
    categories = local_session.query(ForumCategory).all()
    print(f"Found {len(categories)} categories.")

    print("Syncing categories to remote...")
    for cat in categories:
        # Check if exists
        exists = remote_session.query(ForumCategory).filter_by(id=cat.id).first()
        if not exists:
            # Create a new instance for remote session
            new_cat = ForumCategory(
                id=cat.id,
                name=cat.name,
                slug=cat.slug,
                description=cat.description,
                icon=cat.icon,
                color=cat.color,
                order=cat.order,
                is_active=cat.is_active,
                created_at=cat.created_at
            )
            remote_session.add(new_cat)
            print(f"Added category ID: {cat.id}")
        else:
            print(f"Category ID {cat.id} already exists on remote.")

    try:
        remote_session.commit()
        print("Success! Data synced to remote.")
    except Exception as e:
        remote_session.rollback()
        print(f"Error committing to remote: {e}")
    finally:
        local_session.close()
        remote_session.close()

if __name__ == "__main__":
    sync()
