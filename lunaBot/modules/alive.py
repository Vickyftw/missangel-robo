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
  DEVU = f"โ๐๐ผ๐ถ๐ถ, ๐ ๐ฎ๐บ [โคออออโ๐ฒษชss๐งทโบ๐ฆษดษขแดส โ ใ๐ฎ๐ณใ](https://t.me/AngelxRobot)๐ฅ๐ผ๐ฏ๐ผ๐!!โ \n\n"
  DEVU += f"โ **๐'๐บ ๐ช๐ผ๐ฟ๐ธ๐ถ๐ป๐ด ๐ถ๐ป ๐ช๐ฒ๐น๐น ๐ ๐ฎ๐ป๐ป๐ฒ๐ฟ!!** \n\n"
  DEVU += f"โ **๐๐๐ถ ๐๐๐ถ ๐ ๐ ๐ ๐ฎ๐๐๐ฒ๐ฟ : [ใ๐ ๐ ๐ ๐ฎ๐๐๐ฒ๐ฟใ](https://t.me/ThomasShebLYY)** \n\n"
  DEVU += f"โ **๐ง๐ฒ๐น๐ฒ๐๐ต๐ผ๐ป ๐ฉ๐ฒ๐ฟ๐๐ถ๐ผ๐ป : {tlhver}** \n\n"
  DEVU += f"โ **๐ฃ๐๐ฟ๐ผ๐ด๐ฟ๐ฎ๐บ ๐ฉ๐ฒ๐ฟ๐๐ถ๐ผ๐ป : {pyrover}** \n\n"
  DEVU += "**โใ๐ง๐ต๐ฎ๐ป๐๐ ๐๐ผ๐ฟ ๐จ๐๐ถ๐ป๐ด ๐ ๐ฒ ๐๐๐ฟใโค๏ธโ**"
  BUTTON = [[Button.url("ใโแดส สแดแดแดโใ", "https://t.me/angelsupports")]]
  await tbot.send_file(event.chat_id, ALIBE_LOGO, caption=DEVU,  buttons=BUTTON)
#Alive command..!!
