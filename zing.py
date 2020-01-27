import telebot
import requests
from bs4 import BeautifulSoup

TOKEN = ""
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    bot.send_chat_action(message.chat.id, 'typing')
    category(message)


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    if not (message.content_type == 'text'):
        bot.send_message(
            message.chat.id, f"please enter your name for search dear {message.chat.username}!")
    else:
        print(message.text)


def category(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    bot.send_chat_action(message.chat.id, 'typing')
    keyboard.row(
        telebot.types.InlineKeyboardButton(
            'Tracks', callback_data='get-Tracks'
        ),
        telebot.types.InlineKeyboardButton(
            'People', callback_data='get-People'
        ),
        telebot.types.InlineKeyboardButton(
            'Albums', callback_data='get-Albums'
        ),
        telebot.types.InlineKeyboardButton(
            'Playlists', callback_data='get-Playlists'
        )
    )
    bot.send_message(message.chat.id, 'chose your category',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback(query):
    if query.data.startswith('get-'):
        # search_music(query.message, query.data[4::])
        print(query.data)
        # TODO: create related urls
        url = f'https://soundcloud.com/search?q='
        bot.send_message(id, 'enter your search keyword')


def search_music(id, link):
    bot.send_chat_action(id, 'typing')

    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', class_='trackList__item')
    sound = []
    for res in results:
        sound += res.find(class_='sc-button-share')
    bot.send_message(id, sound)


bot.polling()
