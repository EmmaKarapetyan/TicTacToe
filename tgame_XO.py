import random
from telebot import types

class TicTacToeGame:
    def __init__(self, uch, level):
        self.length = 3
        self.board = [[' ' for _ in range(self.length)] for _ in range(self.length)]
        self.level = level
        self.character = 'X'
        self.uch = uch
        self.cch = 'O' if uch == 'X' else 'X'
        self.message_id = None


    def end_game(self):
        if self.evaluate() != 0:
            return f"{self.character} player Wins!"
        if not any(' ' in row for row in self.board):
            return 'Finish'
        return False


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


    def rand_play(self, bot, call):
        check = True
        while check:
            index = random.randint(0, self.length * self.length - 1)
            row, col = divmod(index, self.length)
            if self.board[row][col] == ' ':
                self.board[row][col] = self.character
                self.evaluate()
                if not self.end_game():
                    self.character = self.uch
                check = False
        bot.edit_message_reply_markup(call.message.chat.id, self.message_id, reply_markup=self.edit_board())


    def user_play(self, bot, call):
        row, col = divmod(int(call.data), self.length)
        if self.board[row][col] == ' ':
            self.board[row][col] = self.uch
            bot.edit_message_reply_markup(call.message.chat.id, self.message_id, reply_markup=self.edit_board())
            self.evaluate()
            if not self.end_game():
                self.character = self.cch
                self.bot_move(bot, call)


    def bot_move(self, bot, call):
        if self.level == 'easy':
            self.rand_play(bot, call)
        elif self.level == 'hard':
            self.minimax(0, self.cch == 'O')
            row, col = self.best_move
            self.board[row][col] = self.cch
            self.evaluate()
            if not self.end_game():
                self.character = self.uch
            bot.edit_message_reply_markup(call.message.chat.id, self.message_id, reply_markup=self.edit_board())


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
                if self.board[row1][col1] == 'O':
                    return 10
                else:
                    return -10
        return 0


    def minimax(self, depth, isMax):
        score = self.evaluate()

        if score == 10:
            return score - depth
        if score == -10:
            return score + depth
        if not any(' ' in row for row in self.board):
            return 0

        if isMax:
            best = -1000
            move = None
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = 'O'
                        value = self.minimax(depth + 1, not isMax)
                        self.board[i][j] = ' '
                        if value > best:
                            best = value
                            move = (i, j)
            self.best_move = move
            return best
        else:
            best = 1000
            move = None
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = 'X'
                        value = self.minimax(depth + 1, not isMax)
                        self.board[i][j] = ' '
                        if value < best:
                            best = value
                            move = (i, j)
            self.best_move = move
            return best


    def start_game(self, bot, call):
        send_message = bot.send_message(call.message.chat.id, "Let's play!!!", reply_markup=self.edit_board())
        self.message_id = send_message.message_id
        if self.cch == 'X' :
            self.rand_play(bot, call)
            
            
            