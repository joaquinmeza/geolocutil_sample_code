import os
from dotenv import load_dotenv

load_dotenv()

# GEOLOC_API_KEY needs to be in the environmental variables.  You can use a .env file with GEOLOC_API_KEY='<myapikey>'
API_KEY = os.getenv("GEOLOC_API_KEY")

# SET CONNECTION TIMEOUT HERE #
# Connection timeout = time to attempt to connect before it times out
# Read timeout = time to attempt to read response before it times out
CONNECTION_TIMEOUT = 5
READ_TIMEOUT = 15

# OTHER GLOBAL SETTINGS DO NOT CHANGE
BASE_URL = "http://api.openweathermap.org/geo/1.0/"
ZIP_PATH = "zip"
DIRECT_PATH = "direct"
COUNTRY_CODE = "US"
