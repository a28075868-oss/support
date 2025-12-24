from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove
import asyncio

# Вставь сюда свои данные
BOT_TOKEN = "8274127593:AAHJdVCUOrxMCZtKDuFgumhMT3CMhJGEQEA"
ADMIN_ID = 7394719247  # Например: 123456789

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Отслеживаем пользователей, которые уже отправили жалобу
user_submitted = set()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    if message.from_user.id in user_submitted:
        await message.answer("Вы уже отправляли жалобу, ждите ответа администратора.")
        return

    text = (
        "Привет! Я саппорт проекта Luminius.\n\n"
        "Пожалуйста, отправьте жалобу на баг или дюп **в одном сообщении**, строго по форме:\n"
        "1. Что за баг или дюп\n"
        "2. Как он работает или делается\n"
        "3. Ваш игровой никнейм\n\n"
        "⚠️ Строго всё в одном сообщении."
    )
    await message.answer(text, reply_markup=ReplyKeyboardRemove())

@dp.message()
async def bug_report_handler(message: types.Message):
    user_id = message.from_user.id

    if user_id in user_submitted:
        await message.answer("Вы уже отправили жалобу. Ждите ответа администратора.")
        return

    # Отмечаем, что пользователь отправил жалобу
    user_submitted.add(user_id)

    # Пересылаем администратору
    report_text = (
        f"Новая жалоба от @{message.from_user.username} (ID: {user_id}):\n\n"
        f"{message.text}"
    )
    await bot.send_message(ADMIN_ID, report_text)

    # Отправляем автоответ игроку
    await message.answer(
        "Спасибо за жалобу! Мы рассмотрим её и ответим в кратчайшие сроки."
    )

if __name__ == "__main__":
    import asyncio
    from aiogram import main
    main(dp)
