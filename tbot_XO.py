import telebot
from telebot import types
from tgame_XO import *

bot = telebot.TeleBot('7030877829:AAFMoN2SnbB_ivzfa_HSh-hvKhgVNg7lpLc')

games = {}

@bot.message_handler(commands = ['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Tic_Tac_Toe_easy", callback_data="easy")
    button2 = types.InlineKeyboardButton("Tic_Tac_Toe_hard", callback_data="hard")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Choose: ", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['easy', 'hard'])
def level_choice(call):
    level = call.data
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("X", callback_data=f"X_{level}")
    button2 = types.InlineKeyboardButton("O", callback_data=f"O_{level}")
    markup.add(button1, button2)
    bot.send_message(call.message.chat.id, "X player will go first. Choose:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] in ['X', 'O'])
def character_choice(call):
    character, level = call.data.split('_')
    game = TicTacToeGame(character, level)
    games[call.message.chat.id] = game
    game.start_game(bot, call)

@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def handle_move(call):
    game = games.get(call.message.chat.id)
    if game:
        game.user_play(bot, call)
        message = game.end_game()
        if message:
            bot.send_message(call.message.chat.id, message)
            games.pop(call.message.chat.id, None)
            start_message(call.message)

bot.polling()
