from app.database import SessionLocal
from app.models import AppSetting, News

def seed_featured_news():
    db = SessionLocal()
    try:
        # Get the first news item to use as featured if no specific one is provided
        first_news = db.query(News).first()
        if not first_news:
            print("No news found in database to feature.")
            return

        featured_id = str(first_news.id)
        
        # Check if setting already exists
        setting = db.query(AppSetting).filter(AppSetting.key == "featured_news_id").first()
        
        if setting:
            setting.value = featured_id
            print(f"Updated existing featured_news_id to: {featured_id}")
        else:
            new_setting = AppSetting(
                key="featured_news_id",
                value=featured_id,
                type="string",
                description="ID of the news item to be featured on the home page"
            )
            db.add(new_setting)
            print(f"Created new featured_news_id setting with value: {featured_id}")
            
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error seeding featured news: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_featured_news()
