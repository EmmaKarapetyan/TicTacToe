import telebot
from telebot import types
from tgame_XO import TicTacToeGame

bot = telebot.TeleBot('7030877829:AAFMoN2SnbB_ivzfa_HSh-hvKhgVNg7lpLc')

level = None
character = None

@bot.message_handler(commands = ['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Tic_Tac_Toe_easy", callback_data="easy")
    button2 = types.InlineKeyboardButton("Tic_Tac_Toe_hard", callback_data="hard")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Choose: ", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['easy', 'hard'])
def callback_query(call):
    global level
    level = call.data
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("X", callback_data="X")
    button2 = types.InlineKeyboardButton("O", callback_data="O")
    markup.add(button1, button2)
    bot.send_message(call.message.chat.id, "X player will go first. Choose:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['X', 'O'])
def callback_query(call):
    try:
        global character, level, game_list
        character = call.data
        game = TicTacToeGame(character, level)
        game.start_game(bot, call)
        while game.endGame():        
            game.game(bot, call)
        bot.send_message(call.message.chat.id, f"{game.character} player Wins!")
        start_message(call.message)
    except:
        pass
    
bot.polling() 