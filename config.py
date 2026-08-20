import os

from dotenv import load_dotenv


load_dotenv()


SALESFORCE_CLIENT_ID = os.getenv(
    "SALESFORCE_CLIENT_ID"
)

SALESFORCE_CLIENT_SECRET = os.getenv(
    "SALESFORCE_CLIENT_SECRET"
)

SALESFORCE_INSTANCE_URL = os.getenv(
    "SALESFORCE_INSTANCE_URL"
)

SALESFORCE_API_VERSION = os.getenv(
    "SALESFORCE_API_VERSION",
    "v66.0"
)
