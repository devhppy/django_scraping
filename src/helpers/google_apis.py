import os
import json
from decouple import config
import subprocess
import sys

def safe_import(module_name, package_name=None):
    try:
        return __import__(module_name, fromlist=[""])
    except ModuleNotFoundError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name or module_name])
        return __import__(module_name, fromlist=[""])

# Importing individual modules with fallback installation
flow_module = safe_import("google_auth_oauthlib.flow", "google-auth-oauthlib")
googleapiclient_module = safe_import("googleapiclient.discovery", "google-api-python-client")
creds_module = safe_import("google.oauth2.credentials", "google-auth")
transport_module = safe_import("google.auth.transport.requests", "google-auth")

# Assigning imported classes/functions to variables
InstalledAppFlow = flow_module.InstalledAppFlow
build = googleapiclient_module.build
Credentials = creds_module.Credentials
Request = transport_module.Request

def create_service(api_name, api_version, scopes, prefix=''):
    SCOPES = scopes
    creds = None

    # Directory to store token files
    token_dir = os.path.join(os.getcwd(), 'token_files')
    os.makedirs(token_dir, exist_ok=True)

    # Token filename
    token_file = f'token_{api_name}_{api_version}_{prefix}.json'
    token_path = os.path.join(token_dir, token_file)

    # Create a temporary client secret file from .env
    client_config = {
        "installed": {
            "client_id": config("GOOGLE_CLIENT_ID"),
            "project_id": config("GOOGLE_PROJECT_ID"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": config("GOOGLE_CLIENT_SECRET"),
            "redirect_uris": [config("GOOGLE_API_REDIRECT_URI")]
        }
    }

    credentials_file_path = os.path.join(token_dir, "client_secret_temp.json")
    try:
        with open(credentials_file_path, "w") as f:
            json.dump(client_config, f)

        # Load token if it exists
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        # Refresh or create new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file_path, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the token for future use
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        # Build the API service
        service = build(api_name, api_version, credentials=creds, static_discovery=False)
        print(f"✅ {api_name} service created successfully.")
        return service

    except Exception as e:
        print(f"❌ Error creating {api_name} service: {e}")
        return None

    finally:
        # Clean up the temporary client secret file
        if os.path.exists(credentials_file_path):
            os.remove(credentials_file_path)