import random
from telebot import types

class TicTacToeGame:
    def __new__(cls, *args, **kwargs):
        instance = super(TicTacToeGame, cls).__new__(cls)
        return instance
    
    def __init__(self, uch, level):
        self.length = 3
        self.board = [[' ' for _ in range(self.length)] for _ in range(self.length)]
        self.win = False
        self.level = level
        self.character = 'X'
        self.uch = uch
        self.cch = 'O'
        if uch == 'O':
            self.cch = 'X'
        self.message_id = None


    def edit_board(self):
        button_list = []
        index = 0
        for line in self.board:
            for item in line:
                button = types.InlineKeyboardButton(item, callback_data=str(index))
                button_list.append(button)
                index += 1
        markup = types.InlineKeyboardMarkup(row_width=self.length)
        markup.add(*button_list)
        return markup


    def evaluate(self):
        win_cond = [
            ([0, 0], [0, 1], [0, 2]), ([1, 0], [1, 1], [1, 2]), ([2, 0], [2, 1], [2, 2]),  # Rows
            ([0, 0], [1, 0], [2, 0]), ([0, 1], [1, 1], [2, 1]), ([0, 2], [1, 2], [2, 2]),  # Columns
            ([0, 0], [1, 1], [2, 2]), ([0, 2], [1, 1], [2, 0])   # Diagonals
        ]
        for cond in win_cond:
            row1, col1 = cond[0]
            row2, col2 = cond[1]
            row3, col3 = cond[2]
            if self.board[row1][col1] == self.board[row2][col2] == self.board[row3][col3] != ' ':
                self.win = True
                if self.board[row1][col1] == 'X':
                    return 10
                else:
                    return -10
        return 0


    def rand_play(self, bot, call):
        check = True
        while check:
            index = random.randint(0, self.length * self.length - 1)
            row, col = divmod(index, self.length)
            if self.board[row][col] == ' ':
                self.board[row][col] = self.character
                self.evaluate()
                if not self.win:
                    self.character = self.uch
                else:
                    bot.send_message(call.message.chat.id, f"{self.uch} player Wins!")
                check = False
        bot.edit_message_reply_markup(call.message.chat.id, self.message_id, reply_markup=self.edit_board())
        if not self.win:
            self.user_play(bot, call)
    

    def user_play(self, bot, call):
        @bot.callback_query_handler(func=lambda call: True)
        def play(call):
            row, col = divmod(int(call.data), self.length)
            if self.board[row][col] == ' ':
                self.board[row][col] = self.uch
                bot.edit_message_reply_markup(call.message.chat.id, self.message_id, reply_markup=self.edit_board())
                self.evaluate()
                if not self.win:
                    self.character = self.cch
                    if self.level == 'easy':
                        self.rand_play(bot, call)
                    elif self.level == 'hard':
                        self.hard_play(bot, call)
                else:
                    bot.send_message(call.message.chat.id, f"{self.uch} player Wins!")
        bot.register_next_step_handler(call.message, play)  
        

    def minimax(self, depth, isMax):
        score = self.evaluate()
        self.win = False
        if score == 10:
            return score - depth
        if score == -10:
            return score + depth
        if not any(' ' in row for row in self.board):
            return 0

        if isMax:
            best = -1000
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.cch
                        best = max(best, self.minimax(depth + 1, not isMax))
                        self.board[i][j] = ' '
            return best
        else:
            best = 1000
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.uch
                        best = min(best, self.minimax(depth + 1, not isMax))
                        self.board[i][j] = ' '
            return best


    def find_best_move(self):
        best_move = None
        best_value = -1000 if self.cch == 'X' else 1000
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = self.cch
                    move_value = self.minimax(0, False)
                    self.board[i][j] = ' '
                    
                    if self.cch == 'X':
                        if move_value > best_value:
                            best_value = move_value
                            best_move = (i, j)
                    else:
                        if move_value < best_value:
                            best_value = move_value
                            best_move = (i, j)
        return best_move


    def hard_play(self, bot, call):
        best_move = self.find_best_move()
        if best_move:
            row, col = best_move
            self.board[row][col] = self.cch
            self.evaluate()
            bot.edit_message_reply_markup(call.message.chat.id, self.message_id, reply_markup=self.edit_board())
            if not self.win:
                self.character = self.uch
                self.user_play(bot, call)
            else:
                bot.send_message(call.message.chat.id, f"{self.uch} player Wins!")
        else:
            bot.send_message(call.message.chat.id, "It's a tie!")


    def game(self, bot, call):
        send_message = bot.send_message(call.message.chat.id, "Lets play!!!", reply_markup=self.edit_board())
        self.message_id = send_message.message_id
        if self.character == self.uch:
            self.user_play(bot, call)
        elif self.level == 'easy':
            self.rand_play(bot, call)
        elif self.level == 'hard':
            self.hard_play(bot, call)
    