import telebot
from telebot import types
import random
import time
import schedule
import re

bot = telebot.TeleBot('Your tg key')


# Словарь для хранения языка пользователя
user_language = {}


user_schedules = {}

# Флаг для режима "история"
history_mode = {}

# Словарь для хранения состояния истории
history_state = {}

# Словарь для хранения настроек пользователя
user_settings = {}


is_bot_active = False

# Список сообщений для команды /now
now_messages = [
    "Сейчас ты находишься на пути к успеху! Продолжай двигаться вперед.",
    "Помни, что каждый день - это возможность стать ближе к своей мечте.",
    "Ты уже сделал большие успехи, но впереди еще много интересного!",
    "Не забывай делать перерывы и заботиться о себе. Это поможет тебе оставаться в форме.",
    "Твоя упорная работа обязательно принесет плоды. Не сдавайся!",
    "Ты на верном пути, продолжай в том же духе!"
]

now_external = [
    "Ты можешь добиться большего, если будешь прилагать больше усилий!",
    "Не останавливайся, ты почти у цели!",
    "Помни, что успех ждет тех, кто не боится трудностей.",
    "Ты справишься со всем, если будешь верить в себя.",
    "Каждый день - это шаг к твоей мечте, не упусти свой шанс!"
]

now_internal = [
    "Ты уже многого достиг, будь гордым за себя!",
    "Ты сам знаешь, что тебе нужно делать, следуй своему внутреннему голосу.",
    "Твои решения ведут тебя к успеху, продолжай в том же духе.",
    "Ты сильный и целеустремленный, верь в себя!",
    "Ты сам себе хозяин, ты можешь достичь всего, что пожелаешь."
]

now_mixed = [
    "Ты на верном пути, но не забывай о своих силах и возможностях!",
    "Каждый день - это шанс стать лучше, используй его с умом.",
    "Твоя упорная работа и вера в себя обязательно принесут плоды.",
    "Ты можешь добиться большего, если будешь прилагать усилия и верить в себя.",
    "Не останавливайся, ты уже близок к своей цели, продолжай двигаться вперед!"
]

messages = [
    "Не забывай о своих целях и продолжай двигаться вперед!",
    "Сегодня отличный день, чтобы сделать еще один шаг к успеху.",
    "Помни, что каждый день - это возможность стать лучше.",
    "Ты на верном пути, не сдавайся и продолжай работать над собой.",
    "Сегодня твой день, используй его с максимальной пользой!"
]

time_external = [
    "Не упускай свой шанс, сегодня важный день для твоего успеха!",
    "Помни, что успех ждет тех, кто не боится трудностей.",
    "Сегодня твой день, покажи всем, на что ты способен!",
    "Ты можешь добиться большего, если будешь прилагать больше усилий.",
    "Сегодня отличный день, чтобы сделать еще один шаг к своей мечте."
]

time_internal = [
    "Ты уже многого достиг, будь гордым за себя!",
    "Ты сам знаешь, что тебе нужно делать, следуй своему внутреннему голосу.",
    "Твои решения ведут тебя к успеху, продолжай в том же духе.",
    "Ты сильный и целеустремленный, верь в себя!",
    "Сегодня твой день, используй его с максимальной пользой для себя."
]

time_mixed = [
    "Сегодня отличный день, чтобы сделать еще один шаг к успеху!",
    "Твоя упорная работа и вера в себя обязательно принесут плоды.",
    "Ты можешь добиться большего, если будешь прилагать усилия и верить в себя.",
    "Не останавливайся, ты уже близок к своей цели, продолжай двигаться вперед!",
    "Помни, что каждый день - это возможность стать лучше, используй ее с умом."
]

quotes_messages = [
    "«Успех - это способность двигаться от неудачи к неудаче, не теряя энтузиазма.» - Уинстон Черчилль",
    "«Деньги - это не все, но без них ты ничто.» - Арсений Яценюк",
    "«Если вы можете мечтать об этом, вы можете этого добиться.» - Уолт Дисней",
    "«Не бойтесь совершать ошибки. Бойтесь не делать ничего.» - Роберт Кийосаки",
    "«Успех - это путь, а не пункт назначения.» - Бен Стейн"
]


@bot.message_handler(commands=['start'])
def start(message):
    global is_bot_active
    bot.send_message(message.chat.id, 'Добро пожаловать в бота-помощника! Чтобы узнать, что я умею, введите команду /instruction')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, 'Также вы можете пройти опрос, чтобы определить, какая мотивация вам больше подходит. Введите команду /opros', reply_markup=markup)
    is_bot_active = True


