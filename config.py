import os
from telethon import TelegramClient

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')
bot_username = os.environ.get('BOT_USERNAME')
API_KEY = os.environ.get('API_KEY')
FOLDER_URL = "https://www.googleapis.com/drive/v2/files?q='[FOLDER_ID]'+in+parents&key="
FILE_URL = "https://www.googleapis.com/drive/v3/files/[FILE_ID]?alt=media&key="
BASE = "-1001361915166"
FFMPEG = "-1001514731412"
FFMPEGID = "2 3 4"
FFMPEGCMD = "5"
DESTINATION = "-1001463218112"

FFMPEGID = FFMPEGID.split()
for i in range(len(FFMPEGID)):
    FFMPEGID[i] = int(FFMPEGID[i])

BASE = int(BASE)
FFMPEG = int(FFMPEG)
FFMPEGCMD = int(FFMPEGCMD)
DESTINATION = int(DESTINATION)

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
