import json
import sqlite3
import threading as thr
import telebot
import datetime
from telebot import types

class Date:
    def __init__(self, date):
        date = date.split(' ')
        date = date[0].split('-')
        self.day = date[2]
        self.month = date[1]
        self.year = date[0]
        
class User:
    def __init__(self, id, name, surname, username, is_subscribed = False, is_admin = False, last_message = '/start', last_check = datetime.datetime.now()):
        self.id = id
        self.name = name
        self.surname = surname
        self.username = username
        self.is_subscribed = is_subscribed
        self.is_admin = is_admin
        self.last_message = last_message
        self.last_check = last_check

    def subscribe(self):
        phr = "UPDATE users SET Is_subscribed=1 WHERE Id=" + str(user.id)
        cursor.execute(phr)
        
    def unsubscribe(self):
        phr = "UPDATE users SET Is_subscribed=0 WHERE Id=" + str(user.id)
        cursor.execute(phr)
        
global users, thrs, conn, cursor

def start():
    for thread in thrs:
        thread.start()

#Send schedule
def timer(bot):
    time = datetime.datetime.now().strftime("%H:%M:%S")
    
    if time.split(':')[0]>=17 and time.split(':')[0]<=22:
        for user in users:
            bot.send_document(user.userId, open('NAME_OF_FILE', 'rb'))
            
#It doesn't work yet            
#timerThr = thr.Thread(target=timer, args=bot)
#thrs.append(timerThr)

#Getting list of users
def users():
    users = []
    all = cursor.fetchall()
    for i in range (len(all)):
        id = int(all[i][0])
        name = all[i][1]
        surname = all[i][2]
        username = all[i][3]
        is_subscribed = str(bool(all[i][4]))
        is_admin = str(bool(all[i][5]))
        last_message = all[i][6]
        last_check = all[i][7]
        reg(id, name, surname, username, is_subscribed, is_admin, last_message, last_check)
                     
    return users

#Add users in users
def reg(id, name, surname, username, is_subscribed, is_admin, last_message, last_check):
    users.append(User(id, name, surname, username, is_subscribed, is_admin, last_message, last_check))

#Save users in users.py
def save_data():
    cursor.execute("DELETE FROM users;")
    conn.commit()
    for user in users:
        phr = "INSERT INTO users VALUES (" + user.id + ", '" + user.name + "', '" + user.surname + "', " + user.is_subscribed + ", " + user.is_admin + ", '" + user.last_message + "', '" + user.last_check + "');"
        cursor.execute(phr)

        
#Check if users exists in users
def isInUsers(id, name, surname, username, is_admin, last_message, last_check):
    for user in users:
        if user.id == id:
            user.name = name
            user.surname = surname
            user.username = username
            user.last_message = last_message
            user.last_check = last_check
            save_data()
            return True
            break
    return False

#Reg users if he is not in users
def check(id, name, surname, username, is_admin, last_message, last_check):
    if not isInUsers(id, name, surname, username, is_admin, last_message, last_check):
        reg(id, name, surname, username, is_admin, last_message, last_check)
        save_data()

#Find user in users
def findUserid):
    for i in range(len(users)):
        if users[i].id == id:
            return i
            break
    

token = ''
bot = telebot.TeleBot(token)

users = users()
conn = sqlite3.connect('bot.sqlite')
cursor = conn.cursor()

@bot.message_handler(commands=['start'])
def start(msg):
    check(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.username, False, False, msg.text, datetime.datetime.now())
    
    if msg.from_user.username != 'None':
        bot.send_message(msg.chat.id, f'Приветствую Вас, {msg.from_user.first_name} {msg.from_user.last_name}(@{msg.from_user.username})! Это официальный бот МБОУ "Лицей" г.о.Протвино. Здесь есть множество функций, о которых Вы можете узнать, открыв меню в левом нижнем углу.')
    else:
        bot.send_message(msg.chat.id, f'Приветствую Вас, {msg.from_user.first_name} {msg.from_user.last_name}! Это официальный бот МБОУ "Лицей" г.о.Протвино. Здесь есть множество функций, о которых Вы можете узнать, открыв меню в левом нижнем углу.')

