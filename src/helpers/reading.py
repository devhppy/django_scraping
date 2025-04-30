# from .google_apis import create_service
# from decouple import config, UndefinedValueError
# import requests

# class GoogleSheetPoster:
#     def __init__(self):
#         self.spreadsheet_id = config("GOOGLE_SPREADSHEET_ID")
#         try:
#             self.api_endpoint = config("GOOGLE_API_ENDPOINT")
#         except UndefinedValueError:
#             print("⚠️ GOOGLE_API_ENDPOINT not found. POST requests will be skipped.")
#             self.api_endpoint = None
#         self.service = self._create_service()

#     def _create_service(self):
#         return create_service(
#             api_name='sheets',
#             api_version='v4',
#             scopes=['https://www.googleapis.com/auth/spreadsheets']
#         )

#     def get_sheet_names(self):
#         try:
#             spreadsheet = self.service.spreadsheets().get(
#                 spreadsheetId=self.spreadsheet_id
#             ).execute()
#             sheet_names = [sheet['properties']['title'] for sheet in spreadsheet.get('sheets', [])]
#             print(f"📄 Sheets found: {', '.join(sheet_names)}")
#             # return [sheet['properties']['title'] for sheet in spreadsheet.get('sheets', [])]
#             return sheet_names
#         except Exception as e:
#             print(f"Failed to get sheet names: {e}")
#             return ['Sheet1']

#     def read_all_sheet_data(self):
#         all_data = []
#         for sheet in self.get_sheet_names():
#             try:
#                 result = self.service.spreadsheets().values().get(
#                     spreadsheetId=self.spreadsheet_id,
#                     range=sheet
#                 ).execute()
#                 values = result.get('values', [])
#                 all_data.append((sheet, values))
#             except Exception as e:
#                 print(f"Failed to read sheet '{sheet}': {e}")
#         return all_data

#     def post_rows(self, sheet_name, rows):
#         if not rows:
#             print(f'No data found in sheet: {sheet_name}')
#             return

#         headers = rows[0]
#         data_rows = rows[1:]

#         success = 0
#         fail = 0

#         for row in data_rows:
#             payload = dict(zip(headers, row))
#             payload['niche'] = sheet_name

#             try:
#                 response = requests.post(self.api_endpoint, json=payload)
#                 if response.status_code == 200:
#                     print(f"✅ Posted: {payload}")
#                     success += 1
#                 else:
#                     print(f"❌ Failed ({response.status_code}): {response.text}")
#                     fail += 1
#             except Exception as e:
#                 print(f"❌ Error: {e}")
#                 fail += 1

#         print(f"\n✅ Success: {success}, ❌ Failures: {fail}\n")

#     def run(self):
#         all_data = self.read_all_sheet_data()
#         for sheet_name, rows in all_data:
#             self.post_rows(sheet_name, rows)
#         print("📤 All sheet data processed.")


# from .google_apis import create_service
# from decouple import config, UndefinedValueError
# import requests
# from products.models import ProductsBaseModel

# class GoogleSheetPoster:
#     def __init__(self):
#         self.spreadsheet_id = config("GOOGLE_SPREADSHEET_ID")
#         try:
#             self.api_endpoint = config("GOOGLE_API_ENDPOINT")
#         except UndefinedValueError:
#             print("⚠️ GOOGLE_API_ENDPOINT not found. POST requests will be skipped.")
#             self.api_endpoint = None
#         self.service = self._create_service()

#     def _create_service(self):
#         return create_service(
#             api_name='sheets',
#             api_version='v4',
#             scopes=['https://www.googleapis.com/auth/spreadsheets']
#         )

#     def get_sheet_names(self):
#         try:
#             spreadsheet = self.service.spreadsheets().get(
#                 spreadsheetId=self.spreadsheet_id
#             ).execute()
#             sheet_names = [sheet['properties']['title'] for sheet in spreadsheet.get('sheets', [])]
#             print(f"📄 Sheets found: {', '.join(sheet_names)}")
#             return sheet_names
#         except Exception as e:
#             print(f"Failed to get sheet names: {e}")
#             return ['Sheet1']

#     def read_all_sheet_data(self):
#         all_data = []
#         for sheet in self.get_sheet_names():
#             try:
#                 result = self.service.spreadsheets().values().get(
#                     spreadsheetId=self.spreadsheet_id,
#                     range=sheet
#                 ).execute()
#                 values = result.get('values', [])
#                 all_data.append((sheet, values))
#             except Exception as e:
#                 print(f"Failed to read sheet '{sheet}': {e}")
#         return all_data

