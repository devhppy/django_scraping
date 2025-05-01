# from cassandra.cqlengine.management import sync_table
# from decouple import config
# from cassandra.cluster import Cluster

# import base64
# import tempfile
# import os

# import logging

# logger = logging.getLogger(__name__)


# ASTRA_BUNDLE_B64 = config("ASTRA_BUNDLE_B64", default=None)
# ASTRA_CLIENT_ID = config("ASTRA_CLIENT_ID", default=None)
# ASTRA_CLIENT_SECRET = config("ASTRA_CLIENT_SECRET", default=None)

# if ASTRA_BUNDLE_B64:
#     decoded_zip_path = os.path.join(tempfile.gettempdir(), "secure_connect_bundle.zip")
#     with open(decoded_zip_path, "wb") as f:
#         f.write(base64.b64decode(ASTRA_BUNDLE_B64))
#     SECURE_CONNECT_BUNDLE_PATH = decoded_zip_path

# def sync_all_tables():
#     logger.info("Starting sync_all_tables()...")

#     """
#     Call this during Django or Celery app initialization
#     to ensure Cassandra tables are synced.
#     """
#     from cassandra.auth import PlainTextAuthProvider

#     from products.models import ProductsBaseModel
#     sync_table(ProductsBaseModel)
#     logger.info("sync_all_tables() completed.")

# import os
# import zipfile
# import base64
# import tempfile
# import logging
# from decouple import config
# from cassandra.cqlengine.management import sync_table
# from cassandra.auth import PlainTextAuthProvider
# from cassandra.cluster import Cluster
# from cassandra.cqlengine.connection import register_connection, set_default_connection

# logger = logging.getLogger(__name__)

# # Read environment variables
# ASTRA_BUNDLE_B64 = config("ASTRA_BUNDLE_B64", default=None)
# ASTRA_CLIENT_ID = config("ASTRA_CLIENT_ID", default=None)
# ASTRA_CLIENT_SECRET = config("ASTRA_CLIENT_SECRET", default=None)

# # Path for the secure connect bundle
# # Decode Secure_Connect.zip from base64 if provided
# ASTRA_BUNDLE_B64 = config("ASTRA_BUNDLE_B64", default=None)

# if ASTRA_BUNDLE_B64:
#     decoded_zip_path = os.path.join(tempfile.gettempdir(), "secure_connect_bundle.zip")
#     with open(decoded_zip_path, "wb") as f:
#         f.write(base64.b64decode(ASTRA_BUNDLE_B64))
#     SECURE_CONNECT_BUNDLE_PATH = decoded_zip_path


# def get_cluster():
#     """
#     Validates the secure connect bundle, loads credentials, 
#     and returns a Cassandra Cluster object.
#     """
#     if not SECURE_CONNECT_BUNDLE_PATH or not ASTRA_CLIENT_ID or not ASTRA_CLIENT_SECRET:
#         raise ValueError("❌ Missing required environment variables for Astra DB connection.")
    
#     # Set up authentication provider
#     auth_provider = PlainTextAuthProvider(ASTRA_CLIENT_ID, ASTRA_CLIENT_SECRET)
#     cloud_config = {'secure_connect_bundle': SECURE_CONNECT_BUNDLE_PATH}

#     try:
#         logger.info("Connecting to Astra DB...")
#         cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider, protocol_version=4)
#         logger.info("Connected to Astra DB cluster.")
#     except Exception as e:
#         raise ConnectionError(f"❌ Error connecting to cluster: {e}")

#     return cluster


# def get_session():
#     """
#     Connects to the Cassandra cluster, sets the keyspace, and 
#     registers the session for cqlengine.
#     """
#     cluster = get_cluster()

#     try:
#         session = cluster.connect()
#         logger.info("Connected to Cassandra cluster.")
        
#         # Register the connection for cqlengine
#         register_connection("astra_connection", session=session)
#         set_default_connection("astra_connection")
#         logger.info("Cassandra session registered and default connection set.")
#     except Exception as e:
#         raise ConnectionError(f"❌ Error registering session for cqlengine: {e}")

#     return session


# def sync_all_tables():
#     """
#     Sync all tables with Cassandra after the connection is registered.
#     """
#     logger.info("Starting sync_all_tables()...")
#     from products.models import ProductsBaseModel
#     sync_table(ProductsBaseModel)
#     logger.info("sync_all_tables() completed.")


# import os
# import base64
# import tempfile
# import logging
# from decouple import config
# from cassandra.auth import PlainTextAuthProvider
# from cassandra.cluster import Cluster
# from cassandra.cqlengine.connection import register_connection, set_default_connection
# from cassandra.cqlengine.management import sync_table

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# handler = logging.StreamHandler()
# handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
# logger.addHandler(handler)

