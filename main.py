import telegram.ext
import os.path

updater = telegram.ext.Updater("5523585310:AAHWeQbTTd4hKkI9V-xdEq7z7oly9VooaPw",use_context=True)
disp = updater.dispatcher
players=[]

def updateFile() :
    file = open(os.path.join(os.path.dirname(__file__), 'Players.txt'),"w")
    str = ','.join(players)
    file.write(str)
    file.close()


def updatePlayers():
    f = open(os.path.join(os.path.dirname(__file__), 'Players.txt'), 'r')
    if f.mode=='r':
        contents= f.read()
        x=contents.split(",")
    for i in x :
        players.append(i)
    f.close()

def playersPrint() :
    count=1
    result=""
    for player in players :
        result=result+str(count)+"- "+str(player)+"\n"
        count += 1
    if len(result) :
        return result
    else :
        return "Mafeesh Tashkela"

def is_admin(update,context):
    chat_id = str(update.message.chat.id)
    user_id = str(update.message.from_user.id)
    if str(updater.bot.get_chat_member(chat_id,user_id).status) == "creator" or str(updater.bot.get_chat_member(chat_id,user_id).status) == "administrator" :
        return True
    else:
        return False





def start(update,context):
    players.clear()
    path=os.path.join(os.path.dirname(__file__))+"\Players.txt"
    file_exists=os.path.exists(path)
    if file_exists:
        updatePlayers()
    else:
        file = open(os.path.join(os.path.dirname(__file__), 'Players.txt'),"w")
        file.close()
    update.message.reply_text("HagzKoraBot is Operating")

def restart(update,context):
    if is_admin(update,context):
        players.clear()
        updateFile()
        update.message.reply_text("HagzKoraBot Restarted")
    else:
        update.message.reply_text("Admins Only")

def help(update,context):
    update.message.reply_text("""Boso ya gd3an :
    1- /help ---> hywrek el kalam da
    2- /restart ---> lama n7gz match e3ml restart 3shan tms7 el tashkela el adema
    3- /gai ---> lw htl3b w hy7otak fel tashkela lw feh makan
    4- /mshgai ---> lw kont fel tashkela w 3ayz mtgesh
    5- /tashkela --> shoof el tashkela
    6- /add name --> y7oot el asm fel tashkela
    7- /remove name --> yshel el asm mn el tashkela
    """)


def gai(update,context):
    member_name = update.message.from_user.full_name
    if len(players) <= 14 :
       if member_name in players :
            update.message.reply_text("Esmak fel tashkela aslan")
       else :
           players.append(member_name)
           updateFile()
           update.message.reply_text(playersPrint())
    else:

        update.message.reply_text("Mafesh Makan")


def mshgai(update,context):
    member_name = update.message.from_user.full_name
    if len(players) <= 0 :
        update.message.reply_text("Mfesh tashkela")
    elif member_name not in players :
        update.message.reply_text("Esmak msh fel tashkela aslan")
    else:
        players.remove(member_name)
        updateFile()
        update.message.reply_text(playersPrint())

def tashkela(update,context):
    update.message.reply_text(playersPrint())

def add(update,context):
    if is_admin(update,context):
        string=update.message.text[5:]
        if len(players) <= 14:
            if string in players:
                update.message.reply_text("Mwgod fel tashkela")
            else:
                players.append(string)
                updateFile()
                update.message.reply_text(playersPrint())
        else:
            update.message.reply_text("Mafesh Makan")
    else:
        update.message.reply_text("Admins Only")



def remove(update,context):
    if is_admin(update,context):
        string=update.message.text[8:]
        if len(players) <= 0 :
            update.message.reply_text("Mfesh tashkela")
        elif string not in players :
            update.message.reply_text("Msh fel tashkela aslan")
        else:
            players.remove(string)
            updateFile()
            update.message.reply_text(playersPrint())
    else:
        update.message.reply_text("Admins Only")


disp.add_handler(telegram.ext.CommandHandler("start",start))
disp.add_handler(telegram.ext.CommandHandler("help",help))
disp.add_handler(telegram.ext.CommandHandler("gai",gai))
disp.add_handler(telegram.ext.CommandHandler("restart",restart))
disp.add_handler(telegram.ext.CommandHandler("mshgai",mshgai))
disp.add_handler(telegram.ext.CommandHandler("tashkela",tashkela))
disp.add_handler(telegram.ext.CommandHandler("add",add))
disp.add_handler(telegram.ext.CommandHandler("remove",remove))

updater.start_webhook(listen="0.0.0.0",port=5000,url_path='main',webhook_url='https://hagzkorabot.herokuapp.com//main')
updater.idle()