#     def post_rows(self, sheet_name, rows):
#         if not rows:
#             print(f'No data found in sheet: {sheet_name}')
#             return

#         headers = rows[0]
#         data_rows = rows[1:]

#         success = 0
#         fail = 0

#         for row in data_rows:
#             payload = dict(zip(headers, row))
#             payload['niche'] = sheet_name

#             # Insert into AstraDB if not already present
#             try:
#                 asin = payload.get('asin')
#                 if asin and not ProductsBaseModel.objects.filter(asin=asin).exists():
#                     product = ProductsBaseModel.create(
#                         asin=asin,
#                         niche=sheet_name,
#                         affiliate_link=payload.get('affiliate_link', ''),
#                     )
#                     print(f"✅ Product added: {product}")
#                     success += 1
#                 else:
#                     print(f"❌ Product with ASIN {asin} already exists.")
#                     fail += 1
#             except Exception as e:
#                 print(f"❌ Error inserting data into AstraDB: {e}")
#                 fail += 1

#         print(f"\n✅ Success: {success}, ❌ Failures: {fail}\n")

#     def run(self):
#         all_data = self.read_all_sheet_data()
#         for sheet_name, rows in all_data:
#             self.post_rows(sheet_name, rows)
#         print("📤 All sheet data processed.")


# import logging
# from decouple import config, UndefinedValueError
# from .google_apis import create_service
# from products.models import ProductsBaseModel
# from datetime import datetime, timezone

# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


# class GoogleSheetPoster:
#     def __init__(self):
#         self.spreadsheet_id = config("GOOGLE_SPREADSHEET_ID")

#         try:
#             self.api_endpoint = config("GOOGLE_API_ENDPOINT")
#         except UndefinedValueError:
#             logger.warning("⚠️ GOOGLE_API_ENDPOINT not found, using Astra CRUD only.")
#             self.api_endpoint = None

#         self.service = self._create_service()

#     def _create_service(self):
#         return create_service(
#             api_name="sheets",
#             api_version="v4",
#             scopes=["https://www.googleapis.com/auth/spreadsheets"],
#         )

#     def get_sheet_names(self):
#         try:
#             resp = (
#                 self.service.spreadsheets()
#                 .get(spreadsheetId=self.spreadsheet_id)
#                 .execute()
#             )
#             names = [s["properties"]["title"] for s in resp.get("sheets", [])]
#             logger.info(f"Sheets found: {names}")
#             return names
#         except Exception as e:
#             logger.error(f"Failed to list sheets: {e}")
#             return []

#     def read_all_sheet_data(self):
#         out = []
#         for title in self.get_sheet_names():
#             try:
#                 result = (
#                     self.service.spreadsheets()
#                     .values()
#                     .get(spreadsheetId=self.spreadsheet_id, range=title)
#                     .execute()
#                 )
#                 rows = result.get("values", [])
#                 out.append((title, rows))
#                 logger.info(f"Read {len(rows)-1} data rows from '{title}'")
#             except Exception as e:
#                 logger.error(f"Error reading '{title}': {e}")
#         return out

#     def post_rows(self, sheet_name, rows):
#         if not rows or len(rows) < 2:
#             logger.warning(f"No data in sheet '{sheet_name}'")
#             return

#         headers = rows[0]
#         data_rows = rows[1:]

#         created, updated, skipped, errors = 0, 0, 0, 0

#         for row in data_rows:
#             # Skip if too few columns
#             if len(row) < len(headers):
#                 logger.warning(f"Skipping incomplete row: {row}")
#                 skipped += 1
#                 continue

#             record = dict(zip(headers, row))
#             asin = record.get("asin", "").strip()
#             if not asin:
#                 logger.warning(f"Row missing ASIN, skipping: {record}")
#                 skipped += 1
#                 continue

#             affiliate_link = record.get("affiliate_link", "").strip()
#             niche = sheet_name
#             now = datetime.now(timezone.utc)

