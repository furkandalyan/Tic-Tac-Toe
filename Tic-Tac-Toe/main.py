import random
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import csv
import datetime
import sys

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def initialize_board():
    return [[" " for _ in range(3)] for _ in range(3)]

def get_move(player):
    while True:
        try:
            row = int(input(f"Player {player}, enter row (0-2): "))
            col = int(input(f"Player {player}, enter col (0-2): "))
            if 0 <= row <= 2 and 0 <= col <= 2:
                return row, col
            else:
                print("Invalid input. Please enter numbers between 0 and 2.")
        except ValueError:
            print("Please enter valid numbers.")

def is_valid_move(board, row, col):
    return board[row][col] == " "

def make_move(board, row, col, player):
    board[row][col] = player

def check_winner(board):
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]

    return None

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

class TicTacToe:
    def __init__(self, ai_player=None, human_player=None):
        self.board = self.initialize_board()
        self.current_player = "X"
        self.ai_player = ai_player  # 'X' or 'O' or None
        self.human_player = human_player  # 'X' or 'O' or None
        self.winning_cells = []

    def initialize_board(self):
        return [[" " for _ in range(3)] for _ in range(3)]

    def print_board(self):
        for row in self.board:
            print(" | ".join(row))
            print("-" * 5)

    def is_valid_move(self, row, col):
        return self.board[row][col] == " "

    def make_move(self, row, col, player):
        self.board[row][col] = player

    def check_winner(self):
        # Check rows and columns
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != " ":
                self.winning_cells = [(i, 0), (i, 1), (i, 2)]
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != " ":
                self.winning_cells = [(0, i), (1, i), (2, i)]
                return self.board[0][i]
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            self.winning_cells = [(0, 0), (1, 1), (2, 2)]
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            self.winning_cells = [(0, 2), (1, 1), (2, 0)]
            return self.board[0][2]
        self.winning_cells = []
        return None

    def is_draw(self):
        return all(cell != " " for row in self.board for cell in row)

    def reset(self):
        self.board = self.initialize_board()
        self.current_player = "X"
        self.winning_cells = []

    def get_available_moves(self):
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == " "]

    def minimax(self, is_maximizing, player, opponent):
        winner = self.check_winner()
        if winner == player:
            return 1, None
        elif winner == opponent:
            return -1, None
        elif self.is_draw():
            return 0, None

        best_move = None
        if is_maximizing:
            best_score = -float('inf')
            for r, c in self.get_available_moves():
                self.board[r][c] = player
                score, _ = self.minimax(False, player, opponent)
                self.board[r][c] = " "
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
            return best_score, best_move
        else:
            best_score = float('inf')
            for r, c in self.get_available_moves():
                self.board[r][c] = opponent
                score, _ = self.minimax(True, player, opponent)
                self.board[r][c] = " "
                if score < best_score:
                    best_score = score
                    best_move = (r, c)
            return best_score, best_move

    def ai_move(self):
        if self.ai_player:
            _, move = self.minimax(True, self.ai_player, self.human_player)
            if move:
                row, col = move
                self.make_move(row, col, self.ai_player)
                return row, col
        return None, None

# CLI and GUI logic will use this class

def cli_game():
    print("Welcome to Tic-Tac-Toe!")
    mode = input("Play vs (1) Human or (2) AI? Enter 1 or 2: ")
    if mode == "2":
        human = input("Do you want to be X or O? (X goes first): ").upper()
        ai = "O" if human == "X" else "X"
        game = TicTacToe(ai_player=ai, human_player=human)
    else:
        game = TicTacToe()

    while True:
        game.reset()
        while True:
            game.print_board()
            if game.ai_player and game.current_player == game.ai_player:
                print(f"AI ({game.ai_player}) is making a move...")
                game.ai_move()
            else:
                while True:
                    try:
                        row = int(input(f"Player {game.current_player}, enter row (0-2): "))
                        col = int(input(f"Player {game.current_player}, enter col (0-2): "))
                        if 0 <= row <= 2 and 0 <= col <= 2 and game.is_valid_move(row, col):
                            game.make_move(row, col, game.current_player)
                            break
                        else:
                            print("Invalid move. Try again.")
                    except ValueError:
                        print("Please enter valid numbers.")
            winner = game.check_winner()
            if winner:
                game.print_board()
                print(f"Player {winner} wins!")
                break
            elif game.is_draw():
                game.print_board()
                print("It's a draw!")
                break
            game.current_player = "O" if game.current_player == "X" else "X"
        again = input("Play again? (y/n): ").lower()
        if again != "y":
            break

