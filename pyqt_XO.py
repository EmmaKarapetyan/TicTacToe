from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import random


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        
        self.length = 3
        self.board = []
        self.best_move = None
        self.level = 'EASY'
        self.character = 'X'
        self.uch = 'X'
        self.cch = 'O'
        self.re_level = 'EASY'
        self.re_uch = 'X'
        
        self.main_gui()

        
    def main_gui(self):
        self.setFixedSize(425, 550) 
        self.setStyleSheet("background-color: #BBD5ED")   
        self.setWindowTitle("TicTacToe")
               
        self.turn_label = QtWidgets.QLabel(self)
        self.turn_label.setText(f"       {self.character} TURN       ")
        self.turn_label.setStyleSheet("font-size: 25px; background-color: #A288E3; ")   
        self.turn_label.adjustSize()
        self.turn_label.move(int(self.width()/2) - int(self.turn_label.width()/2), int(self.height()/4*3))
        
        self.character_button = QtWidgets.QPushButton(self)
        self.character_button.setText(f"{self.re_uch}")
        self.character_button.setStyleSheet("""
                                        QPushButton{
                                            width: 100px; height: 30px; font-size: 20px; 
                                            border: 2px solid black; border-radius: 7px; background-color: #CEFDFF;   
                                        }
                                          
                                        QPushButton::hover{
                                            background-color: #A288E3;  
                                        }""")   
        self.character_button.adjustSize()
        self.character_button.move(int(self.width()/4) - int(self.character_button.width()/2), int(self.height()/4*3) + int(self.turn_label.height() * 3 / 2))
        self.character_button.clicked.connect(self.character_change)
        
        self.level_button = QtWidgets.QPushButton(self)
        self.level_button.setText(f"{self.re_level}")
        self.level_button.setStyleSheet("""
                                        QPushButton{
                                            width: 100px; height: 30px; font-size: 20px; 
                                            border: 2px solid black; border-radius: 7px; background-color: #CEFDFF;  
                                        }
                                          
                                        QPushButton::hover{
                                            background-color: #A288E3;  
                                        }""")   
        self.level_button.adjustSize()
        self.level_button.move(int(self.width() / 4 * 3) - int(self.level_button.width()/2), int(self.height()/4*3) + int(self.turn_label.height() * 3 / 2))
        self.level_button.clicked.connect(self.level_change)

        self.restart_button = QtWidgets.QPushButton(self)
        self.restart_button.setText("RESTART")
        self.restart_button.setStyleSheet("""
                                        QPushButton{
                                            width: 500px; height: 30px; font-size: 20px; 
                                            border: 2px solid black; border-radius: 7px; background-color: #CEFDFF; 
                                        }
                                          
                                        QPushButton::hover{
                                            background-color: #A288E3;  
                                        }""")   
        self.restart_button.adjustSize()
        self.restart_button.move(int(self.width() / 2) - int(self.restart_button.width()/2), self.height() - self.restart_button.height() - 10)
        self.restart_button.clicked.connect(self.restart)
        
        self.index0 = QtWidgets.QPushButton(self)
        self.index1 = QtWidgets.QPushButton(self)
        self.index2 = QtWidgets.QPushButton(self)
        self.index3 = QtWidgets.QPushButton(self)
        self.index4 = QtWidgets.QPushButton(self)
        self.index5 = QtWidgets.QPushButton(self)
        self.index6 = QtWidgets.QPushButton(self)
        self.index7 = QtWidgets.QPushButton(self)
        self.index8 = QtWidgets.QPushButton(self)

        self.index0.clicked.connect(lambda: self.user_play(self.index0))
        self.index1.clicked.connect(lambda: self.user_play(self.index1))
        self.index2.clicked.connect(lambda: self.user_play(self.index2))
        self.index3.clicked.connect(lambda: self.user_play(self.index3))
        self.index4.clicked.connect(lambda: self.user_play(self.index4))
        self.index5.clicked.connect(lambda: self.user_play(self.index5))
        self.index6.clicked.connect(lambda: self.user_play(self.index6))
        self.index7.clicked.connect(lambda: self.user_play(self.index7))
        self.index8.clicked.connect(lambda: self.user_play(self.index8))

        self.board = [
            [self.index0, self.index1, self.index2],
            [self.index3, self.index4, self.index5],
            [self.index6, self.index7, self.index8],
        ]

        i, j = 0, 0
        for line in self.board:
            for item in line:
                item.setText(' ')
                item.resize(int(self.width() / 3) - 40, int(self.height() * 3 / 12) - 40)
                item.setStyleSheet("""
                                    QPushButton{
                                        border: 2px solid black;
                                        border-radius: 17px;
                                        background-color: #CEFDFF;
                                        font-size: 25px;
                                    }
                                        
                                    QPushButton::hover{
                                        background-color: #A288E3; 
                                    }""")
                item.move(int(self.width() / 3 * (i + 1)) - 70 - int(item.width() / 2), int(self.height() / 4 * j) + 10)
                j += 1
            i += 1
            j = 0
            
        if self.cch == 'X':
            self.rand_play()
            
        
    def character_change(self):
        self.re_uch = 'X' if self.re_uch == 'O' else 'O'
        self.character_button.setText(f"{self.re_uch}")


    def level_change(self):
        self.re_level = 'HARD' if self.re_level == 'EASY' else "EASY"
        self.level_button.setText(f"{self.re_level}")


    def restart(self):
        self.level = self.re_level
        self.uch = self.re_uch
        self.cch = 'O' if self.uch == 'X' else 'X'
        self.character = 'X'
        self.turn_label.setText(f"       {self.character} TURN       ")
        for line in self.board:
            for item in line:
                item.setText(' ')
        if self.cch == 'X':
            self.rand_play()


    def end_game(self):
        if self.evaluate() != 0:
            self.turn_label.setText(f"  {self.character} player Wins!  ")
            return True
        for row in self.board:
            for col in row:
                if col.text() == ' ':
                    return False
        self.turn_label.setText('       Finish       ')
        return True
        
    
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
            if self.board[row1][col1].text() == self.board[row2][col2].text() == self.board[row3][col3].text() != ' ':
                if self.board[row1][col1].text() == 'O':
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
        if all(col.text() != ' ' for row in self.board for col in row):
            return 0

        if isMax:
            best = -1000
            move = None
            for i in range(3):
                for j in range(3):
                    if self.board[i][j].text() == ' ':
                        self.board[i][j].setText('O')
                        value = self.minimax(depth + 1, not isMax)
                        self.board[i][j].setText(' ')
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
                    if self.board[i][j].text() == ' ':
                        self.board[i][j].setText('X')
                        value = self.minimax(depth + 1, not isMax)
                        self.board[i][j].setText(' ')
                        if value < best:
                            best = value
                            move = (i, j)
            self.best_move = move
            return best


    def c_move(self):
        self.minimax(0, self.cch == 'O')
        if self.best_move:
            row, col = self.best_move
            self.board[row][col].setText(self.cch)
            self.evaluate()
            if not self.end_game():
                self.character = self.uch
                self.user_play(None)

    
    def rand_play(self):
        check = not self.end_game()
        if check:
            while check:
                index = random.randint(0, self.length * self.length - 1)
                row, col = divmod(index, self.length)
                if self.board[row][col].text() == ' ':
                    self.board[row][col].setText(f'{self.cch}')
                    if not self.end_game():
                        self.character = self.uch
                        self.turn_label.setText(f"       {self.character} TURN       ")
                    check = False
            self.user_play(None)

    
    def user_play(self, index):
        if (index and index.text() == ' ' and self.uch == self.character) and not self.end_game():
            index.setText(f'{self.uch}')
            if not self.end_game():
                self.character = self.cch
                self.turn_label.setText(f"       {self.character} TURN       ")
                if self.level == 'EASY':
                    self.rand_play()
                else:
                    self.c_move()


app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec_())