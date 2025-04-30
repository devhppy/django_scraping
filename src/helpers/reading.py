from .google_apis import create_service
from decouple import config, UndefinedValueError
import requests

class GoogleSheetPoster:
    def __init__(self):
        self.spreadsheet_id = config("GOOGLE_SPREADSHEET_ID")
        try:
            self.api_endpoint = config("GOOGLE_API_ENDPOINT")
        except UndefinedValueError:
            print("⚠️ GOOGLE_API_ENDPOINT not found. POST requests will be skipped.")
            self.api_endpoint = None
        self.service = self._create_service()

    def _create_service(self):
        return create_service(
            api_name='sheets',
            api_version='v4',
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )

    def get_sheet_names(self):
        try:
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            sheet_names = [sheet['properties']['title'] for sheet in spreadsheet.get('sheets', [])]
            print(f"📄 Sheets found: {', '.join(sheet_names)}")
            # return [sheet['properties']['title'] for sheet in spreadsheet.get('sheets', [])]
            return sheet_names
        except Exception as e:
            print(f"Failed to get sheet names: {e}")
            return ['Sheet1']

    def read_all_sheet_data(self):
        all_data = []
        for sheet in self.get_sheet_names():
            try:
                result = self.service.spreadsheets().values().get(
                    spreadsheetId=self.spreadsheet_id,
                    range=sheet
                ).execute()
                values = result.get('values', [])
                all_data.append((sheet, values))
            except Exception as e:
                print(f"Failed to read sheet '{sheet}': {e}")
        return all_data

    def post_rows(self, sheet_name, rows):
        if not rows:
            print(f'No data found in sheet: {sheet_name}')
            return

        headers = rows[0]
        data_rows = rows[1:]

        success = 0
        fail = 0

        for row in data_rows:
            payload = dict(zip(headers, row))
            payload['niche'] = sheet_name

            try:
                response = requests.post(self.api_endpoint, json=payload)
                if response.status_code == 200:
                    print(f"✅ Posted: {payload}")
                    success += 1
                else:
                    print(f"❌ Failed ({response.status_code}): {response.text}")
                    fail += 1
            except Exception as e:
                print(f"❌ Error: {e}")
                fail += 1

        print(f"\n✅ Success: {success}, ❌ Failures: {fail}\n")

    def run(self):
        all_data = self.read_all_sheet_data()
        for sheet_name, rows in all_data:
            self.post_rows(sheet_name, rows)
        print("📤 All sheet data processed.")
