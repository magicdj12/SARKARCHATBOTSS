from os import getenv

from dotenv import load_dotenv

load_dotenv()

API_ID = "26082340"
# -------------------------------------------------------------
API_HASH = "3460353254f0e788b6685e51320a92f8"
# --------------------------------------------------------------
BOT_TOKEN = getenv("BOT_TOKEN", None)
STRING1 = getenv("STRING_SESSION", None)
MONGO_URL = getenv("MONGO_URL", None)
OWNER_ID = int(getenv("OWNER_ID", "6543211255"))
SUPPORT_GRP = "atrinmusic_tm1"
UPDATE_CHNL = "atrinmusic_tm"
OWNER_USERNAME = "beblnn"
