import telegram.ext


updater = telegram.ext.Updater("5523585310:AAHWeQbTTd4hKkI9V-xdEq7z7oly9VooaPw",use_context=True)
disp = updater.dispatcher
players=[]

def playersPrint() :
    count=1
    result=""
    for player in players :
        result=result+str(count)+"- "+str(player)+"\n"
        count += 1
    if len(result) :
        return result
    else :
        return "Mafeesh Tashkela !"

def is_admin(update,context):
    chat_id = str(update.message.chat.id)
    user_id = str(update.message.from_user.id)
    if str(updater.bot.get_chat_member(chat_id,user_id).status) == "creator" or str(updater.bot.get_chat_member(chat_id,user_id).status) == "administrator" :
        return True
    else:
        return False





def start(update,context):
    update.message.reply_text("HagzKoraBot is Operating !")

def restart(update,context):
    if is_admin(update,context):
        players.clear()
        update.message.reply_text("HagzKoraBot Restarted.")
    else:
        update.message.reply_text("Batal le3b ya hamada")

def help(update,context):
    update.message.reply_text("""Boso ya gd3an :
    1- /help ---> hywrek el kalam da
    2- /restart ---> lama n7gz match e3ml restart 3shan tms7 el tashkela el adema
    3- /gai ---> lw htl3b w hy7otak fel tashkela lw feh makan
    4- /mshgai ---> lw kont fel tashkela w 3ayz mtgesh
    5- /tashkela --> shoof el tashkela
    """)


def gai(update,context):
    member_name = update.message.from_user.full_name
    if len(players) <= 14 :
       if member_name in players :
            update.message.reply_text("Esmak fel tashkela aslan !")
       else :
           players.append(member_name)
           update.message.reply_text(playersPrint())
    else:

        update.message.reply_text("Mafesh Makan !")


def mshgai(update,context):
    member_name = update.message.from_user.full_name
    if len(players) <= 0 :
        update.message.reply_text("Mfesh tashkela !")
    elif member_name not in players :
        update.message.reply_text("Esmak msh fel tashkela aslan !")
    else:
        players.remove(member_name)
        update.message.reply_text(playersPrint())

def tashkela(update,context):
    update.message.reply_text(playersPrint())

disp.add_handler(telegram.ext.CommandHandler("start",start))
disp.add_handler(telegram.ext.CommandHandler("help",help))
disp.add_handler(telegram.ext.CommandHandler("gai",gai))
disp.add_handler(telegram.ext.CommandHandler("restart",restart))
disp.add_handler(telegram.ext.CommandHandler("mshgai",mshgai))
disp.add_handler(telegram.ext.CommandHandler("tashkela",tashkela))




updater.start_polling()
updater.idle()

