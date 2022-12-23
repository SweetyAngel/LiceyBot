import telebot
import datetime

class Date:
    def __init(self, date):
        date = date.split(' ')
        date = date[0].split('-')
        self.day = date[2]
        self.month = date[1]
        self.year = date[0]
        
class User:
    def __init__(self, userId, username, isSubscribed = False):
        self.userId = userId
        self.username = username
        self.isSubscribed = isSubscribed

    def subscribe(self):
        self.isSubscribed = True
        
global users

def users():
    f = open('users.py', 'r')
    
    countOfUsers = int(f.readline())
    users = []
    
    for i in range(countOfUsers-1):
        user = f.readline().split(':')
        userId = user[0]
        params = user[1].split(' ')
        username = params[0]
        isSubscribed = params[1]
        users.append(User(userId, username, isSubscribed))
                     
    f.close()
                     
    return users

def reg(userId, username, isSubscribed = False):
    users.append(User(userId, username, isSubscribed))

def save_data():
    f = open('users.py', 'w')
    f.write(str(len(users)))
    for user in users:
        f.write(f'{user.userId}:{user.username} {user.isSubscribed}')
        f.write('\n')
    f.close()

def isInUsers(userId, username):
    for user in users:
        if user.userId == userId:
            user.username = username
            save_data()
            return True
            break
    return False

def check(userId, username):
    if not isInUsers(userId, username):
        reg(userId, username)
        save_data()

def findUser(userId):
    for i in range(len(users)):
        if users[i].userId == userId:
            return i
            break
    

token = ''
bot = telebot.TeleBot(token)

users = users()

@bot.message_handler(commands=['start'])
def start(msg):
    check(msg.from_user.id, msg.from_user.username)
    
    if msg.from_user.username != 'None':
        bot.send_message(msg.chat.id, f'Приветствую Вас, {msg.from_user.first_name} {msg.from_user.last_name}(@{msg.from_user.username})! Это официальный бот МБОУ "Лицей" г.о.Протвино. Здесь есть множество функций, о которых Вы можете узнать, открыв меню в левом нижнем углу.')
    else:
        bot.send_message(msg.chat.id, f'Приветствую Вас, {msg.from_user.first_name} {msg.from_user.last_name}! Это официальный бот МБОУ "Лицей" г.о.Протвино. Здесь есть множество функций, о которых Вы можете узнать, открыв меню в левом нижнем углу.')

@bot.message_handler(commands=['help'])
def help(msg):
    check(msg.from_user.id, msg.from_user.username)

    bot.send_message(msg.chat.id, 'Все вопросы главному разработчику в личные сообщения\n Контакты - Гороховский Альберт(@somebodyoncetoldmetheworldisgg).')
    
@bot.message_handler(commands=['website']) 
def website(message):
    check(msg.from_user.id, msg.from_user.username)
    
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Сайт", url='https://protvino-licey.edumsko.ru/')
    markup.add(button1)
    bot.send_message(message.chat.id, "Чтобы перейти на сайт Лицея, нажмите на эту кнопку", reply_markup=markup)
    
@bot.message_handler(commands=['menu']) 
def menu(message):
    check(msg.from_user.id, msg.from_user.username)
    
    markup = types.InlineKeyboardMarkup()
    data = Date(str(datetime.datetime.today()))
    link = 'https://protvino-licey.edumsko.ru/conditions/eating/menu/item/6665?date=' + data.day + '.' + data.month + '.' + data.year
    button1 = types.InlineKeyboardButton("Меню", url=link)
    markup.add(button1)
    bot.send_message(message.chat.id, "Чтобы перейти на сайт Лицея, нажмите на кнопку", reply_markup=markup)

@bot.message_handler(commands=['subscribe'])
def successfulSubscription(msg):
    check(msg.from_user.id, msg.from_user.username)

    index = findUser(msg.from_user.id)
    users[index].subscribe()
    save_data()
    bot.send_message(msg.chat.id, 'Вы успешно зарегистрировались на рассылку расписания. Она происходит примерно между 19 и 20 часами каждый рабочий день.\n Если Вы зарегистрировались случайно, отправьте команду /unsubscribe.')

@bot.message_handler(commands=['unsubscribe'])
def successfulUnsubscription(msg):
    check(msg.from_user.id, msg.from_user.username)

    index = findUser(msg.from_user.id)
    users[index].isSubscribed = False
    save_data()
    bot.send_message(msg.chat.id, 'Вы отписались от рассылки расписания. Теперь Вам не будет приходить расписание.')
    
@bot.message_handler(content_types='text')
def message_reply(message):
    check(msg.from_user.id, msg.from_user.username)
    
    bot.send_message(msg.chat.id, 'Бот Вас не понял. Отправьте одну из команд бота')

bot.infinity_polling()
