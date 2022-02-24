import re
import os

from telethon import events, Button
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from lunaBot.events import register as MEMEK
from lunaBot import telethn as tbot

ALIBE_LOGO = "https://telegra.ph/file/bb00b82ee06f37ff23e0d.mp4"

@MEMEK(pattern=("/alive"))
async def awake(event):
  tai = event.sender.first_name
  DEVU = f"❄𝗛𝗼𝗶𝗶, 𝗜 𝗮𝗺 [⏤͟͟͞͞★🇲ɪss𖧷➺🇦ɴɢᴇʟ ✘ 「🇮🇳」](https://t.me/Errorprobot)𝗥𝗼𝗯𝗼𝘁!!❄ \n\n"
  DEVU += f"✘ **𝗜'𝗺 𝗪𝗼𝗿𝗸𝗶𝗻𝗴 𝗶𝗻 𝗪𝗲𝗹𝗹 𝗠𝗮𝗻𝗻𝗲𝗿!!** \n\n"
  DEVU += f"✘ **𝗛𝘂𝗶 𝗛𝘂𝗶 𝗠𝘆 𝗠𝗮𝘀𝘁𝗲𝗿 : [「𝗠𝘆 𝗠𝗮𝘀𝘁𝗲𝗿」](https://t.me/ThomasShebLYY)** \n\n"
  DEVU += f"✘ **𝗧𝗲𝗹𝗲𝘁𝗵𝗼𝗻 𝗩𝗲𝗿𝘀𝗶𝗼𝗻 : {tlhver}** \n\n"
  DEVU += f"✘ **𝗣𝘆𝗿𝗼𝗴𝗿𝗮𝗺 𝗩𝗲𝗿𝘀𝗶𝗼𝗻 : {pyrover}** \n\n"
  DEVU += "**❄「𝗧𝗵𝗮𝗻𝘅𝘅 𝗙𝗼𝗿 𝗨𝘀𝗶𝗻𝗴 𝗠𝗲 𝘀𝘂𝗿」❤️❄**"
  BUTTON = [[Button.url("「☆ᴍʏ ʜᴏᴍᴇ☆」", "https://t.me/angelsupports")]]
  await tbot.send_file(event.chat_id, ALIBE_LOGO, caption=DEVU,  buttons=BUTTON)
#Alive command..!!
