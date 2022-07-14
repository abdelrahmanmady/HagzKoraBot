from email.mime import application
import telegram.ext
import os.path
import psycopg2
TOKEN = "5523585310:AAHWeQbTTd4hKkI9V-xdEq7z7oly9VooaPw"
PORT = int(os.environ.get('PORT', '5000'))

updater = telegram.ext.Updater(TOKEN,use_context=True)
disp = updater.dispatcher
players=[]

def createFile(): #create table if does not exist
    conn=psycopg2.connect(
    database='dca46qdjuag8tu',
    user='dvdcmwpgmynxbq',
    password='7d4c7717eae7db357092eb2e47c174ad415891650e03cee28c57cd7efbf6e494',
    host='ec2-34-247-72-29.eu-west-1.compute.amazonaws.com',
    port='5432'
    )
    cursor=conn.cursor()
    sql='''SELECT EXISTS (
    SELECT FROM information_schema.tables 
    WHERE  table_schema = 'public'
    AND    table_name   = 'players'
    )'''
    cursor.execute(sql)
    exists=cursor.fetchone()[0]

    if not exists :
        sql2='create table players(name varchar(20) not null)'
        cursor.execute(sql2)
    conn.commit()
    conn.close()

def updateFile() : # Update table of players in the database 
    conn=psycopg2.connect(
    database='dca46qdjuag8tu',
    user='dvdcmwpgmynxbq',
    password='7d4c7717eae7db357092eb2e47c174ad415891650e03cee28c57cd7efbf6e494',
    host='ec2-34-247-72-29.eu-west-1.compute.amazonaws.com',
    port='5432'
    )
    cursor=conn.cursor()
    sql='TRUNCATE players' 
    cursor.execute(sql)

    for player in players:
        cursor.execute('''INSERT into players(name) VALUES ('{}')'''.format(player))
    conn.commit()
    conn.close()


def updatePlayers(): #update list from file
    conn=psycopg2.connect(
    database='dca46qdjuag8tu',
    user='dvdcmwpgmynxbq',
    password='7d4c7717eae7db357092eb2e47c174ad415891650e03cee28c57cd7efbf6e494',
    host='ec2-34-247-72-29.eu-west-1.compute.amazonaws.com',
    port='5432'
    )
    cursor=conn.cursor()

    sql = 'select * from players'
    cursor.execute(sql)
    for player in cursor.fetchall():
        str=''.join(player)
        if str not in players:
            players.append(str)
    conn.commit()
    conn.close()

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
    createFile()
    updatePlayers()
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
    updatePlayers()
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
    updatePlayers()
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
    updatePlayers()
    update.message.reply_text(playersPrint())

def add(update,context):
    updatePlayers()
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
    updatePlayers()
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

updater.start_webhook(listen="0.0.0.0",port=PORT,url_path=TOKEN,webhook_url='https://hagzkorabot.herokuapp.com/'+ TOKEN)
updater.idle()

