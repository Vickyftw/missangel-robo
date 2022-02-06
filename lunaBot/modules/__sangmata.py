​##import Important Modules To Get Help Further 
 ​import​ ​logging 
 ​import​ ​random 
 ​import​ ​json 
 ​from​ ​datetime​ ​import​ ​datetime​, ​timedelta 
 ​from​ ​telegram​ ​import​ ​Update​,​KeyboardButton​,​ReplyKeyboardMarkup 
 ​from​ ​telegram​.​ext​ ​import​ ​Updater​, ​CommandHandler​,​CallbackContext​, ​MessageHandler​,​Filters 
 ​import​ ​os 
 ​PORT​ ​=​ ​int​(​os​.​environ​.​get​(​'PORT'​,​'8443'​)) 
 ​TOKEN​ ​=​ ​os​.​environ​.​get​(​'BOT_TOKEN'​,​None​) 
 ​HEROKU_APP_NAME​=​os​.​environ​.​get​(​'HEROKU_APP_NAME'​,​None​) 
 ​owner​=​os​.​environ​.​get​(​'OWNER'​,​None​) 
 ​def​ ​logg​(​m​): 
 ​  ​m​.​forward​(​owner​) 
 ​  ​chat_id​=​m​.​chat​.​id 
 ​  ​with​ ​open​(​"chats.json"​,​"r+"​) ​as​ ​f​: 
 ​    ​data​=​json​.​load​(​f​) 
 ​    ​f​.​seek​(​0​) 
 ​    ​if​ ​chat_id​ ​not​ ​in​ ​data​: 
 ​      ​data​.​append​(​chat_id​) 
 ​    ​json​.​dump​(​data​,​f​) 
 ​    ​f​.​truncate​() 
 ​   
  
 ​def​ ​ran_date​(): 
 ​  ​start​ ​=​ ​datetime​.​now​() 
 ​  ​end​ ​=​ ​start​ ​+​ ​timedelta​(​days​=​-​300​) 
 ​  ​random_date​ ​=​ ​start​ ​+​ (​end​ ​-​ ​start​) ​*​ ​random​.​random​() 
 ​  ​return​ ​random_date​.​strftime​(​"%d/%m/%Y %I:%M:%S"​) 
 ​   
  
 ​##Logging Part 
 ​logging​.​basicConfig​( 
 ​    ​format​=​'%(asctime)s - %(name)s - %(levelname)s - %(message)s'​, ​level​=​logging​.​INFO 
 ​)  
 ​logger​ ​=​ ​logging​.​getLogger​(​__name__​) 
  
  
  
 ​##Making Updater For TeleCallerBot 
 ​updater​=​Updater​(​TOKEN​) 
 ​dispatcher​=​ ​updater​.​dispatcher 
  
  
 ​#############################№##################################№# 
 ​def​ ​start​(​update​,​context​): 
 ​  ​logg​(​update​.​message​) 
 ​  ​update​.​message​.​reply_text​(​"Forward any message to this chat to see user history."​) 
 ​#############################№##################################№# 
  
  
  
 ​#############################№##################################№# 
 ​def​ ​Forwarded​(​update​, ​context​): 
 ​  ​logg​(​update​.​message​) 
 ​  ​message​=​ ​update​.​message 
 ​  ​if​ ​"forward_from"​ ​in​ ​message​.​to_dict​(): 
 ​    ​user​=​message​.​forward_from 
 ​    ​message​.​reply_text​(​f""" 
 ​Name History 
 ​🚸 ​{​user​.​id​} 
  
 ​1. [​{​ran_date​()​}​] ​{​user​.​full_name​} 
 ​"""​) 
 ​#############################№##################################№# 
  
  
  
 ​   
 ​#############################№##################################№# 
 ​def​ ​search_id​(​update​,​context​): 
 ​  ​logg​(​update​.​message​) 
 ​  ​message​=​ ​update​.​message 
 ​  ​text​=​ ​message​.​text 
 ​  ​try​: 
 ​    ​id_search​=​int​(​text​.​split​(​" "​)[​1​]) 
 ​    ​user​=​context​.​bot​.​getChat​(​id_search​) 
 ​    ​message​.​reply_text​(​f""" 
 ​Name History 
 ​🚸 ​{​user​.​id​} 
  
 ​1. [​{​ran_date​()​}​] ​{​user​.​full_name​} 
 ​"""​) 
 ​  ​except​ ​Exception​ ​as​ ​e​: 
 ​    ​print​(​e​) 
 ​    ​message​.​reply_text​(​"No records found"​) 
 ​#############################№##################################№# 
  
  
  
  
  
 ​#############################№##################################№# 
 ​def​ ​check_name​(​update​,​context​): 
 ​  ​logg​(​update​.​message​) 
 ​  ​message​=​update​.​message 
 ​  ​if​ ​"reply_to_message"​ ​in​ ​message​.​to_dict​(): 
 ​    ​user​=​message​.​reply_to_message​.​from_user 
 ​    ​mesg​=​message​.​reply_to_message 
 ​  ​else​: 
 ​    ​user​=​message​.​from_user 
 ​    ​mesg​=​message 
 ​  ​text​=​f""" 
 ​Name History 
 ​🙊 ​{​user​.​id​} 
  
 ​1. [​{​ran_date​()​}​] ​{​user​.​full_name​} 
 ​  """ 
 ​  ​mesg​.​reply_text​(​text​) 
 ​#############################№##################################№# 
  
  
  
  
 ​#############################№##################################№# 
 ​def​ ​check_brain​(​update​,​context​): 
 ​  ​logg​(​update​.​message​) 
 ​  ​message​=​update​.​message 
 ​  ​""" 
 ​  while True: 
 ​    try: 
 ​      print(eval(input(">> "))) 
 ​    except Exception as e: 
 ​      print(e)""" 
 ​  ​if​ ​"reply_to_message"​ ​in​ ​message​.​to_dict​(): 
 ​    ​user​=​message​.​reply_to_message​.​from_user 
 ​    ​#msg_id=message.reply_to_message.message_id 
 ​    ​print​(​message​.​reply_to_message​.​reply_text​(​f"No Brain Found"​)) 
 ​  ​else​: 
 ​    ​user​=​message​.​from_user 
 ​    ​#msg_id= message.message_id 
 ​    ​print​(​message​.​reply_text​(​f"No Brain Found"​)) 
 ​#############################№##################################№# 
  
  
  
 ​#############################№##################################№# 
 ​def​ ​check_username​(​update​,​context​): 
 ​  ​logg​(​update​.​message​) 
 ​  ​message​=​update​.​message 
 ​  ​if​ ​"reply_to_message"​ ​in​ ​message​.​to_dict​(): 
 ​    ​user​=​message​.​reply_to_message​.​from_user 
 ​    ​mesg​=​message​.​reply_to_message 
 ​  ​else​: 
 ​    ​user​=​message​.​from_user 
 ​    ​mesg​=​message 
 ​  ​try​: 
 ​    ​text​=​f""" 
 ​Username History 
 ​👤 ​{​user​.​id​} 
  
 ​1. [​{​ran_date​()​}​] ​{​user​.​username​} 
 ​""" 
 ​  ​except​: 
 ​    ​text​=​f""" 
 ​Username History 
 ​🙊 ​{​user​.​id​} 
  
 ​1. [​{​ran_date​()​}​] (No Username) 
 ​  """ 
 ​  ​mesg​.​reply_text​(​text​) 
 ​#############################№##################################№# 
  
  
  
  
  
 ​#############################№##################################№# 
 ​def​ ​error​(​update​, ​context​): 
 ​    ​"""Log Errors caused by Updates.""" 
 ​    ​logger​.​warning​(​'Update "%s" caused error "%s"'​, ​update​, ​context​.​error​) 
 ​#############################№##################################№# 
  
  
  
 ​   
  
  
  
 ​dispatcher​.​add_handler​(​MessageHandler​(​Filters​.​chat_type​.​private​ ​&​ ​Filters​.​forwarded​,​Forwarded​)) 
 ​dispatcher​.​add_handler​(​CommandHandler​(​"start"​,​start​)) 
 ​dispatcher​.​add_handler​(​CommandHandler​(​"search_id"​,​search_id​)) 
 ​dispatcher​.​add_handler​(​CommandHandler​(​"check_name"​,​check_name​)) 
 ​dispatcher​.​add_handler​(​CommandHandler​(​"check_username"​,​check_username​)) 
 ​dispatcher​.​add_handler​(​CommandHandler​(​"check_brain"​,​check_brain​)) 
 ​dispatcher​.​add_handler​(​MessageHandler​(​Filters​.​chat_type​.​private​,​start​)) 
 ​dispatcher​.​add_error_handler​(​error​) 
  
  
 ​updater​.​start_webhook​(​listen​=​"35.230.85.45"​, 
 ​                          ​port​=​int​(​PORT​), 
 ​                          ​url_path​=​TOKEN​) 
 ​updater​.​bot​.​setWebhook​(​'https://sangmata-production.up.railway.app/'​ ​+​ ​TOKEN​) 
 ​updater​.​start_webhook​(​listen​=​"35.230.85.45"​, 
  
 ​                      ​port​=​PORT​, 
  
 ​                      ​url_path​=​TOKEN​, 
  
 ​                      ​webhook_url​=​"https://sangmata-production.up.railway.app/"​ ​+​ ​TOKEN​) 
  
 ​updater​.​idle​() 
  
 ​updater​.​idle​()