# GUI implementation with tkinter
def gui_game():
    class TicTacToeGUI:
        def __init__(self, root):
            self.root = root
            self.root.title("Tic-Tac-Toe App")
            self.root.geometry("500x600")
            self.root.minsize(400, 500)
            self.root.resizable(True, True)
            self.is_fullscreen = False
            self.theme = "peace"
            self.themes = {
                "peace": {
                    "bg": "#e3f6f5",
                    "frame_bg": "#e3f6f5",
                    "button_bg": "#bae8e8",
                    "button_fg": "#272343",
                    "active_bg": "#ffd803",
                    "active_fg": "#272343",
                    "score_bg": "#e3f6f5",
                    "status_bg": "#e3f6f5",
                    "x_fg": "#3a86ff",
                    "o_fg": "#ff006e",
                    "win_bg": "#b9fbc0",
                },
                "dark": {
                    "bg": "#222831",
                    "frame_bg": "#222831",
                    "button_bg": "#393E46",
                    "button_fg": "#EEEEEE",
                    "active_bg": "#00ADB5",
                    "active_fg": "#222831",
                    "score_bg": "#f0f0f0",
                    "status_bg": "#f0f0f0",
                    "x_fg": "#2196F3",
                    "o_fg": "#F44336",
                    "win_bg": "#4CAF50",
                },
                "light": {
                    "bg": "#f0f0f0",
                    "frame_bg": "#f0f0f0",
                    "button_bg": "#FFFFFF",
                    "button_fg": "#222831",
                    "active_bg": "#B3E5FC",
                    "active_fg": "#222831",
                    "score_bg": "#222831",
                    "status_bg": "#222831",
                    "x_fg": "#1976D2",
                    "o_fg": "#D32F2F",
                    "win_bg": "#81C784",
                }
            }
            self.set_modern_style()
            self.mode = None
            self.ai_player = None
            self.human_player = None
            self.ai_difficulty = "Unbeatable"  # Default
            self.game = TicTacToe()  # Always have a game instance
            self.buttons = []
            self.status_label = None
            self.scores = {"X": 0, "O": 0, "Draw": 0}
            self.score_label = None
            self.game_results = []  # For CSV export
            # Load icons if available
            try:
                self.x_icon = tk.PhotoImage(file="x_icon.png")
            except Exception:
                self.x_icon = None
            try:
                self.o_icon = tk.PhotoImage(file="o_icon.png")
            except Exception:
                self.o_icon = None
            try:
                self.logo_icon = tk.PhotoImage(file="logo.png")
                self.root.iconphoto(False, self.logo_icon)
            except Exception:
                self.logo_icon = None
            self.create_menu()
            self.show_welcome_screen()

        def set_modern_style(self):
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('TButton', font=('Segoe UI', 16), padding=10, borderwidth=0, relief='flat')
            style.configure('TLabel', font=('Segoe UI', 14), background=self.themes[self.theme]['bg'], foreground=self.themes[self.theme]['button_fg'])
            style.map('TButton', background=[('active', self.themes[self.theme]['active_bg'])])

        def toggle_fullscreen(self):
            self.is_fullscreen = not self.is_fullscreen
            self.root.attributes("-fullscreen", self.is_fullscreen)

        def get_theme(self, key):
            return self.themes[self.theme][key]

        def toggle_theme(self):
            self.theme = "light" if self.theme == "dark" else "dark"
            self.redraw_current_screen()

        def redraw_current_screen(self):
            # Redraws the current screen with the new theme
            if hasattr(self, 'current_screen'):
                self.current_screen()
            else:
                self.show_welcome_screen()

        def create_menu(self):
            menubar = tk.Menu(self.root)
            game_menu = tk.Menu(menubar, tearoff=0)
            game_menu.add_command(label="New Game", command=self.show_welcome_screen)
            game_menu.add_command(label="Export Results to CSV", command=self.export_results_to_csv)
            game_menu.add_command(label="Toggle Fullscreen", command=self.toggle_fullscreen)
            game_menu.add_separator()
            game_menu.add_command(label="Exit", command=self.root.quit)
            menubar.add_cascade(label="Game", menu=game_menu)
            view_menu = tk.Menu(menubar, tearoff=0)
            view_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
            menubar.add_cascade(label="View", menu=view_menu)
            help_menu = tk.Menu(menubar, tearoff=0)
            help_menu.add_command(label="About", command=self.show_about)
            menubar.add_cascade(label="Help", menu=help_menu)
            # Add logo to menu if available
            if getattr(self, 'logo_icon', None) is not None and self.logo_icon is not None:
                menubar.add_command(image=self.logo_icon, compound="left")
            self.root.config(menu=menubar)

        def show_about(self):
            messagebox.showinfo("About", "Tic-Tac-Toe App\nMade with Tkinter\nEnjoy!")

        def show_welcome_screen(self):
            self.clear_window()
            self.current_screen = self.show_welcome_screen
            frame = ttk.Frame(self.root, style='TFrame')
            frame.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
            label = ttk.Label(frame, text="Welcome to Tic-Tac-Toe!", font=("Segoe UI", 24, "bold"), anchor="center")
            label.pack(pady=30)
            btn_human = ttk.Button(frame, text="Play vs Human", command=self.start_human)
            btn_ai = ttk.Button(frame, text="Play vs AI", command=self.setup_ai_selection)
            btn_human.pack(pady=15, ipadx=10, ipady=5, fill='x')
            btn_ai.pack(pady=15, ipadx=10, ipady=5, fill='x')

        def setup_mode_selection(self):
            self.show_welcome_screen()

        def setup_ai_selection(self):
            self.clear_window()
            self.current_screen = self.setup_ai_selection
            frame = ttk.Frame(self.root, style='TFrame')
            frame.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
            label = ttk.Label(frame, text="Do you want to be X or O? (X goes first)", font=("Segoe UI", 16), anchor="center")
            label.pack(pady=20)
            btn_x = ttk.Button(frame, text="X", command=lambda: self.setup_ai_difficulty("X"))
            btn_o = ttk.Button(frame, text="O", command=lambda: self.setup_ai_difficulty("O"))
            btn_x.pack(pady=15, ipadx=10, ipady=5, fill='x')
            btn_o.pack(pady=15, ipadx=10, ipady=5, fill='x')

        def setup_ai_difficulty(self, human):
            self.clear_window()
            self.current_screen = lambda: self.setup_ai_difficulty(human)
            frame = ttk.Frame(self.root, style='TFrame')
            frame.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
            label = ttk.Label(frame, text="Select AI Difficulty", font=("Segoe UI", 16), anchor="center")
            label.pack(pady=20)
            btn_easy = ttk.Button(frame, text="Easy", command=lambda: self.start_ai(human, "Easy"))
            btn_unbeatable = ttk.Button(frame, text="Unbeatable", command=lambda: self.start_ai(human, "Unbeatable"))
            btn_easy.pack(pady=15, ipadx=10, ipady=5, fill='x')
            btn_unbeatable.pack(pady=15, ipadx=10, ipady=5, fill='x')

        def start_human(self):
            self.game = TicTacToe()
            self.current_screen = self.draw_board
            self.draw_board()

        def start_ai(self, human, difficulty):
            ai = "O" if human == "X" else "X"
            self.ai_difficulty = difficulty
            self.game = TicTacToe(ai_player=ai, human_player=human)
            self.current_screen = lambda: self.draw_board()
            self.draw_board()
            if self.game.current_player == self.game.ai_player:
                self.root.after(500, self.ai_move)

        def draw_board(self):
            self.clear_window()
            self.current_screen = self.draw_board
            # Board canvas settings
            board_size = min(self.root.winfo_width(), self.root.winfo_height() - 200)
            board_size = max(board_size, 300)
            self.board_size = board_size = 420  # Fixed for now, can be dynamic
            self.cell_size = cell_size = board_size // 3
            canvas_frame = ttk.Frame(self.root, style='TFrame')
            canvas_frame.pack(expand=True, fill=tk.BOTH, padx=0, pady=0)
            self.board_canvas = tk.Canvas(canvas_frame, width=board_size, height=board_size, bg="white", highlightthickness=0)
            self.board_canvas.pack(pady=10)
            self.board_canvas.bind("<Button-1>", self.on_canvas_click)
            self.draw_grid()
            self.draw_symbols()
            # Score label
            self.score_label = ttk.Label(self.root, text=self.get_score_text(), font=("Segoe UI", 14, "bold"), anchor="center")
            self.score_label.pack(pady=10)
            self.status_label = ttk.Label(self.root, text=f"Player {self.game.current_player}'s turn", font=("Segoe UI", 16), anchor="center")
            self.status_label.pack(pady=10)
            # Add logo to the top left if available
            if getattr(self, 'logo_icon', None) is not None and self.logo_icon is not None:
                logo_label = ttk.Label(self.root, image=self.logo_icon)
                logo_label.place(x=10, y=10)
            self.canvas_symbols = [[None for _ in range(3)] for _ in range(3)]
            self.canvas_win_highlights = []

        def draw_grid(self):
            size = self.board_size
            cell = self.cell_size
            self.board_canvas.delete("grid")
            for i in range(1, 3):
                # Vertical lines
                self.board_canvas.create_line(i*cell, 0, i*cell, size, fill="black", width=4, tags="grid")
                # Horizontal lines
                self.board_canvas.create_line(0, i*cell, size, i*cell, fill="black", width=4, tags="grid")

        def draw_symbols(self):
            self.board_canvas.delete("symbol")
            for r in range(3):
                for c in range(3):
                    x = c * self.cell_size + self.cell_size // 2
                    y = r * self.cell_size + self.cell_size // 2
                    symbol = self.game.board[r][c]
                    if symbol == "X" and self.x_icon:
                        self.board_canvas.create_image(x, y, image=self.x_icon, tags="symbol")
                    elif symbol == "O" and self.o_icon:
                        self.board_canvas.create_image(x, y, image=self.o_icon, tags="symbol")
                    elif symbol == "X":
                        self.board_canvas.create_text(x, y, text="X", font=("Segoe UI", 48, "bold"), fill=self.get_theme("x_fg"), tags="symbol")
                    elif symbol == "O":
                        self.board_canvas.create_text(x, y, text="O", font=("Segoe UI", 48, "bold"), fill=self.get_theme("o_fg"), tags="symbol")

        def on_canvas_click(self, event):
            col = event.x // self.cell_size
            row = event.y // self.cell_size
            if 0 <= row < 3 and 0 <= col < 3:
                self.on_click(row, col)

        def get_score_text(self):
            return f"X: {self.scores['X']}    O: {self.scores['O']}    Draws: {self.scores['Draw']}"

        def update_score_label(self):
            if self.score_label is not None:
                self.score_label.config(text=self.get_score_text())

        def update_board(self):
            self.draw_symbols()
            self.board_canvas.delete("win")
            if self.game.winning_cells:
                for (r, c) in self.game.winning_cells:
                    x0 = c * self.cell_size + 8
                    y0 = r * self.cell_size + 8
                    x1 = (c+1) * self.cell_size - 8
                    y1 = (r+1) * self.cell_size - 8
                    self.board_canvas.create_rectangle(x0, y0, x1, y1, outline="#b9fbc0", width=8, tags="win")

        def on_click(self, row, col):
            if self.game.board[row][col] != " " or (self.game.ai_player and self.game.current_player == self.game.ai_player):
                return
            self.game.make_move(row, col, self.game.current_player)
            self.update_board()
            winner = self.game.check_winner()
            if winner:
                if self.status_label is not None:
                    self.status_label.config(text=f"Player {winner} wins!")
                self.show_game_over(f"Player {winner} wins!")
                return
            elif self.game.is_draw():
                if self.status_label is not None:
                    self.status_label.config(text="It's a draw!")
                self.show_game_over("It's a draw!")
                return
            self.game.current_player = "O" if self.game.current_player == "X" else "X"
            if self.status_label is not None:
                self.status_label.config(text=f"Player {self.game.current_player}'s turn")
            if self.game.ai_player and self.game.current_player == self.game.ai_player:
                self.root.after(500, self.ai_move)

        def ai_move(self):
            if self.ai_difficulty == "Easy":
                moves = self.game.get_available_moves()
                if moves:
                    row, col = random.choice(moves)
                    self.game.make_move(row, col, self.game.ai_player)
            else:
                self.game.ai_move()
            self.update_board()
            winner = self.game.check_winner()
            if winner:
                if self.status_label is not None:
                    self.status_label.config(text=f"Player {winner} wins!")
                self.show_game_over(f"Player {winner} wins!")
                return
            elif self.game.is_draw():
                if self.status_label is not None:
                    self.status_label.config(text="It's a draw!")
                self.show_game_over("It's a draw!")
                return
            self.game.current_player = "O" if self.game.current_player == "X" else "X"
            if self.status_label is not None:
                self.status_label.config(text=f"Player {self.game.current_player}'s turn")

        def show_game_over(self, message):
            # Update scores
            if "Player X wins" in message:
                self.scores["X"] += 1
                winner = "X"
            elif "Player O wins" in message:
                self.scores["O"] += 1
                winner = "O"
            elif "draw" in message.lower():
                self.scores["Draw"] += 1
                winner = "Draw"
            else:
                winner = "Unknown"
            # Record game result
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            difficulty = self.ai_difficulty if self.game.ai_player else "N/A"
            self.game_results.append({
                "Time": now,
                "Winner": winner,
                "Difficulty": difficulty
            })
            self.update_score_label()
            self.update_board()  # Ensure highlight is shown
            if winner in ("X", "O"):
                self.celebrate_win(self.game.winning_cells)
            result = messagebox.askquestion("Game Over", f"{message}\n\nDo you want to play again?", icon='info')
            if result == 'yes':
                self.show_welcome_screen()
            else:
                self.root.quit()

        def end_game(self, message):
            # Deprecated, replaced by show_game_over
            self.show_game_over(message)

        def clear_window(self):
            for widget in self.root.winfo_children():
                widget.destroy()

        def export_results_to_csv(self):
            if not self.game_results:
                messagebox.showinfo("Export Results", "No game results to export yet.")
                return
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Save Game Results As..."
            )
            if not file_path:
                return
            try:
                with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
                    fieldnames = ["Time", "Winner", "Difficulty"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in self.game_results:
                        writer.writerow(row)
                messagebox.showinfo("Export Results", f"Results exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export results:\n{e}")

        def celebrate_win(self, cells):
            # Simple color pulse animation for winning cells
            colors = ["#fff3b0", "#f9c74f", "#b9fbc0", self.get_theme("win_bg")]
            def pulse(step=0):
                color = colors[step % len(colors)]
                self.board_canvas.delete("win")
                for (r, c) in cells:
                    x0 = c * self.cell_size + 8
                    y0 = r * self.cell_size + 8
                    x1 = (c+1) * self.cell_size - 8
                    y1 = (r+1) * self.cell_size - 8
                    self.board_canvas.create_rectangle(x0, y0, x1, y1, outline=color, width=8, tags="win")
                if step < 8:
                    self.root.after(120, lambda: pulse(step+1))
            pulse()

    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    print("Choose interface:")
    print("1. CLI (console)")
    print("2. Tkinter GUI (desktop)")
    mode = input("Enter 1 or 2: ")
    if mode == "2":
        gui_game()
    else:
        cli_game()
