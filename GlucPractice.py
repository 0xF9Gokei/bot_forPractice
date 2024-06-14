import re
import paramiko
import psycopg2
import time
import os
from apiFunctions import *
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

TOKEN = '' #Token of bot
host = '' #ip of DB host
port = '' #port
username = ''
password = ''

id_val = ''
sur = ''

def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')

def session(update: Update, context):
    connection = None
    try:
        connection = psycopg2.connect(user="postgres",
                                    password="",
                                    host='',
                                    port='', 
                                    database='')

        cursor = connection.cursor()
        print("Connection begin")
        cursor.execute("SELECT * FROM Customers;")
        data = cursor.fetchall()
        for row in data:
            update.message.reply_text(row)  
        update.message.reply_text("Ошибок нет")
    except (Exception) as error:
        update.message.reply_text("Ошибка при работе с PostgreSQL")
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
            
def checkId(update: Update, context):
    connection = None
    try:
        connection = psycopg2.connect(user="postgres",
                                    password="",
                                    host='',
                                    port='', 
                                    database='')

        cursor = connection.cursor()
        print("Connection begin")
        cursor.execute("SELECT * FROM id;")
        data = cursor.fetchall()
        for row in data:
            update.message.reply_text(row)  
        update.message.reply_text("Ошибок нет")
    except (Exception) as error:
        update.message.reply_text("Ошибка при работе с PostgreSQL")
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

def helpCommand(update: Update, context):
    update.message.reply_text('Help!')


def User_InfoCommand(update: Update, context):
    update.message.reply_text("Введите id человека")
    return 'User_Info'

def User_Info(update: Update, context):
    global id_val
    global sur
    user_input = update.message.text
    id_val = user_input
    if user_input.isdigit() == True:
        user_info = getUserInfo(int(user_input))
    else:
        user_info = getUserInfo(user_input)
        
    sur = user_info['first_name'] + " " + user_info['last_name']
    update.message.reply_text(user_info['first_name'] + " " + user_info['last_name'])
    
    if 'mobile_phone' in user_info:
        update.message.reply_text("Мобильный телефон: " + user_info['mobile_phone'])
        
    if 'career' in user_info:
        answer = ''
        for i in user_info['career']:
            if 'name' in i:
                answer+= i['position'] + '; '
            if 'group_id' in i:
                answer+= "id группы: " + str(i['group_id']) + "; " 
        update.message.reply_text("Карьера: " + answer)
        
        
    if 'universities' in user_info:
        answer = ''
        for i in user_info['universities']:
            answer+= i['name']
        update.message.reply_text("Образование: " + answer)
        
    if 'about' in user_info:
        update.message.reply_text("Доп. инфа: " + user_info['about'])
        
    update.message.reply_text("Аккаунт закрыт от сообщений?: " + str(user_info['can_access_closed']))
    update.message.reply_text("Закрыта?: "  + str(user_info['is_closed']))
    update.message.reply_text("-----------------------------------------------------------------------------")
    update.message.reply_text("Записать человечка?..(yes/нет)")
    return 'Print'

def Print(update: Update, context):
    user_input = update.message.text
    if user_input == 'yes':
        update.message.reply_text("Okey")
        connection = None
        try:
            connection = psycopg2.connect(user="postgres",
                                        password="",
                                        host='',
                                        port='', 
                                        database='' )

            cursor = connection.cursor()
            print("Connection begin")
            print(id_val, sur)
            print(f"INSERT INTO id (Id, Name) VALUES ({id_val}, {sur});")
            cursor.execute(f"INSERT INTO id (Id, Name) VALUES ('{id_val}', '{sur}');")
            connection.commit()
            update.message.reply_text("Ошибок нет")
        except (Exception) as error:
            update.message.reply_text("Ошибка при работе c PostgreSQL")
        finally:
            if connection is not None:
                cursor.close()
                connection.close()        
    return ConversationHandler.END



def getFriendsCommand(update: Update, context):
    update.message.reply_text("Введитe id человека. Именно номер!")
    return 'getFriends'

def getFriends(update: Update, context):
    user_input = update.message.text
    user_info = getUserFriends(user_input)
    answer = ''
    for i in user_info:
        answer+=str(i['id']) + " " + i['first_name'] + " - " + i['last_name'] + "\n"
    update.message.reply_text(answer)
    return ConversationHandler.END



def getGroupsCommand(update: Update, context):
    update.message.reply_text("Введитe id человека. Именно номер!")
    return 'getGroups'

def getGroups(update: Update, context):
    user_input = update.message.text
    user_info = getGroup(user_input)
    answer = ''
    counter = 0
    for i in user_info:
        if counter == 70:
            break
        if 'name' in i:
            answer += i['name']
        answer += "\n"
        counter +=1
    update.message.reply_text(answer)
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    convHandlerUserInfo = ConversationHandler(
        entry_points=[CommandHandler('User_Info', User_InfoCommand)],
        states={
            'User_Info': [MessageHandler(Filters.text & ~Filters.command, User_Info)],
            'Print': [MessageHandler(Filters.text & ~Filters.command, Print)]
        },
        fallbacks=[]
    )
    
    convHandlergetUsers = ConversationHandler(
        entry_points=[CommandHandler('getFriends', getFriendsCommand)],
        states={
            'getFriends': [MessageHandler(Filters.text & ~Filters.command, getFriends)],
        },
        fallbacks=[]
    )
    
    convHandlergetGroups = ConversationHandler(
        entry_points=[CommandHandler('getGroups', getGroupsCommand)],
        states={
            'getGroups': [MessageHandler(Filters.text & ~Filters.command, getGroups)],
        },
        fallbacks=[]
    )
  
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("session", session))
    dp.add_handler(CommandHandler("checkId", checkId))
    dp.add_handler(convHandlerUserInfo)
    dp.add_handler(convHandlergetUsers)
    dp.add_handler(convHandlergetGroups)
    updater.start_polling()
    updater.idle()

main()
