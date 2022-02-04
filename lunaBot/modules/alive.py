import re
import os

from telethon import events, Button
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from lunaBot.events import register as MEMEK
from lunaBot import telethn as tbot

RELOAD_LOGO = "https://telegra.ph/file/f7b0387db2dd5070e6eab.mp4"
ALIBE_LOGO = "https://telegra.ph/file/179825db677596b9f574d.mp4"

@MEMEK(pattern=("/alibe"))
async def awake(event):
  tai = event.sender.first_name
  DEVU = "**HoII!, I'm Devu Robot!** \n\n"
  DEVU += "🔴 **I'm Working Properly** \n\n"
  DEVU += "🔴 **My Master : [HYPER](https://t.me/HYPER_AD17)** \n\n"
  DEVU += f"🔴 **Telethon Version : {tlhver}** \n\n"
  DEVU += f"🔴 **Pyrogram Version : {pyrover}** \n\n"
  DEVU += "**Thanks For Adding Me Here ❤️**"
  BUTTON = [[Button.url("ʜᴇʟᴘ", "https://t.me/DEVU_ROBOT?start=help"), Button.url("sᴜᴘᴘᴏʀᴛ", "https://t.me/SCILENT_BOTS")]]
  await tbot.send_file(event.chat_id, ALIBE_LOGO, caption=DEVU,  buttons=BUTTON)

@MEMEK(pattern=("/reload"))
async def reload(event):
  tai = event.sender.first_name
  LUNA = "✅ **bot restarted successfully**\n\n• Admin list has been **updated**"
  BUTTON = [[Button.url("📡 ᴜᴘᴅᴀᴛᴇs", "https://t.me/SCILENT_BOTS")]]
  await tbot.send_file(event.chat_id, RELOAD_LOGO, caption=DEVU,  buttons=BUTTON)
