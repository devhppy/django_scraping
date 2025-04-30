from django.apps import apps
from celery import shared_task
from helpers.reading import GoogleSheetPoster



@shared_task
def process_google_sheet_data():
    poster = GoogleSheetPoster()
    poster.run()
    print("Google Sheet data has been processed.")