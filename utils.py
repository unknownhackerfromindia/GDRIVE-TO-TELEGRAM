
import asyncio
from FastTelethonhelper import fast_upload
from config import bot
import os

from config import DESTINATION

D = str(DESTINATION).replace("-100", "")

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        return f'[stdout]\n{stdout.decode()}'
    if stderr:
        return f'[stderr]\n{stderr.decode()}'

async def encode(chat, file, cmd):
    msg = await bot.send_message(chat, f"Encoding File: {file}")
    command = cmd.text.replace('[file]', file)
    c = await msg.reply(command)
    o = await run(f'{command}')
    x = await msg.reply(o[-2000:]) 
    res_file = await fast_upload(client = bot, file_location = f"./downloads/[AG] {file}", reply = msg)
    await msg.delete()
    os.remove(f"./downloads/{file}")
    os.remove(f"./downloads/[AG] {file}")
    try:
        y = await bot.send_message(DESTINATION,f"./downloads/[AG] {file}", file=res_file, force_document=True)
    except:
        y = await msg.reply(f"./downloads/[AG] {file}", file=res_file, force_document=True)
    await bot.send_message(chat, f"Encoding done....\n`./downloads/[AG] {file}`\nt.me/c/{D}/{y.id}")
    await asyncio.sleep(5)
    await x.delete()
    await c.delete()
