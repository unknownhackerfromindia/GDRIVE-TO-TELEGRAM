import os
from telethon import TelegramClient

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')
API_KEY = os.environ.get('API_KEY')
FOLDER_URL = "https://www.googleapis.com/drive/v2/files?q='[FOLDER_ID]'+in+parents&key="
FILE_URL = "https://www.googleapis.com/drive/v3/files/[FILE_ID]?alt=media&key="

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
