'''
BOTNI ISHGA TUSHIRISH UCHUN KERAK BO'LADIGAN NARSALARNI KIRG'IZING
'''
from telebot import TeleBot
from config import TOKEN
from database.database import DataBase
from telebot import custom_filters
from telebot.storage import StateMemoryStorage
from telebot.types import BotCommand


db = DataBase()

state_storage = StateMemoryStorage()

bot = TeleBot(TOKEN, use_class_middlewares=True, state_storage=state_storage)

bot.set_my_commands(
    commands=[
        BotCommand('/start', 'Botni qayta ishga tushirish'),
        BotCommand('/help', 'Yordam uchun mu\'rojat qilish')
    ]
)





bot.add_custom_filter(custom_filters.StateFilter(bot))
