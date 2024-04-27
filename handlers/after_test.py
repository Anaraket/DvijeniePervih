import os

from aiogram import Router, F
from aiogram.types import FSInputFile
from aiogram.types import Message

from utils.db import Database
from utils.sertificate_create import certificate

router = Router()


# Недописанная функция с получением сертификата
@router.message(F.text.lower().in_(['получить сертификат']))
async def get_certificate(message: Message):
    try:
        await message.answer(text="Пожалуйста, подождите, сертификат создаётся ⌛️")
        db = Database(os.getenv('DATABASE_NAME'))
        certificate(fio=db.select_columns_from_users_table(column_names=['fio'], user_id=message.from_user.id),
                    result=db.select_columns_from_users_table(column_names=['result'], user_id=message.from_user.id))
        cat = FSInputFile(
            path=f"/root/bots/DvijeniePervih/utils/upload/{(db.select_columns_from_users_table(['fio'], message.from_user.id))[0]}.pdf")
        await message.answer_document(document=cat,
                                      caption='Поздравляю! Ваш заслуженный сертификат о прохождении завершающего'
                                              ' тестирования!')
    except TypeError:
        await message.answer(text="Для начала пройдите тестирование")
        print("Произошла ошибка: объект NoneType не поддерживает индексацию "
              "(кто-то пытается получить сертификат без прохождения теста)")


# Хэндлер на команду "/channel" и функция, отправляющая пользователю ссылку на канал
# (ссылка указана в файле конфигурации (.env)
@router.message(F.text.lower().in_(['/channel']))
async def get_chanel(message: Message):
    await message.answer(os.getenv('LINK'))


# Хэндлер на команду "/help" и функция, выдающая основную информацию о боте и командах
@router.message(F.text.lower().in_(['/help']))
async def get_help(message: Message):
    await message.answer(text='На прохождение теста даётся одна попытка, без возможности изменения результатов.'
                              'После прохождения теста Вы сможете посмотреть ошибки и скачать сертификат!\n'
                              'Команды для взаимодействия с ботом:\n'
                              '/start - здесь Вы можете начать прохождение теста\n'
                              '/help - Вы сейчас здесь 😊\n'
                              '/channel - бот отправит ссылку на канал')


# Хэндлер на остальные сообщения
@router.message(F.text)
async def else_message(message: Message):
    await message.answer('Извините, я не знаю такой команды 😔\nПопробуйте /start, /channel или /help')
