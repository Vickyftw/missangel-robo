import importlib
import time
import re
from sys import argv
from typing import Optional

from lunaBot import (
    ALLOW_EXCL,
    CERT_PATH,
    DONATION_LINK,
    LOGGER,
    OWNER_ID,
    PORT,
    SUPPORT_CHAT,
    TOKEN,
    URL,
    WEBHOOK,
    SUPPORT_CHAT,
    dispatcher,
    StartTime,
    telethn,
    pbot,
    updater,
)

# needed to dynamically load modules
# NOTE: Module order is not guaranteed, specify that in the config file!
from lunaBot.modules import ALL_MODULES
from lunaBot.modules.helper_funcs.chat_status import is_user_admin
from lunaBot.modules.helper_funcs.misc import paginate_modules
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

START_LOGO = "https://telegra.ph/file/aa138c012e3bf75c13628.mp4"

PM_START_TEXT = (f"""
𝗛𝗲𝘆![,](https://telegra.ph/file/f31af856c345e00513c36.mp4) 𝗜 𝗮𝗺 [ᴅᴇᴠᴜ ʀᴏʙᴏᴛ「⚜️」](https://t.me/DEVU_ROBOT),
️◁───ꔸꔸꔸꔸꔸꔸꔸꔸꔸꔸ❚❚ꔸꔸꔸꔸꔸꔸꔸꔸꔸꔸ───▷
`𝗜'𝗺 𝗩𝗲𝗿𝘆 𝗽𝗼𝘄𝗲𝗿𝗳𝘂𝗹𝗹 𝗠𝗮𝗻𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁 && 𝗧𝗿𝘂𝘀𝘁𝗲𝗱 𝗥𝗼𝗯𝗼𝘁 𝗪𝗶𝘁𝗵 𝗼𝘀𝗺 𝗺𝗼𝗱𝘂𝗹𝗲𝘀.♻️`
️●───────❚❚───────●
☉ **𝗖𝗹𝗶𝗰𝗸 /help or !help 𝗙𝗼𝗿 𝗠𝗼𝗿𝗲 𝗜𝗻𝗳𝗼.**
""")

buttons = [
    [
        InlineKeyboardButton(text="❄ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ.!! ❄", url="http://t.me/DEVU_ROBOT?startgroup=true"),
    ],
    [
        InlineKeyboardButton(text="❇️☆•ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ᴍᴇ•☆❇️", callback_data="luna_"),
    ],
]


HELP_STRINGS = """
**Main commands:**
❂ /start: `Starts me! You've probably already used this.`
"""

DONATE_STRING = """NHI CHAHIYE DONATION GO ANYWERE LOL!!🙋‍♂️,\n SHINING OFFFFF && HATERS FMK OFF🌚,"""


IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("lunaBot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


@run_async
def test(update: Update, context: CallbackContext):
    # pprint(eval(str(update)))
    # update.effective_message.reply_text("Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN)
    update.effective_message.reply_text("This person edited a message")
    print(update.effective_message)


@run_async
def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="help_back")]]
                    ),
                )

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            update.effective_message.reply_text(
                PM_START_TEXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
        update.effective_message.reply_video(
            START_LOGO, caption= "☆ɪ'ᴍ ᴀᴡᴀᴋᴇ ᴀʟʀᴇᴀᴅʏ!\n<b>☆ʜᴀᴠᴇɴ'ᴛ sʟᴇᴘᴛ sɪɴᴄᴇ:</b> <code>{}</code>\n\n☆".format(
                uptime
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(text="Sᴜᴘᴘᴏʀᴛ", url="https://t.me/SCILENCE_SUPPORT")]]
            ),
        )
        
def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors


@run_async
def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "Here is the help for the *{}* module:\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="help_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete()

    except BadRequest:
        pass


