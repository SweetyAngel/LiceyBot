import json
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
    def __init__(self, userId, firstName, secondName, username, isSubscribed = False):
        self.userId = userId
        self.firstName = firstName
        self.secondName = secondName
        self.username = username
        self.isSubscribed = isSubscribed

    def subscribe(self):
        self.isSubscribed = True
        
global users, thrs

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
    f = open('users.py', 'r')
    
    countOfUsers = int(f.readline())
    users = []
    
    for i in range(countOfUsers):
        user = f.readline().split(':')
        userId = user[0]
        params = user[1].split(' ')
        firstName = params[0]
        secondName = params[1]
        username = params[2]
        isSubscribed = params[3]
        users.append(User(userId, firstName, secondName, username, isSubscribed))
                     
    f.close()
                     
    return users

#Add users in users
def reg(userId, firstName, secondName, username, isSubscribed = False):
    users.append(User(userId, firstName, secondName, username, isSubscribed))

#Save users in users.py
def save_data():
    f = open('users.py', 'w')
    f.write(str(len(users)))
    for user in users:
        f.write(f'\n{user.userId}:{user.firstName} {user.secondName} {user.username} {user.isSubscribed}')
    f.close()

#Check if users exists in users
def isInUsers(userId, firstName, secondName, username):
    for user in users:
        if user.userId == userId:
            user.firstName = firstName
            user.secondName = secondName
            user.username = username
            save_data()
            return True
            break
    return False

#Reg users if he is not in users
def check(userId, firstName, secondName, username):
    if not isInUsers(userId, firstName, secondName, username):
        reg(userId, firstName, secondName, username)
        save_data()

#Find user in user
def findUser(userId):
    for i in range(len(users)):
        if users[i].userId == userId:
            return i
            break
    

token = ''
bot = telebot.TeleBot(token)

users = users()

@bot.message_handler(commands=['start'])
def start_msg(msg):
    check(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.username)
    
    if msg.from_user.username != 'None':
        bot.send_message(msg.chat.id, f'Приветствую Вас, {msg.from_user.first_name} {msg.from_user.last_name}(@{msg.from_user.username})! Это официальный бот МБОУ "Лицей" г.о.Протвино. Здесь есть множество функций, о которых Вы можете узнать, открыв меню в левом нижнем углу.')
    else:
        bot.send_message(msg.chat.id, f'Приветствую Вас, {msg.from_user.first_name} {msg.from_user.last_name}! Это официальный бот МБОУ "Лицей" г.о.Протвино. Здесь есть множество функций, о которых Вы можете узнать, открыв меню в левом нижнем углу.')

@bot.message_handler(commands=['help'])
def help(msg):
    check(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.username)

    bot.send_message(msg.chat.id, 'Все вопросы главному разработчику в личные сообщения\n Контакты - Гороховский Альберт(@somebodyoncetoldmetheworldisgg).')
    
@bot.message_handler(commands=['website']) 
def website(message):
    check(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.username)
    
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Сайт", url='https://protvino-licey.edumsko.ru/')
    markup.add(button1)
    bot.send_message(message.chat.id, "Чтобы перейти на сайт Лицея, нажмите на эту кнопку", reply_markup=markup)
    
@bot.message_handler(commands=['menu']) 
def menu(message):
    check(messsge.from_user.id, msg.from_user.first_name, msg.from_user.last_name, message.from_user.username)
    
    markup = types.InlineKeyboardMarkup()
    data = Date(str(datetime.datetime.today()))
    link = 'https://protvino-licey.edumsko.ru/conditions/eating/menu/item/6665?date=' + data.day + '.' + data.month + '.' + data.year
    button1 = types.InlineKeyboardButton("Меню", url=link)
    markup.add(button1)
    bot.send_message(message.chat.id, "Нажмите на кнопку, чтобы узнать меню на сегодня", reply_markup=markup)

@bot.message_handler(commands=['subscribe'])
def successfulSubscription(msg):
    check(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.username)

    index = findUser(msg.from_user.id)
    users[index].subscribe()
    save_data()
    bot.send_message(msg.chat.id, 'Вы успешно зарегистрировались на рассылку расписания. Она происходит примерно между 19 и 20 часами каждый рабочий день.\n Если Вы зарегистрировались случайно, отправьте команду /unsubscribe.')

@bot.message_handler(commands=['unsubscribe'])
def successfulUnsubscription(msg):
    check(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.username)

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
    check(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.username)
    
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
                       types.InlineKeyboardButton(text=f'Вперёд --->',
                                            callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                page + 1) + ",\"CountPage\":" + str(count) + "}"))
        elif page == count:
            markup.add(types.InlineKeyboardButton(text=f'<--- Назад',
                                            callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                page - 1) + ",\"CountPage\":" + str(count) + "}"),
                       types.InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '))
        else:
            markup.add(types.InlineKeyboardButton(text=f'<--- Назад', callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(page-1) + ",\"CountPage\":" + str(count) + "}"),
                           types.InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                           types.InlineKeyboardButton(text=f'Вперёд --->', callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(page+1) + ",\"CountPage\":" + str(count) + "}"))
        bot.edit_message_text(f'Страница {page} из {count}', reply_markup = markup, chat_id=call.message.chat.id, message_id=call.message.message_id)

mainThr = thr.Thread(target=bot.infinity_polling, args=())
thrs.append(mainThr)

start()