#             try:
#                 # Try to get existing
#                 obj = ProductsBaseModel.objects.filter(asin=asin).first()
#                 if obj:
#                     # Update only if something changed
#                     changed = False
#                     if obj.affiliate_link != affiliate_link:
#                         obj.affiliate_link = affiliate_link
#                         changed = True
#                     if obj.niche != niche:
#                         obj.niche = niche
#                         changed = True
#                     if changed:
#                         obj.created_at = now
#                         obj.save()
#                         logger.info(f"🔄 Updated ASIN={asin}")
#                         updated += 1
#                     else:
#                         logger.info(f"⏭️ No change ASIN={asin}")
#                         skipped += 1
#                 else:
#                     # Create new
#                     ProductsBaseModel.objects.create(
#                         asin=asin,
#                         niche=niche,
#                         affiliate_link=affiliate_link,
#                         created_at=now,
#                     )
#                     logger.info(f"✅ Created ASIN={asin}")
#                     created += 1

#             except Exception as e:
#                 logger.error(f"❌ Error on ASIN={asin}: {e}")
#                 errors += 1

#         logger.info(
#             f"Sheet '{sheet_name}': Created={created}, Updated={updated}, "
#             f"Skipped={skipped}, Errors={errors}"
#         )

#     def run(self):
#         logger.info("▶️ Starting sheet sync")
#         all_data = self.read_all_sheet_data()
#         for sheet, rows in all_data:
#             self.post_rows(sheet, rows)
#         logger.info("✅ All sheets processed")


# import logging
# from decouple import config, UndefinedValueError
# from .google_apis import create_service
# from datetime import datetime, timezone

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# handler = logging.StreamHandler()
# handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
# logger.addHandler(handler)

# class GoogleSheetPoster:
#     def __init__(self):
#         self.spreadsheet_id = config("GOOGLE_SPREADSHEET_ID")
#         try:
#             self.api_endpoint = config("GOOGLE_API_ENDPOINT")
#         except UndefinedValueError:
#             logger.warning("⚠️ No GOOGLE_API_ENDPOINT configured; skipping POST.")
#             self.api_endpoint = None
#         self.service = self._create_service()

#     def _create_service(self):
#         return create_service(
#             api_name="sheets",
#             api_version="v4",
#             scopes=["https://www.googleapis.com/auth/spreadsheets"],
#         )

#     def get_sheet_names(self):
#         try:
#             meta = self.service.spreadsheets().get(
#                 spreadsheetId=self.spreadsheet_id
#             ).execute()
#             names = [s["properties"]["title"] for s in meta.get("sheets", [])]
#             logger.info(f"Sheets found: {names}")
#             return names
#         except Exception as e:
#             logger.error(f"Error listing sheets: {e}")
#             return []

#     def read_all_sheet_data(self):
#         data = []
#         for title in self.get_sheet_names():
#             try:
#                 resp = self.service.spreadsheets().values().get(
#                     spreadsheetId=self.spreadsheet_id, range=title
#                 ).execute()
#                 rows = resp.get("values", [])
#                 logger.info(f"Read {len(rows)-1} rows from '{title}'")
#                 data.append((title, rows))
#             except Exception as e:
#                 logger.error(f"Error reading sheet '{title}': {e}")
#         return data

#     def post_rows(self, sheet_name, rows):
#         if not rows or len(rows) < 2:
#             logger.warning(f"No data in sheet '{sheet_name}', skipping.")
#             return

#         headers, data_rows = rows[0], rows[1:]
#         created, updated, skipped, errors = 0, 0, 0, 0

#         for row in data_rows:
#             # Skip incomplete rows
#             if len(row) < len(headers):
#                 skipped += 1
#                 logger.warning(f"Incomplete row, skipping: {row}")
#                 continue

#             payload = dict(zip(headers, row))
#             asin = payload.get("asin", "").strip()
#             if not asin:
#                 skipped += 1
#                 logger.warning(f"No ASIN, skipping: {payload}")
#                 continue

#             affiliate_link = payload.get("affiliate_link", "").strip()
#             niche = sheet_name
#             now = datetime.now(timezone.utc)

#             try:
#                 # Import model here so Django apps are ready
#                 from products.models import ProductsBaseModel

#                 existing = ProductsBaseModel.objects.filter(asin=asin).first()
#                 if existing:
#                     changed = False
#                     if existing.affiliate_link != affiliate_link:
#                         existing.affiliate_link = affiliate_link
#                         changed = True
#                     if existing.niche != niche:
#                         existing.niche = niche
#                         changed = True
#                     if changed:
#                         existing.created_at = now
#                         existing.save()
#                         updated += 1
#                         logger.info(f"Updated ASIN={asin}")
#                     else:
#                         skipped += 1
#                         logger.info(f"No change for ASIN={asin}")
#                 else:
#                     ProductsBaseModel.objects.create(
#                         asin=asin,
#                         niche=niche,
#                         affiliate_link=affiliate_link,
#                         created_at=now,
#                     )
#                     created += 1
#                     logger.info(f"Created ASIN={asin}")

