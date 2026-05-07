import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Загружаем переменные окружения из файла .env
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Пожалуйста, установите TELEGRAM_BOT_TOKEN в файле .env")

# Инициализируем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = (
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Я — бот управления **Adaptive Behavioral Stealth VPN**.\n"
        "Здесь ты сможешь получить свой профиль подключения и отслеживать статус маскировки трафика.\n\n"
        "Нажми /connect для получения тестовых настроек."
    )
    await message.answer(welcome_text, parse_mode="Markdown")

import aiohttp

# Хэндлер на команду /connect
@dp.message(Command("connect"))
async def cmd_connect(message: types.Message):
    # Делаем асинхронный запрос к нашему ML-движку
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://127.0.0.1:5000/pattern?profile=video") as response:
                if response.status == 200:
                    data = await response.json()
                    jitter = data.get("jitter_ms", "N/A")
                    padding = data.get("padding_bytes", "N/A")
                    
                    connect_text = (
                        "🔐 **Соединение установлено!**\n\n"
                        "Связь с ML-ядром успешна. ИИ сгенерировал новый паттерн маскировки:\n"
                        f"Имитация: `Потоковое видео`\n"
                        f"Задержка (Jitter): `{jitter} мс`\n"
                        f"Размер мусора (Padding): `{padding} байт`\n\n"
                        "Текущий статус туннеля: 🟢 АКТИВЕН"
                    )
                else:
                    connect_text = "⚠️ Ошибка связи с ML-сервером. Используются базовые настройки."
    except Exception as e:
        connect_text = f"⚠️ ML-модуль недоступен. Запустите api.py!\nОшибка: {e}"

    await message.answer(connect_text, parse_mode="Markdown")

async def main():
    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