# Функция для обработки команды /history
@bot.message_handler(commands=['history'])
def history(message):
    history_mode[message.chat.id] = True
    history_state[message.chat.id] = 0
    bot.send_message(message.chat.id, 'Добро пожаловать в историю миллионера! Ваши решения будут влиять на его судьбу. Чтобы остановить историю, отправьте команду /stop')
    bot.send_message(message.chat.id, 'Итак, начнем. Вы просыпаетесь утром от звонка будильника. Вы чувствуете себя уставшим и не хотите вставать. Что вы сделаете?', reply_markup=get_choices_markup('Встать', 'Продолжить спать'))


@bot.message_handler(commands=['stop'])
def stop(message):
    history_mode[message.chat.id] = False
    user_settings[message.chat.id] = {'motivation': 'mixed'}
    bot.send_message(message.chat.id,'История остановлена. Все настройки сброшены. Чтобы начать заново, отправьте команду /start')


@bot.message_handler(func=lambda message: history_mode.get(message.chat.id, False))
def history_progress(message):
    state = history_state[message.chat.id]
    if state == 0:
        if message.text == 'Встать':
            bot.send_message(message.chat.id, 'Вы решили встать и начать свой день. Вы чувствуете себя бодрым и готовым к новым свершениям. Вы идете на работу с хорошим настроением.')
            bot.send_message(message.chat.id, 'На работе вам предлагают новый проект. Это рискованный, но потенциально прибыльный проект. Что вы сделаете?', reply_markup=get_choices_markup('Принять проект', 'Отказаться от проекта'))
            history_state[message.chat.id] = 1
        elif message.text == 'Продолжить спать':
            bot.send_message(message.chat.id, 'Вы решили продолжить спать. Вы проспали важную встречу на работе и упустили возможность получить повышение. Ваша карьера застопорилась.')
            history_state[message.chat.id] = -1
    elif state == 1:
        if message.text == 'Принять проект':
            bot.send_message(message.chat.id, 'Вы приняли проект и усердно работали над ним. Проект оказался успешным, и вы получили большую прибыль. Ваша репутация на работе значительно выросла.')
            bot.send_message(message.chat.id, 'Теперь у вас есть возможность инвестировать эти деньги. Что вы сделаете?', reply_markup=get_choices_markup('Инвестировать в акции', 'Открыть свой бизнес'))
            history_state[message.chat.id] = 2
        elif message.text == 'Отказаться от проекта':
            bot.send_message(message.chat.id, 'Вы отказались от проекта. Хотя вы избежали риска, вы также упустили возможность значительно продвинуться в карьере. Ваша карьера продолжается в обычном темпе.')
            history_state[message.chat.id] = -1
    elif state == 2:
        if message.text == 'Инвестировать в акции':
            bot.send_message(message.chat.id, 'Вы решили инвестировать деньги в акции. Вы внимательно изучили рынок и сделали удачные вложения. Ваши инвестиции принесли хорошую прибыль, и ваше состояние значительно выросло.')
            bot.send_message(message.chat.id, 'Теперь у вас есть возможность открыть свой бизнес. Что вы сделаете?', reply_markup=get_choices_markup('Открыть свой бизнес', 'Продолжить инвестировать'))
            history_state[message.chat.id] = 3
        elif message.text == 'Открыть свой бизнес':
            bot.send_message(message.chat.id, 'Вы решили открыть свой бизнес. Вы тщательно изучили рынок, составили бизнес-план и нашли надежных партнеров. Ваш бизнес оказался успешным, и вы стали владельцем процветающей компании.')
            history_state[message.chat.id] = 4
    elif state == 3:
        if message.text == 'Открыть свой бизнес':
            bot.send_message(message.chat.id, 'Вы решили открыть свой бизнес. Вы тщательно изучили рынок, составили бизнес-план и нашли надежных партнеров. Ваш бизнес оказался успешным, и вы стали владельцем процветающей компании.')
            bot.send_message(message.chat.id, 'Поздравляем! Вы успешно прошли историю миллионера. Ваши решения привели вас к богатству и успеху. Вы стали уважаемым и влиятельным человеком в обществе.')
            history_mode[message.chat.id] = False
            history_state[message.chat.id] = 4
        elif message.text == 'Продолжить инвестировать':
            bot.send_message(message.chat.id, 'Вы продолжили инвестировать свои деньги. Вы стали опытным инвестором и научились эффективно управлять своим портфелем. Ваше состояние продолжало расти, и вы стали одним из самых богатых людей в городе.')
            history_state[message.chat.id] = 4
            bot.send_message(message.chat.id,'Поздравляем! Вы успешно прошли историю миллионера. Ваши решения привели вас к богатству и успеху. Вы стали уважаемым и влиятельным человеком в обществе.')
            history_mode[message.chat.id] = False
            history_state[message.chat.id] = 4
    elif state == -1:
        bot.send_message(message.chat.id, 'К сожалению, ваши решения не привели к успеху. Вы продолжаете жить обычной жизнью и не становитесь миллионером.')
        history_mode[message.chat.id] = False


