from telethon import events
from config import bot, API_KEY, FOLDER_URL, FILE_URL

import requests
import os
from downloader import DownLoadFile


@bot.on(events.NewMessage(pattern=(f"/start")))
async def start(event):
    await bot.send_message(event.chat_id, "Im Running")


@bot.on(events.NewMessage(pattern=f"/download"))
async def _(event):
    data = event.text.split(":")
    if "folder" in data[1]:
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
            file = await fast_upload(bot, f, reply)
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
        file = await fast_upload(bot, f, reply)
        await bot.send_message(event.chat_id, f, file=file, force_document= True)
        await reply.delete()
        os.remove(f)


bot.start()

bot.run_until_disconnected()
