import os

from aiogram import Router, F
from aiogram.types import FSInputFile
from aiogram.types import Message

from utils.functions import show_mistakes

router = Router()
cat = FSInputFile("C:/Users/user/PycharmProjects/DvijeniePervih/certificate.jpg")


# Хэндлер, на кнопку "посмотреть ошибки" и функция отправки сообщения с ошибками
@router.message(F.text.lower().in_(['посмотреть ошибки']))
async def show_mistakes_button(message: Message):
    answer_text = show_mistakes(message.from_user.id)
    await message.answer(text=answer_text)


# Недописанная функция с получением сертификата
@router.message(F.text.lower().in_(['получить сертификат']))
async def get_certificate(message: Message):
    await message.answer_photo(photo=cat,
                               caption='Сертификат!')


# Хэндлер на команду "/channel" и функция, отправляющая пользователю ссылку на канал
# (ссылка указана в файле конфигурации (.env)
@router.message(F.text.lower().in_(['/channel']))
async def get_chanel(message: Message):
    await message.answer(os.getenv('LINK'))


# Хэндлер на команду "/help" и функция, выдающая основную информацию о боте и командах
@router.message(F.text.lower().in_(['/help']))
async def get_chanel(message: Message):
    await message.answer(text='На прохождение теста даётся одна попытка, без возможности изменения результатов. '
                              'После прохождения теста будет возможность посмотреть ошибки и скачать сертификат\n'
                              '/start - это приветственное сообщение, описывающее предназначение бота\n'
                              '/test - команда, для начала тестирования. Её также нужно нажать после подписки на канал '
                              '(до прохождения теста)\n'
                              '/help - Вы сейчас здесь 😊\n'
                              '/channel - бот отправит ссылку на канал')


# Хэндлер на остальные сообщения
@router.message(F.text)
async def else_messege(message: Message):
    await message.answer('Извините, я не знаю такой команды :(\nПопробуйте "/start", "/test или /help')
