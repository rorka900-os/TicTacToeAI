from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                                QGridLayout, QPushButton, QVBoxLayout, 
                                QHBoxLayout, QLabel, QMessageBox, QComboBox,
                                QSizePolicy, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QTimer, QSize, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QFont, QColor, QPalette
import sys


class TicTacToeAI:
    
    def __init__(self, difficulty='hard'):
        self.difficulty = difficulty
    
    def minimax(self, board, depth, is_maximizing, alpha, beta):
        winner = self.check_winner(board)
        
        if winner == 'O':
            return 10 - depth
        elif winner == 'X':
            return depth - 10
        elif self.is_board_full(board):
            return 0
        
        if is_maximizing:
            max_eval = -float('inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = 'O'
                    eval = self.minimax(board, depth + 1, False, alpha, beta)
                    board[i] = ''
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = 'X'
                    eval = self.minimax(board, depth + 1, True, alpha, beta)
                    board[i] = ''
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval
    
    def get_best_move(self, board):
        if self.difficulty == 'easy':
            import random
            available = [i for i in range(9) if board[i] == '']
            return random.choice(available) if available else None
        
        elif self.difficulty == 'medium':
            import random
            if random.random() < 0.5:
                available = [i for i in range(9) if board[i] == '']
                return random.choice(available) if available else None
        
        best_score = -float('inf')
        best_move = None
        
        for i in range(9):
            if board[i] == '':
                board[i] = 'O'
                score = self.minimax(board, 0, False, -float('inf'), float('inf'))
                board[i] = ''
                
                if score > best_score:
                    best_score = score
                    best_move = i
        
        return best_move
    
    def check_winner(self, board):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        
        for combo in winning_combinations:
            if (board[combo[0]] == board[combo[1]] == board[combo[2]] 
                and board[combo[0]] != ''):
                return board[combo[0]]
        return None
    
    def is_board_full(self, board):
        return '' not in board


class MaterialButton(QPushButton):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumSize(80, 80)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCursor(Qt.PointingHandCursor)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        self.reset_style()
    
    def reset_style(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #E8DEF8;
                color: #1C1B1F;
                border: none;
                border-radius: 16px;
                font-size: 48px;
                font-weight: bold;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
            }
            QPushButton:hover {
                background-color: #D0BCFF;
            }
            QPushButton:pressed {
                background-color: #B69DF8;
            }
        """)
    
    def set_x_style(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #6750A4;
                color: #FFFFFF;
                border: none;
                border-radius: 16px;
                font-size: 48px;
                font-weight: bold;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
            }
        """)
    
    def set_o_style(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #D0BCFF;
                color: #381E72;
                border: none;
                border-radius: 16px;
                font-size: 48px;
                font-weight: bold;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
            }
        """)


class TicTacToeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Крестики-нолики с ИИ | Material Design 3")
        self.setMinimumSize(450, 600)
        self.resize(500, 700)
        
        self.apply_material_theme()
        
        self.board = [''] * 9
        self.current_player = 'X'
        self.game_over = False
        self.ai = TicTacToeAI(difficulty='hard')
        self.scores = {'X': 0, 'O': 0, 'Draw': 0}
        
        self.init_ui()
    
    def apply_material_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FEF7FF;
            }
            QWidget {
                background-color: #FEF7FF;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
            }
        """)
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(24)
        main_layout.setContentsMargins(24, 24, 24, 24)
        
        title_label = QLabel("Крестики-нолики")
        title_label.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title_label.setStyleSheet("color: #1C1B1F; margin-bottom: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        info_widget = QWidget()
        info_widget.setStyleSheet("""
            QWidget {
                background-color: #E8DEF8;
                border-radius: 20px;
                padding: 16px;
            }
        """)
        info_layout = QVBoxLayout(info_widget)
        info_layout.setSpacing(8)
        
        self.status_label = QLabel("Ваш ход (X)")
        self.status_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.status_label.setStyleSheet("color: #381E72; background: transparent;")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        self.score_label = QLabel("X: 0  |  O: 0  |  Ничья: 0")
        self.score_label.setFont(QFont("Segoe UI", 14))
        self.score_label.setStyleSheet("color: #49454F; background: transparent;")
        self.score_label.setAlignment(Qt.AlignCenter)
        
        info_layout.addWidget(self.status_label)
        info_layout.addWidget(self.score_label)
        main_layout.addWidget(info_widget)
        
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(12)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        self.buttons = []
        for i in range(9):
            btn = MaterialButton()
            btn.clicked.connect(lambda checked, idx=i: self.make_move(idx))
            self.buttons.append(btn)
            grid_layout.addWidget(btn, i // 3, i % 3)
        
        main_layout.addWidget(grid_widget, 1)
        
        control_widget = QWidget()
        control_layout = QHBoxLayout(control_widget)
        control_layout.setSpacing(12)
        
        reset_btn = QPushButton("Новая игра")
        reset_btn.setFont(QFont("Segoe UI", 14, QFont.DemiBold))
        reset_btn.setCursor(Qt.PointingHandCursor)
        reset_btn.setMinimumHeight(48)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #6750A4;
                color: white;
                border: none;
                border-radius: 24px;
                padding: 12px 24px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #7965AF;
            }
            QPushButton:pressed {
                background-color: #5A3F9A;
            }
        """)
        reset_btn.clicked.connect(self.reset_game)
        
        reset_shadow = QGraphicsDropShadowEffect(reset_btn)
        reset_shadow.setBlurRadius(12)
        reset_shadow.setColor(QColor(0, 0, 0, 40))
        reset_shadow.setOffset(0, 2)
        reset_btn.setGraphicsEffect(reset_shadow)
        
        difficulty_label = QLabel("Сложность:")
        difficulty_label.setFont(QFont("Segoe UI", 12))
        difficulty_label.setStyleSheet("color: #49454F;")
        
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Легко", "Средне", "Сложно"])
        self.difficulty_combo.setCurrentIndex(2)
        self.difficulty_combo.setFont(QFont("Segoe UI", 13))
        self.difficulty_combo.setCursor(Qt.PointingHandCursor)
        self.difficulty_combo.setMinimumHeight(48)
        self.difficulty_combo.setStyleSheet("""
            QComboBox {
                background-color: #E8DEF8;
                color: #1C1B1F;
                border: 2px solid #79747E;
                border-radius: 12px;
                padding: 8px 16px;
                min-width: 120px;
            }
            QComboBox:hover {
                border-color: #6750A4;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid #49454F;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: #FEF7FF;
                border: 2px solid #79747E;
                border-radius: 12px;
                selection-background-color: #E8DEF8;
                selection-color: #1C1B1F;
                padding: 4px;
            }
        """)
        self.difficulty_combo.currentIndexChanged.connect(self.change_difficulty)
        
        control_layout.addWidget(reset_btn, 2)
        control_layout.addWidget(difficulty_label)
        control_layout.addWidget(self.difficulty_combo, 1)
        
        main_layout.addWidget(control_widget)
    
    def make_move(self, index):
        if self.game_over or self.board[index] != '' or self.current_player != 'X':
            return
        
        self.board[index] = 'X'
        self.buttons[index].setText('X')
        self.buttons[index].set_x_style()
        
        if self.check_game_end():
            return
        
        self.current_player = 'O'
        self.status_label.setText("Ход компьютера...")
        
        QTimer.singleShot(500, self.ai_move)
    
    def ai_move(self):
        if self.game_over:
            return
        
        move = self.ai.get_best_move(self.board)
        if move is not None:
            self.board[move] = 'O'
            self.buttons[move].setText('O')
            self.buttons[move].set_o_style()
            
            if not self.check_game_end():
                self.current_player = 'X'
                self.status_label.setText("Ваш ход (X)")
    
    def check_game_end(self):
        winner = self.ai.check_winner(self.board)
        
        if winner:
            self.game_over = True
            self.scores[winner] += 1
            self.update_score_label()
            
            if winner == 'X':
                self.show_result('🎉 Вы победили!', 'Поздравляем! Вы выиграли!')
            else:
                self.show_result('🤖 Компьютер победил', 'К сожалению, вы проиграли.')
            return True
        
        elif self.ai.is_board_full(self.board):
            self.game_over = True
            self.scores['Draw'] += 1
            self.update_score_label()
            self.show_result('🤝 Ничья!', 'Игра закончилась вничью.')
            return True
        
        return False
    
    def show_result(self, title, message):
        self.status_label.setText(title)
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Игра окончена")
        msg_box.setText(title)
        msg_box.setInformativeText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #FEF7FF;
            }
            QPushButton {
                background-color: #6750A4;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 8px 20px;
                min-width: 80px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #7965AF;
            }
        """)
        msg_box.exec()
    
    def reset_game(self):
        self.board = [''] * 9
        self.current_player = 'X'
        self.game_over = False
        self.status_label.setText("Ваш ход (X)")
        
        for btn in self.buttons:
            btn.setText('')
            btn.reset_style()
    
    def change_difficulty(self, index):
        difficulties = ['easy', 'medium', 'hard']
        self.ai.difficulty = difficulties[index]
        self.reset_game()
    
    def update_score_label(self):
        self.score_label.setText(f"X: {self.scores['X']}  |  O: {self.scores['O']}  |  Ничья: {self.scores['Draw']}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    app.setFont(QFont("Segoe UI", 10))
    
    window = TicTacToeWindow()
    window.show()
    sys.exit(app.exec())
