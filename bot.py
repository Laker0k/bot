import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from dotenv import load_dotenv

# Загружаем токен из .env
load_dotenv()
BOT_TOKEN = os.getenv("8014426625:AAFguwZOWffOOKOz5mxK3qPpumCP4R0_gF8")
CHANNEL_ID = "@hatasoloda"

# Настраиваем бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Полный список серверов
servers = {
    "🫛Podolsk": "",
    "💥Surgut": "",
    "😾Izhevsk": "",
    "🏍️Tver": "",
    "🛞Tomsk": "",
    "🥊Vologda": "",
    "🫐Taganrog": "",
    "🌼N.Novgorod": "",
    "🌸Kaluga": "",
    "🎭Vladimir": "",
    "🦆Kostroma": "",
    "🦎Chita": "",
    "🧣Astrakhan": "",
    "👜Bratsk": "",
    "🥐Tambov": "",
    "🥽Yakutsk": "",
    "🍭Ulyanovsk": "",
    "🎈Lipetsk": "",
    "💦Barnaul": "",
    "🏛Yaroslavl": "",
    "🦅Orel": "",
    "🧸Bryansk": "",
    "🪭Pskov": "",
    "🫚Smolensk": "",
    "🪼Stavropol": "",
    "🪅Ivanovo": "",
    "🪸Tolyatti": "",
    "🐋Tyumen": "",
    "🌺Kemerovo": "",
    "🔫Kirov": "",
    "🍖Orenburg": "",
    "🥋Arkhangelsk": "",
    "🃏Kursk": "",
    "🎳Murmansk": "",
    "🎷Penza": "",
    "🎭Ryazan": "",
    "⛳Tula": "",
    "🏟Perm": "",
    "🐨Khabarovsk": "",
    "🪄Cheboksary": "",
    "🖇Krasnoyarsk": "",
    "🕊Chelyabinsk": "",
    "👒Kaliningrad": "",
    "🧶Vladivostok": "",
    "🌂Vladikavkaz": "",
    "⛑️Makhachkala": "",
    "🎓Belgorod": "",
    "👑Voronezh": "",
    "🎒Volgograd": "",
    "🌪Irkutsk": "",
    "🪙Omsk": "",
    "🐉Saratov": "",
    "🍙Grozny": "",
    "🍃Novosib": "",
    "🪿Arzamas": "",
    "🪻Krasnodar": "",
    "📗Ekb": "",
    "🪺Anapa": "",
    "🍺Rostov": "",
    "🎧Samara": "",
    "🏛Kazan": "",
    "🌊Sochi": "",
    "🌪Ufa": "",
    "🌉Spb": "",
    "🌇Moscow": "",
    "🤎Choco": "",
    "📕Chilli": "",
    "❄Ice": "",
    "📓Gray": "",
    "📘Aqua": "",
    "🩶Platinum": "",
    "💙Azure": "",
    "💛Gold": "",
    "❤‍🔥Crimson": "",
    "🩷Magenta": "",
    "🤍White": "",
    "💜Indigo": "",
    "🖤Black": "",
    "🍒Cherry": "",
    "💕Pink": "",
    "🍋Lime": "",
    "💜Purple": "",
    "🧡Orange": "",
    "💛Yellow": "",
    "💙Blue": "",
    "💚Green": "",
    "❤️Red": ""
}

# Категории
categories = ["ЕГА", "Гараж БУС", "Гараж АРЗ", "БАТ ВЧ", "БАТ ферма", "ГАР", "НИЖ", "ЕГА БГ", "ЕГА СГ", "КОР", "БУС"]

# Клавиатуры
main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(KeyboardButton("📜 Показать список"), KeyboardButton("➕ Добавить информацию"))

server_kb = ReplyKeyboardMarkup(resize_keyboard=True)
for server in servers.keys():
    server_kb.add(KeyboardButton(server))

category_kb = ReplyKeyboardMarkup(resize_keyboard=True)
for category in categories:
    category_kb.add(KeyboardButton(category))


# Проверка подписки на канал
async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not await check_subscription(message.from_user.id):
        await message.answer("❗ Подпишитесь на канал, чтобы использовать бота: https://t.me/hatasoloda")
        return
    await message.answer("Привет! Выберите действие:", reply_markup=main_kb)


@dp.message_handler(lambda message: message.text == "📜 Показать список")
async def show_list(message: types.Message):
    text = "\n".join([f"{name} - {info}" for name, info in servers.items()])
    await message.answer(f"📜 Текущий список:\n\n{text}")


@dp.message_handler(lambda message: message.text == "➕ Добавить информацию")
async def choose_server(message: types.Message):
    if not await check_subscription(message.from_user.id):
        await message.answer("❗ Подпишитесь на канал, чтобы использовать бота: https://t.me/hatasoloda")
        return
    await message.answer("Выберите сервер:", reply_markup=server_kb)


@dp.message_handler(lambda message: message.text in servers.keys())
async def choose_category(message: types.Message):
    global selected_server
    selected_server = message.text
    await message.answer(f"Вы выбрали {selected_server}. Теперь выберите категорию:", reply_markup=category_kb)


@dp.message_handler(lambda message: message.text in categories)
async def add_info(message: types.Message):
    global selected_server
    servers[selected_server] += f"{message.text}, "
    await message.answer(f"✅ Добавлено: {message.text} в {selected_server}!", reply_markup=main_kb)
    await check_auto_broadcast()


# Авторассылка
user_data = {}
broadcast_threshold = 20


async def check_auto_broadcast():
    total_entries = sum(len(info.split(", ")) for info in servers.values())
    if total_entries >= broadcast_threshold:
        message_text = "📢 Важное обновление!\n\n" + "\n".join([f"{name} - {info}" for name, info in servers.items()])
        await send_broadcast(message_text)
        clear_data()


async def send_broadcast(text):
    for user_id in user_data.keys():
        try:
            await bot.send_message(user_id, text)
        except Exception as e:
            logging.error(f"Ошибка отправки сообщения пользователю {user_id}: {e}")


def clear_data():
    for key in servers.keys():
        servers[key] = ""


async def schedule_daily_broadcast():
    while True:
        now = asyncio.get_event_loop().time()
        target_time = now + (4.5 * 3600)  # 04:30 МСК
        await asyncio.sleep(target_time - now)
        message_text = "📢 Ежедневный отчет!\n\n" + "\n".join([f"{name} - {info}" for name, info in servers.items()])
        await send_broadcast(message_text)
        clear_data()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(schedule_daily_broadcast())
    executor.start_polling(dp, skip_updates=True)