#             except Exception as e:
#                 errors += 1
#                 logger.error(f"Error upserting ASIN={asin}: {e}")

#         logger.info(
#             f"Sheet '{sheet_name}' results: created={created}, "
#             f"updated={updated}, skipped={skipped}, errors={errors}"
#         )

#     def run(self):
#         logger.info("Starting GoogleSheetPoster.run()")
#         for sheet_name, rows in self.read_all_sheet_data():
#             self.post_rows(sheet_name, rows)
#         logger.info("GoogleSheetPoster.run() completed")


# import logging
# from decouple import config
# from .google_apis import create_service
# from datetime import datetime, timezone

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# handler = logging.StreamHandler()
# handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
# logger.addHandler(handler)

# class GoogleSheetPoster:
#     def __init__(self):
#         # Load only the spreadsheet ID now
#         self.spreadsheet_id = config("GOOGLE_SPREADSHEET_ID")
#         self.service = self._create_service()

#     def _create_service(self):
#         return create_service(
#             api_name="sheets",
#             api_version="v4",
#             scopes=["https://www.googleapis.com/auth/spreadsheets"],
#         )

#     def get_sheet_names(self):
#         try:
#             meta = self.service.spreadsheets().get(
#                 spreadsheetId=self.spreadsheet_id
#             ).execute()
#             names = [s["properties"]["title"] for s in meta.get("sheets", [])]
#             logger.info(f"Sheets found: {names}")
#             return names
#         except Exception as e:
#             logger.error(f"Error listing sheets: {e}")
#             return []

#     def read_all_sheet_data(self):
#         data = []
#         for title in self.get_sheet_names():
#             try:
#                 resp = self.service.spreadsheets().values().get(
#                     spreadsheetId=self.spreadsheet_id,
#                     range=title
#                 ).execute()
#                 rows = resp.get("values", [])
#                 logger.info(f"Read {len(rows)-1} data rows from '{title}'")
#                 data.append((title, rows))
#             except Exception as e:
#                 logger.error(f"Error reading sheet '{title}': {e}")
#         return data

#     def post_rows(self, sheet_name, rows):
#         # skip sheets with only header or no rows
#         if not rows or len(rows) < 2:
#             logger.info(f"No data rows in sheet '{sheet_name}', skipping.")
#             return

#         headers, data_rows = rows[0], rows[1:]
#         created = updated = skipped = errors = 0

#         for row in data_rows:
#             # skip incomplete rows
#             if len(row) < len(headers):
#                 skipped += 1
#                 logger.warning(f"Incomplete row, skipping: {row}")
#                 continue

#             payload = dict(zip(headers, row))
#             asin = payload.get("asin", "").strip()
#             if not asin:
#                 skipped += 1
#                 logger.warning(f"No ASIN in row, skipping: {payload}")
#                 continue

#             affiliate_link = payload.get("affiliate_link", "").strip()
#             niche = sheet_name
#             now = datetime.now(timezone.utc)

#             try:
#                 # import model here so apps are loaded
#                 from products.models import ProductsBaseModel

#                 existing = ProductsBaseModel.objects.filter(asin=asin).first()
#                 if existing:
#                     changed = False
#                     if existing.affiliate_link != affiliate_link:
#                         existing.affiliate_link = affiliate_link
#                         changed = True
#                     if existing.niche != niche:
#                         existing.niche = niche
#                         changed = True
#                     if changed:
#                         existing.created_at = now
#                         existing.save()
#                         updated += 1
#                         logger.info(f"Updated ASIN={asin}")
#                     else:
#                         skipped += 1
#                         logger.info(f"No change for ASIN={asin}")
#                 else:
#                     ProductsBaseModel.create(
#                         asin=asin,
#                         niche=niche,
#                         affiliate_link=affiliate_link,
#                         created_at=now
#                     )
#                     created += 1
#                     logger.info(f"Created ASIN={asin}")

#             except Exception as e:
#                 errors += 1
#                 logger.error(f"Error upserting ASIN={asin}: {e}")

