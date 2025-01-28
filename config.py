from os import getenv

from dotenv import load_dotenv

load_dotenv()

API_ID = "22543203"
# -------------------------------------------------------------
API_HASH = "6b0baaf3002dd71f048cba92774b0c55"
# --------------------------------------------------------------
BOT_TOKEN = getenv("BOT_TOKEN", None)
STRING1 = getenv("STRING_SESSION", None)
MONGO_URL = getenv("MONGO_URL", None)
OWNER_ID = int(getenv("OWNER_ID", "7154410907"))
SUPPORT_GRP = "Poshtibaninetroplusbot"
UPDATE_CHNL = "me_nitroplus"
OWNER_USERNAME = "Owner_nitroplus"