@bot.message_handler(commands=['help'])
def help(msg):
    check(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.username, False, False, msg.text, datetime.datetime.now())

    bot.send_message(msg.chat.id, 'Все вопросы главному разработчику в личные сообщения\n Контакты - Гороховский Альберт(@somebodyoncetoldmetheworldisgg).')
    
@bot.message_handler(commands=['website']) 
def website(msg):
    check(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.username, False, False, msg.text, datetime.datetime.now())
    
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Сайт", url='https://protvino-licey.edumsko.ru/')
    markup.add(button1)
    bot.send_message(msg.chat.id, "Чтобы перейти на сайт Лицея, нажмите на эту кнопку", reply_markup=markup)
    
@bot.message_handler(commands=['menu']) 
def menu(msg):
    check(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.username, False, False, msg.text, datetime.datetime.now())
    
    markup = types.InlineKeyboardMarkup()
    data = Date(str(datetime.datetime.today()))
    link = 'https://protvino-licey.edumsko.ru/conditions/eating/menu/item/6665?date=' + data.day + '.' + data.month + '.' + data.year
    button1 = types.InlineKeyboardButton("Меню", url=link)
    markup.add(button1)
    bot.send_message(msg.chat.id, "Нажмите на кнопку, чтобы узнать меню на сегодня", reply_markup=markup)

@bot.message_handler(commands=['subscribe'])
def subscribe(msg):
    check(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.username, False, False, msg.text, datetime.datetime.now())

    index = findUser(msg.from_user.id)
    users[index].subscribe()
    save_data()
    bot.send_message(msg.chat.id, 'Вы успешно зарегистрировались на рассылку расписания. Она происходит примерно между 19 и 20 часами каждый рабочий день.\n Если Вы зарегистрировались случайно, отправьте команду /unsubscribe.')

@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(msg):
    check(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.username, False, False, msg.text, datetime.datetime.now())

    index = findUser(msg.from_user.id)
    users[index].isSubscribed = False
    save_data()
    bot.send_message(msg.chat.id, 'Вы отписались от рассылки расписания. Теперь Вам не будет приходить расписание.')

@bot.message_handler(commands=['text'])
def start(m):
    count = 10
    page = 1
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
    markup.add(types.InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
               types.InlineKeyboardButton(text=f'Вперёд --->', callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(page+1) + ",\"CountPage\":" + str(count) + "}"))

    bot.send_message(m.from_user.id, "Привет!!!", reply_markup = markup)
    
@bot.message_handler(content_types='text')
def message_reply(msg):
    check(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.username, False, False, msg.text, datetime.datetime.now())
    
    bot.send_message(msg.chat.id, 'Бот Вас не понял. Отправьте одну из команд бота')
    
@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    req = call.data.split('_')
    if req[0] == 'unseen':
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif 'pagination' in req[0]:
        json_string = json.loads(req[0])
        count = json_string['CountPage']
        page = json_string['NumberPage']
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
        if page == 1:
            markup.add(types.InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                       types.InlineKeyboardButton(text=f'Вперёд --->', callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(page + 1) + ",\"CountPage\":" + str(count) + "}"))
        elif page == count:
            markup.add(types.InlineKeyboardButton(text=f'<--- Назад', callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(page - 1) + ",\"CountPage\":" + str(count) + "}"), types.InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '))
        else:
            markup.add(types.InlineKeyboardButton(text=f'<--- Назад', callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(page-1) + ",\"CountPage\":" + str(count) + "}"), types.InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '), types.InlineKeyboardButton(text=f'Вперёд --->', callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(page+1) + ",\"CountPage\":" + str(count) + "}"))
        bot.edit_message_text(f'Страница {page} из {count}', reply_markup = markup, chat_id=call.message.chat.id, message_id=call.message.message_id)

mainThr = thr.Thread(target=bot.infinity_polling, args=())
thrs.append(mainThr)

start()