#         logger.info(
#             f"Sheet '{sheet_name}' results: created={created}, "
#             f"updated={updated}, skipped={skipped}, errors={errors}"
#         )

#     def run(self):
#         logger.info("Starting GoogleSheetPoster.run()")
#         for sheet_name, rows in self.read_all_sheet_data():
#             self.post_rows(sheet_name, rows)
#         logger.info("GoogleSheetPoster.run() completed")


# import logging
# from decouple import config
# from .google_apis import create_service
# from datetime import datetime, timezone
# from cassandra.cqlengine.query import DoesNotExist

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# handler = logging.StreamHandler()
# handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
# logger.addHandler(handler)

# class GoogleSheetPoster:
#     def __init__(self):
#         self.spreadsheet_id = config("GOOGLE_SPREADSHEET_ID")
#         self.service = self._create_service()

#     def _create_service(self):
#         return create_service(
#             api_name="sheets",
#             api_version="v4",
#             scopes=["https://www.googleapis.com/auth/spreadsheets"],
#         )

#     def get_sheet_names(self):
#         try:
#             meta = self.service.spreadsheets().get(
#                 spreadsheetId=self.spreadsheet_id
#             ).execute()
#             names = [s["properties"]["title"] for s in meta.get("sheets", [])]
#             logger.info(f"Sheets found: {names}")
#             return names
#         except Exception as e:
#             logger.error(f"Error listing sheets: {e}")
#             return []

#     def read_all_sheet_data(self):
#         data = []
#         for title in self.get_sheet_names():
#             try:
#                 resp = self.service.spreadsheets().values().get(
#                     spreadsheetId=self.spreadsheet_id,
#                     range=title
#                 ).execute()
#                 rows = resp.get("values", [])
#                 logger.info(f"Read {len(rows)-1} data rows from '{title}'")
#                 data.append((title, rows))
#             except Exception as e:
#                 logger.error(f"Error reading sheet '{title}': {e}")
#         return data

#     def post_rows(self, sheet_name, rows):
#         if not rows or len(rows) < 2:
#             logger.info(f"No data rows in sheet '{sheet_name}', skipping.")
#             return

#         headers, data_rows = rows[0], rows[1:]
#         created = updated = skipped = errors = 0

#         from products.models import ProductsBaseModel

#         for row in data_rows:
#             if len(row) < len(headers):
#                 skipped += 1
#                 logger.warning(f"Incomplete row, skipping: {row}")
#                 continue

#             payload = dict(zip(headers, row))
#             asin = payload.get("asin", "").strip()
#             if not asin:
#                 skipped += 1
#                 logger.warning(f"No ASIN in row, skipping: {payload}")
#                 continue

#             affiliate_link = payload.get("affiliate_link", "").strip()
#             niche = sheet_name
#             now = datetime.now(timezone.utc)

#             try:
#                 existing = ProductsBaseModel.objects.filter(asin=asin).first()

#                 if existing:
#                     changed = False
#                     if existing.affiliate_link != affiliate_link:
#                         existing.affiliate_link = affiliate_link
#                         changed = True
#                     if existing.niche != niche:
#                         existing.niche = niche
#                         changed = True
#                     if changed:
#                         existing.created_at = now
#                         existing.save()
#                         updated += 1
#                         logger.info(f"Updated ASIN={asin}")
#                     else:
#                         skipped += 1
#                         logger.info(f"No change for ASIN={asin}")
#                 else:
#                     # ✅ Use CQLengine's `create` method
#                     ProductsBaseModel.create(
#                         asin=asin,
#                         niche=niche,
#                         affiliate_link=affiliate_link,
#                         created_at=now
#                     )
#                     created += 1
#                     logger.info(f"Created ASIN={asin}")

#             except Exception as e:
#                 errors += 1
#                 logger.error(f"Error upserting ASIN={asin}: {e}")

#         logger.info(
#             f"Sheet '{sheet_name}' results: created={created}, "
#             f"updated={updated}, skipped={skipped}, errors={errors}"
#         )

#     def run(self):
#         logger.info("Starting GoogleSheetPoster.run()")
#         for sheet_name, rows in self.read_all_sheet_data():
#             self.post_rows(sheet_name, rows)
#         logger.info("GoogleSheetPoster.run() completed")


import logging
from decouple import config
from .google_apis import create_service
from datetime import datetime, timezone
from cassandra.cqlengine.query import DoesNotExist

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)

