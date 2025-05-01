from django.apps import apps
from celery import shared_task
from helpers.reading import GoogleSheetPoster
from products.models import ProductsBaseModel, ScrapedProductDataModel
from helpers.cassi import get_session
from helpers.scraper import Scraper
from datetime import datetime, timezone

@shared_task
def process_google_sheet_data():
    poster = GoogleSheetPoster()
    poster.run()
    print("Google Sheet data has been processed.")



@shared_task
def full_ingest_scrape_and_track():
    print("🔁 Starting full ingestion and scrape task...")
    get_session()  # Maintain single Cassandra session
    # GoogleSheetPoster().run()

    all_asins = [p.asin for p in ProductsBaseModel.objects().all()]
    print(f"📦 Scraping {len(all_asins)} ASINs...")

    for asin in all_asins:
        try:
            scraper = Scraper(asin=asin)
            data = scraper.scrape()
            if data:
                ScrapedProductDataModel.create(
                    asin=asin,
                    title=data.get("title"),
                    price=data.get("price"),
                    total=data.get("total"),
                    description=data.get("description"),
                    image_url=data.get("image_url"),
                    rating=data.get("rating"),
                    total_reviews=data.get("total_reviews"),
                    # reviews=data.get("reviews"),
                    updated_at=datetime.now(timezone.utc),
                )
                print(f"✅ Scraped and stored: {asin}")
        except Exception as e:
            print(f"❌ Error for {asin}: {e}")