# # Load Astra credentials from environment
# ASTRA_BUNDLE_B64    = config("ASTRA_BUNDLE_B64")
# ASTRA_CLIENT_ID     = config("ASTRA_CLIENT_ID")
# ASTRA_CLIENT_SECRET = config("ASTRA_CLIENT_SECRET")
# ASTRA_KEYSPACE      = config("ASTRA_KEY_SPACE")

# # Write the bundle to a temp file
# SECURE_CONNECT_BUNDLE_PATH = None
# if ASTRA_BUNDLE_B64:
#     decoded = base64.b64decode(ASTRA_BUNDLE_B64)
#     temp_path = os.path.join(tempfile.gettempdir(), "secure_connect_bundle.zip")
#     with open(temp_path, "wb") as f:
#         f.write(decoded)
#     SECURE_CONNECT_BUNDLE_PATH = temp_path


# def get_cluster():
#     """Return a configured Cluster for Astra DB."""
#     if not all([SECURE_CONNECT_BUNDLE_PATH, ASTRA_CLIENT_ID, ASTRA_CLIENT_SECRET, ASTRA_KEYSPACE]):
#         raise ValueError("Missing ASTRA_BUNDLE_B64/ID/SECRET/KEYSPACE in env")
#     auth_provider = PlainTextAuthProvider(ASTRA_CLIENT_ID, ASTRA_CLIENT_SECRET)
#     cloud_config = {"secure_connect_bundle": SECURE_CONNECT_BUNDLE_PATH}
#     logger.info("▶ Connecting to Astra cluster…")
#     cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider, protocol_version=4)
#     logger.info("✅ Astra Cluster object created")
#     return cluster


# def get_session():
#     """Connect, set keyspace, and register cqlengine session."""
#     cluster = get_cluster()
#     session = cluster.connect()
#     logger.info(f"▶ Setting keyspace to '{ASTRA_KEYSPACE}'")
#     session.set_keyspace(ASTRA_KEYSPACE)
#     register_connection("astra_conn", session=session)
#     set_default_connection("astra_conn")
#     logger.info("✅ Cassandra session registered & default_connection set")
#     return session


# def sync_all_tables():
#     """Sync your Cassandra models to the keyspace tables."""
#     logger.info("▶ Syncing Cassandra tables…")
#     # Import here so Django has loaded settings
#     from products.models import ProductsBaseModel
#     sync_table(ProductsBaseModel)
#     logger.info("✅ sync_all_tables completed")


import os, base64, tempfile, logging
from decouple import config
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from cassandra.cqlengine.connection import register_connection, set_default_connection
from cassandra.cqlengine.management import sync_table

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(handler)

# Load credentials
ASTRA_BUNDLE_B64    = config("ASTRA_BUNDLE_B64")
ASTRA_CLIENT_ID     = config("ASTRA_CLIENT_ID")
ASTRA_CLIENT_SECRET = config("ASTRA_CLIENT_SECRET")
ASTRA_KEYSPACE      = config("ASTRA_KEY_SPACE")

# Decode bundle
bundle_path = os.path.join(tempfile.gettempdir(), "secure_connect_bundle.zip")
with open(bundle_path, "wb") as f:
    f.write(base64.b64decode(ASTRA_BUNDLE_B64))

def get_cluster():
    auth = PlainTextAuthProvider(ASTRA_CLIENT_ID, ASTRA_CLIENT_SECRET)
    cloud = {"secure_connect_bundle": bundle_path}
    logger.info("Connecting to Astra DB cluster…")
    return Cluster(cloud=cloud, auth_provider=auth, protocol_version=4)


def get_session():
    sess = get_cluster().connect()
    logger.info(f"Setting keyspace → {ASTRA_KEYSPACE}")
    sess.set_keyspace(ASTRA_KEYSPACE)
    register_connection("astra_conn", session=sess)
    set_default_connection("astra_conn")
    logger.info("Registered Astra session in cqlengine")
    return sess
# _global_session = None
# def get_session():
#     """
#     Returns a globally cached Cassandra session.
#     Registers it with cqlengine only once.
#     """
#     global _global_session
#     if _global_session is None:
#         cluster = get_cluster()
#         _global_session = cluster.connect()
#         _global_session.set_keyspace(ASTRA_KEYSPACE)
#         register_connection("astra_conn", session=_global_session)
#         set_default_connection("astra_conn")
#         logger.info("✅ Global Cassandra session established and registered.")
#     else:
#         logger.debug("🔁 Returning existing global Cassandra session.")
#     return _global_session

def sync_all_tables():
    from products.models import ProductsBaseModel, ScrapedProductDataModel
    logger.info("Syncing Cassandra tables…")
    sync_table(ProductsBaseModel)
    sync_table(ScrapedProductDataModel)
    logger.info("Cassandra tables synced")
