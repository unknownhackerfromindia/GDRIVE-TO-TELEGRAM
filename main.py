from telethon import events
from config import bot, API_KEY, FOLDER_URL, FILE_URL, BASE, FFMPEG, FFMPEGCMD, FFMPEGID, bot_username
from FastTelethonhelper import fast_upload, fast_download
import requests
import os
from downloader import DownLoadFile, download_torrent, upload_files
import asyncio
import subprocess
from utils import encode, delete_files

loop = asyncio.get_event_loop()

async def dl_ffmpeg():
    global Locked
    message = "Starting up..."
    a = await bot.send_message(BASE, "Starting up...")
    r = await bot.send_message(BASE, "Downloading ffmpeg files now.....")
    msgs = await bot.get_messages(FFMPEG, ids=FFMPEGID)
    cmd = await bot.get_messages(FFMPEG, ids=FFMPEGCMD)
    for msg in msgs:
        s = await fast_download(bot, msg, r, "")
        subprocess.call(f"chmod 777 ./{s}", shell=True)
        message = f"{message}\n{s} Downloaded" 
        await a.edit(message)     
    await r.edit(f"FFMPEG download complete, and the active command is: \n\n`{cmd.text}`")
    Locked = False

@bot.on(events.NewMessage(pattern=(f"/start")))
async def start(event):
    if event.text == '/start' or event.text == f'/start{bot_username}':
        await bot.send_message(event.chat_id, "Im Running")

@bot.on(events.NewMessage(pattern=f"/ls{bot_username}"))
async def _(event):
    p = subprocess.Popen(f'ls -lh downloads', stdout=subprocess.PIPE, shell=True)
    x = await event.reply(p.communicate()[0].decode("utf-8", "replace").strip())
    await asyncio.sleep(15)
    await x.delete()

@bot.on(events.NewMessage(pattern=f"/encode{bot_username}"))
async def _(event):
    cmd = await bot.get_messages(FFMPEG, ids=FFMPEGCMD)
    data = event.text.split(":")

    if "magnet" in data[1] or "torrent" in data[1]:
        r = await event.reply("Downloading...")
        f = await download_torrent(data[1], r)
        file = await fast_upload(bot, f"./downloads/{f}", r)
        await bot.send_message(event.chat_id, f, file=file, force_document= True)
        await r.delete()
        os.remove(f"./downloads/{f}")
        for root, subdirectories, files in os.walk('./downloads'):
            for file in files:
               f = os.path.join(root, file)
               await encode(event.chat_id, f, cmd)

    elif "folder" in data[1]:
        folder_id = data[1].split("/")[-1]
        url = FOLDER_URL
        url = url.replace("[FOLDER_ID]", folder_id)
        r = requests.get(f"{url}{API_KEY}")
        j = r.json()
        main = await event.reply("STATUS:")
        items = j['items'][::-1]
        for i in items:
            name = i['title']
            file_id = i['id']
            url = FILE_URL
            url = url.replace("[FILE_ID]", file_id)
            url = f"{url}{API_KEY}"
            reply = await event.reply("Downloading...")
            await main.edit(f"STATUS:\n`Downloading {name}`")
            f = await DownLoadFile(url, reply, file_name=name)
            await reply.delete()
            await encode(event.chat_id, f, cmd)
        await main.edit("ALL FILES UPLOADED")

    elif "file" in data[1]:
        file_id = data[1].split("/")[-1]
        url = FILE_URL
        url = url.replace("[FILE_ID]", file_id)
        url = f"{url}{API_KEY}"
        info_url = FILE_URL
        info_url = info_url.replace("[FILE_ID]", file_id)
        info_url = info_url.replace("alt=media&", "")
        r = requests.get(f"{info_url}{API_KEY}")
        j = r.json()
        name = j['name']
        
        reply = await event.reply("Downloading...")
        f = await DownLoadFile(url, reply, file_name=name)
        await reply.delete()
        await encode(event.chat_id, f, cmd)

@bot.on(events.NewMessage(pattern=f"/download{bot_username}"))
async def _(event):
    data = event.text.split(":")
    if "magnet" in data[1] or "torrent" in data[1]:
        r = await event.reply("Downloading...")
        f = await download_torrent(data[1], r)
        file = await fast_upload(bot, f"./downloads/{f}", r)
        await bot.send_message(event.chat_id, f, file=file, force_document= True)
        await r.delete()
        os.remove(f"./downloads/{f}")
        file_list = []  
        for root, subdirectories, files in os.walk('./downloads'):
            for file in files:
                file_list.append(os.path.join(root, file))
        await upload_files(event,file_list)
        delete_files('downloads')

    elif "folder" in data[1]:
        folder_id = data[1].split("/")[-1]
        url = FOLDER_URL
        url = url.replace("[FOLDER_ID]", folder_id)
        r = requests.get(f"{url}{API_KEY}")
        j = r.json()
        main = await event.reply("STATUS:")
        items = j['items'][::-1]
        for i in items:
            name = i['title']
            file_id = i['id']
            url = FILE_URL
            url = url.replace("[FILE_ID]", file_id)
            url = f"{url}{API_KEY}"
            reply = await event.reply("Downloading...")
            await main.edit(f"STATUS:\n`Downloading {name}`")
            f = await DownLoadFile(url, reply, file_name=name)
            await main.edit(f"STATUS:\n`Uploading {name}`")
            file = await fast_upload(bot, f"./downloads/{f}", reply)
            await bot.send_message(event.chat_id, f, file=file, force_document= True)
            await reply.delete()
            os.remove(f)
        await main.edit("ALL FILES UPLOADED")

    elif "file" in data[1]:
        file_id = data[1].split("/")[-1]
        url = FILE_URL
        url = url.replace("[FILE_ID]", file_id)
        url = f"{url}{API_KEY}"
        info_url = FILE_URL
        info_url = info_url.replace("[FILE_ID]", file_id)
        info_url = info_url.replace("alt=media&", "")
        r = requests.get(f"{info_url}{API_KEY}")
        j = r.json()
        name = j['name']
        
        reply = await event.reply("Downloading...")
        f = await DownLoadFile(url, reply, file_name=name)
        file = await fast_upload(bot, f"./downloads/{f}", reply)
        await bot.send_message(event.chat_id, f, file=file, force_document= True)
        await reply.delete()
        os.remove(f"./downloads/{f}")

loop.run_until_complete(dl_ffmpeg())

bot.start()

bot.run_until_disconnected()