@run_async
def luna_about_callback(update, context):
    query = update.callback_query
    if query.data == "luna_":
        query.message.edit_text(
            text="""ʜɪ ᴀɢᴀɪɴ!\n\n ɪ'ᴀᴍ ᴀ ꜰᴜʟʟ-ꜰʟᴇᴅɢᴇᴅ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ ʙᴜɪʟᴛ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴇᴀsɪʟʏ.\n\n
                    \nɪ ᴄᴀɴ ᴅᴏ ʟᴏᴛ ᴏꜰ sᴛᴜꜰꜰ, sᴏᴍᴇ ᴏꜰ ᴛʜᴇᴍ ᴀʀᴇ:\n
                    \n• ʀᴇsᴛʀɪᴄᴛ ᴜsᴇʀs ᴡʜᴏ ꜰʟᴏᴏᴅ ʏᴏᴜʀ ᴄʜᴀᴛ ᴜsɪɴɢ ᴍʏ ᴀɴᴛɪ-ꜰʟᴏᴏᴅ ᴍᴏᴅᴜʟᴇ.\n
                    \n• sᴀꜰᴇɢᴜᴀʀᴅ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴡɪᴛʜ ᴛʜᴇ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɴᴅ ʜᴀɴᴅʏ ᴀɴᴛɪsᴘᴀᴍ sʏsᴛᴇᴍ.\n
                    \n• ɢʀᴇᴇᴛ ᴜsᴇʀs ᴡɪᴛʜ ᴍᴇᴅɪᴀ + ᴛᴇxᴛ ᴀɴᴅ ʙᴜᴛᴛᴏɴs, ᴡɪᴛʜ ᴘʀᴏᴘᴇʀ ꜰᴏʀᴍᴀᴛᴛɪɴɢ.\n
                    \n• sᴀᴠᴇ ɴᴏᴛᴇs ᴀɴᴅ ꜰɪʟᴛᴇʀs ᴡɪᴛʜ ᴘʀᴏᴘᴇʀ ꜰᴏʀᴍᴀᴛᴛɪɴɢ ᴀɴᴅ ʀᴇᴘʟʏ ᴍᴀʀᴋᴜᴘ.\n
                    \n• ɪ ᴀᴍ ꜰᴜʟʟ ᴛʀᴜsᴛᴇᴅ ʙᴏᴛ ᴡɪᴛʜ ᴛᴏᴜɢʜ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ᴏꜰ ʏᴏᴜʀ ʟᴏʙᴇʟʏ ɢʀᴏᴜᴘ.\n
                    \nɴᴏᴛᴇ: ɪ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴘʀᴏᴍᴏᴛᴇᴅ ᴡɪᴛʜ ᴘʀᴏᴘᴇʀ ᴀᴅᴍɪɴ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ꜰᴜᴄᴛɪᴏɴ ᴘʀᴏᴘᴇʀʟʏ.\n
                    \nᴄʜᴇᴄᴋ sᴇᴛᴜᴘ ɢᴜɪᴅᴇ ᴛᴏ ʟᴇᴀʀɴ ᴏɴ sᴇᴛᴛɪɴɢ ᴜᴘ ᴛʜᴇ ʙᴏᴛ ᴀɴᴅ ᴏɴ ʜᴇʟᴘ ᴛᴏ ʟᴇᴀʀɴ ᴍᴏʀᴇ!!\n""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="ᴜᴘᴅᴀᴛᴇ", url="https://t.me/SCILENT_BOT"
                        ),
                        InlineKeyboardButton(text="♻️ᴏᴡɴᴇʀ🤍", url="https://github.com/HYPER-AD17"),
                    ],
                    [
                        InlineKeyboardButton(text="💘ᴅᴇᴠᴜ ᴍᴜsɪᴄ💟", callback_data="luna_notes"),
                        InlineKeyboardButton(text="🧑‍💻ᴅᴇᴠs&ᴄᴏᴍᴍᴀɴᴅs🆘", callback_data="luna_basichelp"),
                    ],
                    [InlineKeyboardButton(text="ɢᴏ ʙᴀᴄᴋ", callback_data="luna_back")],
                ]
            ),
        )
    elif query.data == "luna_back":
        query.message.edit_text(
                PM_START_TEXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
                disable_web_page_preview=False,
        )

    elif query.data == "luna_basichelp":
        query.message.edit_text(
            text=f'''ᴜᴍᴍ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴇᴇ ᴍʏ ꜰᴀᴛʜᴇʀ && ᴍᴏᴛʜᴇʀ !! ʟᴏʟ. \n\nʜᴇʀᴇ ɪs ᴍʏ ᴅᴇᴠᴇʟᴏᴘᴇʀs ᴡʜᴏ ᴄʀᴇᴀᴛᴇᴅ ᴍᴇ \n\nꜰᴏʀ ᴍᴏʀᴇ ʜᴇʟᴘ ᴛᴀᴘ ᴏɴ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ʙᴇʟʟᴏ ʜᴇʀᴇ .!!''',
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="ᴅᴜᴅᴜ❤️", url="https://t.me/Itsme_Dream_AD_1713"),
                    InlineKeyboardButton(text="ʙᴜʙᴜ😌", url="https://t.me/HYPER_AD17"),
                 ],
                 [  
                    InlineKeyboardButton(text="🚸ʜᴇʟᴘ&ᴍᴏᴅᴜʟᴇ🚸", callback_data="help_back"),
                 ],
                 [
                    InlineKeyboardButton(text="ɢᴏ ʙᴀᴄᴋ", callback_data="luna_"),
                 ],
                ],
            ),
        )
    elif query.data == "luna_admin":
        query.message.edit_text(
            text=f"**──「 Basic Guide 」──\n**"
            f"\n┌───𝗕𝗔𝗦𝗜𝗖 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦𝄞🇮🇳\n"

            f"\n/play (song name/yt link/reply to audio file) :- 𝗣𝗹𝗮𝘆 𝗬𝗼𝘂𝗿 𝗚𝗶𝘃𝗲𝗻 𝗦𝗼𝗻𝗴 𝗜𝗻 𝘃𝗰!!\n"
            f"\n/song (song name/yt link) :- 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝘆𝗼𝘂𝗿 𝗴𝗶𝘃𝗲𝗻 𝗦𝗼𝗻𝗴 !!\n"
            f"\n/playlist :- 𝗦𝗲𝗲 𝗖𝘂𝗿𝗿𝗲𝗻𝘁 𝗣𝗹𝗮𝘆𝗟𝗶𝘀𝘁\n"
            f"\n/lyrics :- 𝗦𝗲𝗮𝗿𝗰𝗵 𝗟𝘆𝗿𝗶𝗰𝘀 𝗼𝗳 𝗮𝗻𝘆 𝘀𝗼𝗻𝗴\n"
            f"\n/blacklistedchat :- 𝗖𝗵𝗲𝗰𝗸 𝗪𝗲𝗮𝘁𝗵𝗲𝗿 𝗧𝗵𝗲 𝗖𝗵𝗮𝘁 𝗶𝘀 𝗯𝗹𝗮𝗰𝗸𝗹𝗶𝘀𝘁𝗲𝗱 𝗼𝗿 𝗻𝗼𝘁!!\n"
            f"\n/checkassistant :- 𝗖𝗵𝗲𝗮𝗸 𝗖𝘂𝗿𝗿𝗲𝗻𝘁 𝗽𝗹𝗮𝘆𝗶𝗻𝗴 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁!!\n",
            f"\n/alive - check bot is alive or not (fun cmd for user)",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Back", callback_data="luna_notes")]],
            ),
        )

    elif query.data == "luna_notes":
        query.message.edit_text(
            text=f"ʜᴇʏ!, ɪ ᴀᴍ ᴅᴇᴠᴜ ʀᴏʙᴏᴛ\n\nᴄᴏɴᴛᴀɪɴɪɴɢ ʜɪɢʜ ǫᴜᴀʟɪᴛʏ ᴏꜰ ᴍᴜsɪᴄ sʏsᴛᴇᴍ ᴀᴅᴅ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ᴀɴᴅ ᴇɴᴊᴏʏ ʟᴀɢ ꜰʀᴇᴇ  ᴍᴜsɪᴄ\n\nsᴇᴇ  ʜᴇʀᴇ ʙᴇʟᴏᴡ ᴀᴅᴍɪɴ ɴᴅ ᴜsᴇʀ ᴄᴏᴍᴍᴀɴᴅs\nᴛᴏ ᴜsᴇ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ..!!",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                  InlineKeyboardButton(text="💝ʙᴀsɪᴄ ᴄᴍᴅs💝", callback_data="luna_admin"),
                  InlineKeyboardButton(text="🔯ᴀᴅᴍɪɴ ᴄᴍᴅs🔯", callback_data="luna_support"),
                 ],
                 [
                  InlineKeyboardButton(text="💘sᴜᴅᴏ ᴄᴍᴅ🧑‍💻", callback_data="luna_credit"),
                  InlineKeyboardButton(text="🔥ᴏᴡɴᴇʀ ᴄᴍᴅs🤍", callback_data="luna_aselole"),
                 ],
                 [
                  InlineKeyboardButton(text="💘ᴍᴜsɪᴄ ᴀssɪsᴛᴀɴᴛ1🤍", url="https://t.me/DevuAssistant"),
                  InlineKeyboardButton(text="♻️ᴍᴜsɪᴄ ᴀssɪsᴛᴀɴᴛ2🤍", url="https://t.me/DevuAssistant2"),
                 ],
                [InlineKeyboardButton(text="Back", callback_data="luna_")]
                ],   
            ),
    elif query.data == "luna_support":
        query.message.edit_text(
            text=f"──「 Admin CMD 」──\n"
              f"\n┌───𝗔𝗗𝗠𝗜𝗡𝗦 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦𝄞🇮🇳\n"

            f"\n/pause :- 𝗣𝗮𝘂𝘀𝗲 𝘁𝗵𝗲 𝗖𝘂𝗿𝗿𝗲𝗻𝘁 𝗦𝗼𝗻𝗴!!\n"
            f"\n/resume :- 𝗥𝗲𝘀𝘂𝗺𝗲 𝘁𝗵𝗲 𝘀𝗼𝗻𝗴!!\n"
            f"\n/skip :- 𝗦𝗸𝗶𝗽 𝘁𝗼 𝗻𝗲𝘅𝘁 𝗦𝗼𝗻𝗴 𝗶𝗻 𝗾𝘂𝗲𝘂𝗲!!\n"
            f"\n/end or /stop :- 𝗘𝗻𝗱 𝘄𝗵𝗼𝗹𝗲 𝗽𝗹𝗮𝘆𝗹𝗶𝘀𝘁!!\n"
            f"\n/queue :- 𝗦𝗲𝗲 𝗾𝘂𝗲𝘂𝗲 𝗦𝗼𝗻𝗴𝘀!!\n"
            f"\n/auth (username/reply to user) :- 𝗔𝘂𝘁𝗵 𝗻𝗼𝗻-𝗮𝗱𝗺𝗶𝗻 𝘂𝘀𝗲𝗿 𝘁𝗼 𝘀𝗸𝗶𝗽/𝗽𝗮𝘂𝘀𝗲/𝗲𝗻𝗱 𝗰𝗺𝗱𝘀!!\n"
            f"\n/unauth :- 𝗥𝗲𝗺𝗼𝘃𝗲 𝗮𝘂𝘁𝗵 𝗳𝗿𝗼𝗺 𝘂𝘀𝗲𝗿!\n"
            f"\n/authusers :- 𝗦𝗲𝗲 𝗮𝘂𝘁𝗵 𝗹𝗶𝘀𝘁 𝗶𝗻 𝘁𝗵𝗲 𝗰𝗵𝗮𝘁!!\n",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                   InlineKeyboardButton(text="Back", callback_data="luna_notes"),
                 
                 ]
                ]
            ),
        )
    elif query.data == "luna_credit":
        query.message.edit_text(
            text=f"──「 `Sudo CMD` 」──\n"
            f"\n ┌───𝗦𝗨𝗗𝗢𝗦 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦𝄞🇮🇳\n"

            f"\n/blacklistchat (chat id) :- 𝗕𝗹𝗮𝗰𝗸𝗹𝗶𝘀𝘁 𝗮𝗻𝘆 𝗰𝗵𝗮𝘁𝘀!!\n"
            f"\n/whitelistchat (chat id) :- 𝗪𝗵𝗶𝘁𝗲𝗹𝗶𝘀𝘁 𝗮𝗻𝘆 𝗯𝗹𝗮𝗰𝗸𝗹𝗶𝘀𝘁𝗲𝗱 𝗰𝗵𝗮𝘁!!\n"
            f"\n/broadcast (Message/reply to message) :- 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗺𝗲𝘀𝘀𝗮𝗴𝗲!!\n"
            f"\n/broadcast_pin (Message/reply to message) :- 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗺𝗲𝘀𝘀𝗮𝗴𝗲!!\n"
            f"\n/broadcast_pin_loud (Message/reply to message) :- 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗺𝗲𝘀𝘀𝗮𝗴𝗲!!\n"
            f"\n/joinassistant (chat id/username) :- 𝗔𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝘁 𝗝𝗼𝗶𝗻𝗲𝗱 𝘁𝗼 𝗧𝗵𝗲 𝗖𝗵𝗮𝘁!!\n"
            f"\n/leaveassistant (chat id/username) :- 𝗟𝗲𝗮𝘃𝗲 𝗮𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝘁 𝗳𝗿𝗼𝗺 𝘁𝗵𝗮𝘁 𝗰𝗵𝗮𝘁!\n"
            f"\n/changeassistant (assistant number) :- 𝗖𝗵𝗮𝗻𝗴𝗲 𝗮𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝘁 !!\n"
            f"\n/setassistant (assistant no./random) :- 𝗦𝗲𝘁 𝗮𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝘁!\n"
            f"\n/activevc :- 𝗖𝗵𝗲𝗰𝗸 𝘄𝗲𝗮𝘁𝗵𝗲𝗿 𝘃𝗰 𝗶𝘀 𝗼𝗻 𝗼𝗿 𝗻𝗼𝘁!!\n",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="ɢᴏ ʙᴀᴄᴋ", callback_data="luna_notes"),
                 ]
                ]
            ),
        )
        
    elif query.data == "luna_aselole":
        query.message.edit_text(
            text=f"──「 Admin CMD 」──\n"
                 f"\n┌───𝗢𝗪𝗡𝗘𝗥 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦𝄞🇮🇳\n"

                 f"\n/leavebot (chat id/username) :- 𝗣𝗹𝗮𝘆 𝗬𝗼𝘂𝗿 𝗚𝗶𝘃𝗲𝗻 𝗦𝗼𝗻𝗴 𝗜𝗻 𝘃𝗰!!\n"
                 f"\n/addsudo (username/user id) :- 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝘆𝗼𝘂𝗿 𝗴𝗶𝘃𝗲𝗻 𝗦𝗼𝗻𝗴 !!\n"
                 f"\n/delsudo (username/user id) :- 𝗦𝗲𝗲 𝗖𝘂𝗿𝗿𝗲𝗻𝘁 𝗣𝗹𝗮𝘆𝗟𝗶𝘀𝘁\n"
                 f"\n/restart :- 𝗦𝗲𝗮𝗿𝗰𝗵 𝗟𝘆𝗿𝗶𝗰𝘀 𝗼𝗳 𝗮𝗻𝘆 𝘀𝗼𝗻𝗴\n"
                 f"\n/maintenance (enable/disable) :- 𝗖𝗵𝗲𝗰𝗸 𝗪𝗲𝗮𝘁𝗵𝗲𝗿 𝗧𝗵𝗲 𝗖𝗵𝗮𝘁 𝗶𝘀 𝗯𝗹𝗮𝗰𝗸𝗹𝗶𝘀𝘁𝗲𝗱 𝗼𝗿 𝗻𝗼𝘁!!\n"
                 f"\n/update :- 𝗖𝗵𝗲𝗮𝗸 𝗖𝘂𝗿𝗿𝗲𝗻𝘁 𝗽𝗹𝗮𝘆𝗶𝗻𝗴 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁!!\n"
                 f"\n/clean :-  𝗦𝗲𝗲 𝗦𝘂𝗱𝗼 𝗟𝗶𝘀𝘁 𝗼𝗳 𝘁𝗵𝗲 𝗯𝗼𝘁!!\n",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="Back", callback_data="luna_notes"),
                 
                 ]
                ]
            ),
        )

    elif query.data == "luna_asu":
        query.message.edit_text(
            text=f"｢ Admin Permissions 」\n"
                     f"\nTo avoid slowing down, Devu caches admin rights for each user. This cache lasts about 10 minutes; this may change in the future. This means that if you promote a user manually (without using the /promote command), Luna will only find out ~10 minutes later.\n"
                    f"\nIf you want to update them immediately, you can use the /admincache or /reload command, that'll force Luna to check who the admins are again and their permissions\n"
                    f"\nIf you are getting a message saying:\nYou must be this chat administrator to perform this action!\n"
                    f"\nThis has nothing to do with Devu's rights; this is all about YOUR permissions as an admin. Devu respects admin permissions; if you do not have the Ban Users permission as a telegram admin, you won't be able to ban users with Luna. Similarly, to change Devu settings, you need to have the Change group info permission.\n"
                    f"\nThe message very clearly states that you need these rights - not Devu.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [InlineKeyboardButton(text="Back", callback_data="luna_aselole")]
            ),
        )

    elif query.data == "luna_asi":
        query.message.edit_text(
            text=f"｢ Anti-Spam Settings 」\n"
                     f"\nAntispam: "
                     f"\nBy enabling this, you can protect your groups free from scammers/spammers.\nRun /antispam on in your chat to enable.\nAppeal Chat: @ZZZZZ\n"
                     f"\n✪ Anti-Flood allows you to keep your chat clean from flooding."
                     f"\n✪ With the help of Blaclists you can blacklist words,sentences and stickers which you don't want to be used by group members."
                     f"\n✪ By enabling Reports, admins get notified when users reports in chat."
                     f"\n✪ Locks allows you to lock/restrict some comman items in telegram world."
                     f"\n✪ Warnings allows to warn users and set auto-warns. "
                     f"\n✪ Welcome Mute helps you prevent spambots or users flooding/spamming your group. Checl Greetings for more info",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Back", callback_data="luna_aselole")]]
            ),
        )

    elif query.data == "luna_puqi":
        query.message.edit_text(
            text=f" ｢ Terms and Conditions 」\n"
                f"\nTo use this bot, You need to agree with Terms and Conditions.\n"
                f"\n✪ If someone is spamming your group, you can use report feature from your Telegram Client."
                f"\n✪ Make sure antiflood is enabled, so that users cannot flood/spam your chat."
                f"\n✪ Do not spam commands, buttons, or anything in bot PM, else you will be Ignored by bot or Gbanned."
                f"\n✪ If you need to ask anything about this bot or you need help, reach us at @ZZZZZZ"
                f"\n✪ Make sure you read rules and follow them when you join Support Chat."
                f"\n✪ Spamming in Support Chat, will reward you GBAN and reported to Telegram as well.\n"
                f"\nTerms & Conditions can be changed anytime.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                  [
                     InlineKeyboardButton(text="Credits", callback_data="luna_angjay"),
                     InlineKeyboardButton(text="Back", callback_data="luna_"),
                  ]
                ]
            ),
        )

    elif query.data == "luna_angjay":
        query.message.edit_text(
            text=f"Luna is a powerful bot for managing groups with additional features.\n"
              f"\nLuna's Licensed Under The GNU (General Public License v3.0)\n"
              f"\nIf you have any question about Luna,"
              f"\nreach us at Support Chat.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                  [
                     InlineKeyboardButton(text="Back", callback_data="luna_puqi"),
                     InlineKeyboardButton(text="☎️ Support", url=f"https://t.me/ZZZZZZ"),
                  ]
                ]
            ),
        )   

@run_async
def Source_about_callback(update, context):
    query = update.callback_query
    if query.data == "source_":
        query.message.edit_text(
            text=""" Hi.. ɪ'ᴀᴍ Lᴜɴᴀ*
                 \nHere is the [sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ](https://t.me/THN_NETWORK) .""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="Back", callback_data="source_back")
                 ]
                ]
            ),
        )
    elif query.data == "source_back":
        query.message.edit_text(
                PM_START_TEXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
                disable_web_page_preview=False,
        )

