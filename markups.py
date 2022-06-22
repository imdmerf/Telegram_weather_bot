from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --- Menu ---
know_weater = KeyboardButton('Узнать погоду')
subscribe = KeyboardButton('Подписаться на уведомления о погоде')
unsubscribe = KeyboardButton('Отписаться от уведомлени о погоде')

mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(
    know_weater,
    subscribe,
    unsubscribe,)

btncn = KeyboardButton("Отмена")
cancel = ReplyKeyboardMarkup(resize_keyboard = True).add(
    btncn
)
yes = KeyboardButton("Да")
confirm = ReplyKeyboardMarkup(resize_keyboard= True).add(
    yes,
    btncn
)
