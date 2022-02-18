import os
import requests
import time
import libtorrent as lt
import time
import datetime
from config import bot
from FastTelethonhelper import fast_upload

class Timer:
    def __init__(self, time_between=5):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False

def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"

def progress_bar_str(done, total):
    percent = round(done/total*100, 2)
    strin = "░░░░░░░░░░"
    strin = list(strin)
    for i in range(round(percent)//10):
        strin[i] = "█"
    strin = "".join(strin)
    final = f"Percent: {percent}%\n{human_readable_size(done)}/{human_readable_size(total)}\n{strin}"
    return final

async def DownLoadFile(url, reply, chunk_size=1024*10, file_name="file.mkv"):
    if os.path.exists(file_name):
        os.remove(file_name)
    if not url:
        return file_name
    timer = Timer()

    r = requests.get(url, allow_redirects=True, stream=True)
    total_size = int(r.headers.get("content-length", 0))
    downloaded_size = 0
    with open(f"./downloads/{file_name}", 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                fd.write(chunk)
                downloaded_size += chunk_size
                if timer.can_send():
                    try:
                        data = progress_bar_str(downloaded_size, total_size)
                        await reply.edit(f"Downloading\n{data}")
                    except:
                        pass

    return file_name

async def download_torrent(link, event):
    ses = lt.session()
    ses.listen_on(6881, 6891)
    params = {
        'save_path': 'downloads',
        'storage_mode': lt.storage_mode_t(2)
    }

    handle = lt.add_magnet_uri(ses, link, params)
    ses.start_dht()

    begin = time.time()
    print(datetime.datetime.now())

    message = await bot.send_message(event.chat_id,"Downloading Metadata...")
    while (not handle.has_metadata()):
        time.sleep(1)
    await bot.edit_message(event.chat_id,message,"Got Metadata, Starting Torrent Download...")

    print("Starting", handle.name())
    await bot.edit_message(event.chat_id,message,f"Starting, {handle.name()}")
    while (handle.status().state != lt.torrent_status.seeding):
        s = handle.status()
        state_str = ['queued', 'checking', 'downloading metadata', \
                'downloading', 'finished', 'seeding', 'allocating']
        size_bytes = s.total_wanted
        size_mb = size_bytes/(1024*1024)
        size_gb = size_bytes/(1024*1024*1024)
        size = size_mb
        byte = "MB"
        if size_gb > 1:
            size = size_gb
            byte = "GB"
        await bot.edit_message(event.chat_id,message,"%s \n\nSize: %.2f %s\n\n %.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s " % \
        (handle.name(), size,byte, s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
        s.num_peers, state_str[s.state]))
        time.sleep(5)

    end = time.time()

    await bot.edit_message(event.chat_id,message,f"{handle.name()} COMPLETE")

    await bot.send_message(event.chat_id, f"Elapsed Time: {int((end-begin)//60)} min :{int((end-begin)%60)} sec")

    return handle.name()

async def upload_files(chat,file_list):
    file_list = sorted(file_list)
    for files in file_list:
        name = files.split('/')
        msg = await bot.send_message(chat, "Uploading...")
        file = await fast_upload(bot,files,reply=msg)
        await bot.send_message(chat, name[-1], file = file, force_document=True)
        await msg.delete()