@run_async
def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_text(
                f"Contact me in PM to get help of {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Help",
                                url="t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_text(
            "Contact me in PM to get the list of possible commands.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Hᴇʟᴘ ❔",
                            url="t.me/{}?start=help".format(context.bot.username),
                        )
                    ],
                    [
                        InlineKeyboardButton(text="💝ᴅᴇᴠᴜ ᴍᴜsɪᴄ ᴄᴍᴅs💝", url="https://telegra.ph/%E1%B4%85%E1%B4%87%E1%B4%A0%E1%B4%9CMusic-02-11"),
                    ],
                ],
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Here is the available help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="help_back")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Sepertinya tidak ada pengaturan khusus pengguna yang tersedia :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="Which module would you like to check {}'s settings for?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any chat settings available :'(\nSend this "
                "in a group chat you're admin in to find its current settings!",
                parse_mode=ParseMode.MARKDOWN,
            )


@run_async
def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Back",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                text="Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "Message is not modified",
            "Query_id_invalid",
            "Message can't be deleted",
        ]:
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))


@run_async
def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "Click here to get this chat's settings, as well as yours."
            msg.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Settings",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "Click here to check your settings."

    else:
        send_settings(chat.id, user.id, True)


@run_async
def donate(update: Update, context: CallbackContext):
    user = update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]
    bot = context.bot
    if chat.type == "private":
        update.effective_message.reply_text(
             DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )

        if OWNER_ID != 1996039846 and DONATION_LINK:
            update.effective_message.reply_text(
                "You can also donate to the person currently running me "
                "[here]({})".format(DONATION_LINK),
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        try:
            bot.send_message(
                user.id,
                DONATE_STRING,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )

            update.effective_message.reply_text(
                "I've PM'ed you about donating to my creator!"
            )
        except Unauthorized:
            update.effective_message.reply_text(
                "Contact me in PM first to get donation information."
            )


def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop


def main():

    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.sendMessage(f"@{SUPPORT_CHAT}", "ᴏᴍғᴏ ɪ, ᴀᴍ ᴀʟɪᴠᴇ sɪʀ 🔥!!")
        except Unauthorized:
            LOGGER.warning(
                "Bot isnt able to send message to support_chat, go and check!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)

    test_handler = CommandHandler("test", test)
    start_handler = CommandHandler("start", start)

    help_handler = CommandHandler("help", get_help)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_.*")

    settings_handler = CommandHandler("settings", get_settings)
    settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_")

    about_callback_handler = CallbackQueryHandler(luna_about_callback, pattern=r"luna_")
    source_callback_handler = CallbackQueryHandler(Source_about_callback, pattern=r"source_")

    donate_handler = CommandHandler("donate", donate)
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)

    # dispatcher.add_handler(test_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(source_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(donate_handler)

    dispatcher.add_error_handler(error_callback)

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN, certificate=open(CERT_PATH, "rb"))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4, clean=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    pbot.start()
    main()