class GoogleSheetPoster:
    def __init__(self):
        self.spreadsheet_id = config("GOOGLE_SPREADSHEET_ID")
        self.service = self._create_service()

    def _create_service(self):
        return create_service(
            api_name="sheets",
            api_version="v4",
            scopes=["https://www.googleapis.com/auth/spreadsheets"],
        )

    def get_sheet_names(self):
        try:
            meta = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            names = [s["properties"]["title"] for s in meta.get("sheets", [])]
            logger.info(f"Sheets found: {names}")
            print(f"[INFO] Sheets found: {names}")
            return names
        except Exception as e:
            logger.error(f"Error listing sheets: {e}")
            print(f"[ERROR] Error listing sheets: {e}")
            return []

    def read_all_sheet_data(self):
        data = []
        for title in self.get_sheet_names():
            try:
                resp = self.service.spreadsheets().values().get(
                    spreadsheetId=self.spreadsheet_id,
                    range=title
                ).execute()
                rows = resp.get("values", [])
                logger.info(f"Read {len(rows)-1} data rows from '{title}'")
                print(f"[INFO] Read {len(rows)-1} data rows from '{title}'")
                data.append((title, rows))
            except Exception as e:
                logger.error(f"Error reading sheet '{title}': {e}")
                print(f"[ERROR] Error reading sheet '{title}': {e}")
        return data

    def post_rows(self, sheet_name, rows):
        if not rows or len(rows) < 2:
            logger.info(f"No data rows in sheet '{sheet_name}', skipping.")
            print(f"[INFO] No data rows in sheet '{sheet_name}', skipping.")
            return

        headers, data_rows = rows[0], rows[1:]
        created = updated = skipped = errors = 0

        from products.models import ProductsBaseModel

        for row in data_rows:
            if len(row) < len(headers):
                skipped += 1
                logger.warning(f"Incomplete row, skipping: {row}")
                print(f"[WARN] Incomplete row, skipping: {row}")
                continue

            # Normalize headers to lowercase
            payload = {k.lower(): v for k, v in zip(headers, row)}
            asin = payload.get("asin", "").strip()
            if not asin:
                skipped += 1
                logger.warning(f"No ASIN in row, skipping: {payload}")
                print(f"[WARN] No ASIN in row, skipping: {payload}")
                continue

            affiliate_link = payload.get("affiliate_link", "").strip()
            niche = sheet_name
            now = datetime.now(timezone.utc)

            try:
                try:
                    existing = ProductsBaseModel.objects.get(asin=asin)
                except DoesNotExist:
                    existing = None

                if existing:
                    changed = False
                    if existing.affiliate_link != affiliate_link:
                        existing.affiliate_link = affiliate_link
                        changed = True
                    if existing.niche != niche:
                        existing.niche = niche
                        changed = True
                    if changed:
                        existing.created_at = now
                        existing.save()
                        updated += 1
                        logger.info(f"Updated ASIN={asin}")
                        print(f"[UPDATE] Updated ASIN={asin}")
                    else:
                        skipped += 1
                        logger.info(f"No change for ASIN={asin}")
                        print(f"[SKIP] No change for ASIN={asin}")
                else:
                    ProductsBaseModel.create(
                        asin=asin,
                        niche=niche,
                        affiliate_link=affiliate_link,
                        created_at=now
                    )
                    created += 1
                    logger.info(f"Created ASIN={asin}")
                    print(f"[CREATE] Created ASIN={asin}")

            except Exception as e:
                errors += 1
                logger.error(f"Error upserting ASIN={asin}: {e}")
                print(f"[ERROR] Error upserting ASIN={asin}: {e}")

        logger.info(
            f"Sheet '{sheet_name}' results: created={created}, "
            f"updated={updated}, skipped={skipped}, errors={errors}"
        )
        print(
            f"[RESULTS] Sheet '{sheet_name}': created={created}, "
            f"updated={updated}, skipped={skipped}, errors={errors}"
        )

    def run(self):
        from helpers.cassi import get_session
        get_session()
        logger.info("Starting GoogleSheetPoster.run()")
        print("[START] Running GoogleSheetPoster...")
        for sheet_name, rows in self.read_all_sheet_data():
            self.post_rows(sheet_name, rows)
        logger.info("GoogleSheetPoster.run() completed")
        print("[DONE] GoogleSheetPoster run completed.")
