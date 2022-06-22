from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import markups as nav
import aiogram.utils.markdown as hlink
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from parse import weater_now
from database import Database


TOKEN = "" # enter bot token


bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database('users.db')

class application(StatesGroup):
    city = State()
    register_city = State()
    unregiser = State()

secretstates = application.city, application.register_city
@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    if not db.user_registered(message.from_user.id):
        db.add_user(message.from_user.id)
    await bot.send_message(message.from_user.id, "Добро пожаловать!\nЭто бот поможет вам узнать погоду!", reply_markup = nav.mainMenu)


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await bot.send_message(message.from_user.id, 'Операция отменена', reply_markup=nav.mainMenu)
        return

    await state.finish()
    await message.reply('Операция отменена', reply_markup=nav.mainMenu)

@dp.message_handler(Text(equals='Узнать погоду'))
async def cmd_start(message: types.Message):
    await application.city.set()
    await message.reply("Укажите ваш город:", reply_markup=nav.cancel)


@dp.message_handler(state=application.city)
async def process_city(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['city'] = message.text
            await application.next()
            weater_data = weater_now(data['city'])
            await bot.send_message(message.from_user.id, hlink.text(
                hlink.text("Ваш город: ", data['city'].capitalize()),
                hlink.text("На данный момент на улице:", weater_data[1], "℃"),
                hlink.text("Сейчас:", weater_data[2].capitalize()),
                sep='\n'
            ), 
            reply_markup=nav.mainMenu)
            await state.finish()
    except KeyError as ke:
        await bot.send_message(message.from_user.id, 'Проверьте правильность названия города!')
        await application.city.set()
        return
        

@dp.message_handler(Text(equals='Подписаться на уведомления о погоде'))
async def cmd_start(message: types.Message):
    await application.register_city.set()
    await message.reply("Укажите ваш город:", reply_markup=nav.cancel)

@dp.message_handler(state=application.register_city)
async def process_register_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['register_city'] = message.text
        await application.next()
        db.set_sub(message.from_user.id, data['register_city'])
        await bot.send_message(message.from_user.id, 'Вы были успешно зарегистрированы!', reply_markup=nav.mainMenu)
        await state.finish()

@dp.message_handler(Text(equals='Отписаться от уведомлени о погоде'))
async def cmd_start(message: types.Message):
    await application.unregiser.set()
    await message.reply("Вы уверены?", reply_markup=nav.confirm)

@dp.message_handler(state=application.unregiser)
async def process_unregiser(message: types.Message, state: FSMContext):
    await application.next()
    if message.text == "Да":
        db.set_unsub(message.from_user.id)
        await bot.send_message(message.from_user.id, 'Вы больше не будете получать оповещения о погоде!', reply_markup=nav.mainMenu)
    else:
        await bot.send_message(message.from_user.id, 'Операция отменена', reply_markup=nav.mainMenu)  
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)