@bot.message_handler(commands=['quotes'])
def quotes(message):
    random_quote = random.choice(quotes_messages)
    bot.send_message(message.chat.id, random_quote)


@bot.message_handler(commands=['opros'])
def opros(message):
    bot.send_message(message.chat.id, "Чтобы выявить свою мотивацию, пройдите опрос по ссылке")
    bot.send_message(message.chat.id, "@OprosMotivationJack_bot")


@bot.message_handler(commands=['now'])
def now(message):
    motivation = user_settings.get(message.chat.id, {'motivation': 'mixed'})['motivation']
    if motivation == 'external':
        random_message = random.choice(now_external)
    elif motivation == 'internal':
        random_message = random.choice(now_internal)
    else:
        random_message = random.choice(now_mixed)
    bot.send_message(message.chat.id, random_message)

#----------------------------------------------

#----------------------------------------------
@bot.message_handler(commands=['settings'])
def settings(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Внешняя мотивация')
    btn2 = types.KeyboardButton('Внутренняя мотивация')
    btn3 = types.KeyboardButton('Смешанная мотивация')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'Выберите тип мотивации:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['Внешняя мотивация', 'Внутренняя мотивация', 'Смешанная мотивация'])
def set_motivation(message):
    user_settings[message.chat.id] = {'motivation': message.text.lower().replace('мотивация', '').strip()}
    bot.send_message(message.chat.id, f'Установлена {message.text}.')


@bot.message_handler(commands=['instruction'])
def instruction(message):
    bot.send_message(message.chat.id, 'Инструкция по использованию бота:\n\n'
                                     '1. Команда /start - запуск бота и приветствие.\n'
                                     '2. Команда /history - запуск истории миллионера, где вы будете принимать решения, влияющие на его судьбу.\n'
                                     '3. Команда /stop - остановка и сброс всех настроек.\n'
                                     '4. Команда /now - получение мотивирующего сообщения.\n'
                                     '5. Команда /time - установка времени для получения ежедневных мотивирующих сообщений.\n'
                                     '6. Команда /quotes - получение цитаты известного миллионера.\n'
                                     '7. Команда /settings - выбор типа мотивации (внешняя, внутренняя, смешанная).\n'
                                     '8. Команда /opros - прохождение опроса для определения типа мотивации.\n'
                                     '9. Команда /instruction - вывод этой инструкции.')


# Обработчик команды /time
@bot.message_handler(commands=['time'])
def start(message):
    global is_bot_active
    if is_bot_active:
        bot.reply_to(message, "Бот начал работу. Введите время отправки сообщений в формате: -3 ЧЧ:ММ, разделяя временные отметки точкой с запятой (например, если вы хотите, что бы сообщения приходили в 22:01;12:30;17:52 по МСК времени, то введите: 19:01;09:30;14:52 ).")
        is_bot_active = True
    else:
         bot.reply_to(message, "Бот не активен. Используйте команду /start для запуска бота.")

# Обработчик сообщений с временем отправки
@bot.message_handler(func=lambda message: True)
def set_schedule(message):
    if is_bot_active:
        user_id = message.from_user.id
        try:
            # Разбиваем сообщение на части для получения времени отправки
            times = message.text.split(';')
            for time_str in times:
                if not re.match(r'^\d{2}:\d{2}$', time_str.strip()):
                    bot.reply_to(message,
                    "Ошибка: введите команду или если вы в команде /time то введён неверный формат времени.")
                    return
            user_schedules[user_id] = times
            bot.reply_to(message, f"Расписание установлено. Сообщения будут отправляться в {', '.join(times)}.")
            setup_user_schedules()
        except:
            bot.reply_to(message,
                "Ошибка: введите команду или если вы в команде /time то введён неверный формат времени.")


# Функция для отправки случайного сообщения пользователю
def send_random_message(user_id):
    if is_bot_active and user_id in user_schedules:
        message = random.choice(messages)
        bot.send_message(user_id, message)

# Функция для настройки расписания отправки сообщений для каждого пользователя
def setup_user_schedules():
    schedule.clear()
    for user_id, times in user_schedules.items():
        for time_str in times:
            schedule.every().day.at(time_str).do(send_random_message, user_id=user_id)

def run_scheduler():
     while True:
        schedule.run_pending()
        time.sleep(1)

def get_choices_markup(choice1, choice2):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(choice1)
    btn2 = types.KeyboardButton(choice2)
    markup.add(btn1, btn2)
    return markup


if __name__ == '__main__':
    import threading
    threading.Thread(target=run_scheduler).start()
    bot.polling(none_stop=True)
    bot.polling()

