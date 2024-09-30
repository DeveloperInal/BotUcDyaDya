from dotenv import load_dotenv
from os import getenv

load_dotenv()

TOKEN = getenv('TOKEN')
HTTP_SERVER = getenv('HTTP_SERVER')
CHANNEL = {
    "tg_id:" "-1002214960127"
}
ADMINS = {
    "admins": {
        "1285554209",
        "1331366076",
    }
}