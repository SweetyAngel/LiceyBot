import telebot

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
    f.write(len(users))
    for user in users:
        f.write(f'{user.userId}:{user.username} {user.isSubscribed}')
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
    for i in range(len(users)-1):
        if users[i].userId == userId:
            return i
            break
    

token = ''
bot = telebot.TeleBot(token)

users = users()

@bot.message_handler(commands=['start'])
def start(msg):
    users = check(msg.from_user.id, msg.from_user.username)
    
    if msg.from_user.username != 'None':
        bot.send_message(msg.chat.id, 'Приветствую Вас, {msg.from_user.first_name} {msg.from_user.last_name}(@{msg.from_user.username})! Это официальный бот МБОУ "Лицей" г.о.Протвино. Здесь есть множество функций, о которых Вы можете узнать, открыв меню в левом нижнем углу.')
    else:
        bot.send_message(msg.chat.id, 'Приветствую Вас, {msg.from_user.first_name} {msg.from_user.last_name}! Это официальный бот МБОУ "Лицей" г.о.Протвино. Здесь есть множество функций, о которых Вы можете узнать, открыв меню в левом нижнем углу.')

@bot.message_handler(commands=['help'])
def help(msg):
    users = check(msg.from_user.id, msg.from_user.username)

    save_data()
    bot.send_message(msg.chat.id, 'Все вопросы главному разработчику в личные сообщения\n Контакты - Гороховский Альберт(@somebodyoncetoldthewordisgg).')

@bot.message_handler(commands=['subscribe'])
def successfulSubscription(msg):
    users = check(msg.from_user.id, msg.from_user.username)

    index = findUser(msg.from_user.id)
    users[i].isSubscribed = True
    save_data()
    bot.send_message(msg.chat.id, 'Вы успешно зарегистрировались на рассылку расписания. Она происходит примерно между 19 и 20 часами каждый рабочий день.\n Если В ы зарегестрировались случайно, отправьте команду /unsubscribe.')

@bot.message_handler(commands=['unsubscribe'])
def successfulUnsubscription(msg):
    users = check(msg.from_user.id, msg.from_user.username)

    index = findUser(msg.from_user.id)
    users[i].isSubscribed = False
    save_data()
    bot.send_message(msg.chat.id, 'Вы отписались от рассылки расписания. Теперь Вам не будет приходить расписание.') 

bot.infinity_polling()
