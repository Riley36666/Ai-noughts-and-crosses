import pygame
import sys
import math
import tkinter as tk
import threading

# --- Game Setup ---
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)

# Game state
board = [" " for _ in range(9)]
playerscore = 0
Aiscore = 0

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Noughts and Crosses AI')
screen.fill(BG_COLOR)
FONT = pygame.font.SysFont(None, 50)


scores_vars = {}

def start_score_window():
    def show_score():
        root = tk.Tk()
        root.title("Scoreboard")
        root.geometry("300x150+700+100")  # position near the game window
        player_var = tk.StringVar()
        ai_var = tk.StringVar()
        tk.Label(root, text="Scoreboard", font=("Arial", 18)).pack(pady=5)
        tk.Label(root, textvariable=player_var, font=("Arial", 16)).pack(pady=5)
        tk.Label(root, textvariable=ai_var, font=("Arial", 16)).pack(pady=5)

        root.mainloop()

    threading.Thread(target=show_score, daemon=True).start()

# Draw grid lines
def draw_lines():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Draw X and O
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            mark = board[row * 3 + col]
            if mark == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif mark == 'X':
                start_desc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
                end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (start_desc[0], end_desc[1]), (end_desc[0], start_desc[1]), CROSS_WIDTH)

# Game logic
def check_winner(brd, player):
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    return any(brd[i] == brd[j] == brd[k] == player for i,j,k in wins)

def is_draw(brd):
    return " " not in brd

def minimax(brd, is_max):
    if check_winner(brd, "O"):
        return 1
    elif check_winner(brd, "X"):
        return -1
    elif is_draw(brd):
        return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if brd[i] == " ":
                brd[i] = "O"
                val = minimax(brd, False)
                brd[i] = " "
                best = max(best, val)
        return best
    else:
        best = math.inf
        for i in range(9):
            if brd[i] == " ":
                brd[i] = "X"
                val = minimax(brd, True)
                brd[i] = " "
                best = min(best, val)
        return best

def best_move():
    best_score = -math.inf
    move = -1
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

def draw_rematch_box():
    box_width, box_height = 400, 200
    box_x = WIDTH // 2 - box_width // 2
    box_y = HEIGHT // 2 - box_height // 2
    pygame.draw.rect(screen, (250, 250, 250), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, LINE_COLOR, (box_x, box_y, box_width, box_height), 5)

    text = FONT.render("Play again?", True, (0, 0, 0))
    screen.blit(text, (box_x + 100, box_y + 30))

    pygame.draw.rect(screen, (0, 200, 0), (box_x + 50, box_y + 100, 120, 50))
    yes_text = FONT.render("Yes", True, (255, 255, 255))
    screen.blit(yes_text, (box_x + 80, box_y + 110))

    pygame.draw.rect(screen, (200, 0, 0), (box_x + 230, box_y + 100, 120, 50))
    no_text = FONT.render("No", True, (255, 255, 255))
    screen.blit(no_text, (box_x + 270, box_y + 110))

    return {
        "yes": pygame.Rect(box_x + 50, box_y + 100, 120, 50),
        "no": pygame.Rect(box_x + 230, box_y + 100, 120, 50)
    }

def restart():
    global board, game_over, player_turn
    while True:
        pygame.display.update()
        buttons = draw_rematch_box()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons["yes"].collidepoint(event.pos):
                    board = [" " for _ in range(9)]
                    screen.fill(BG_COLOR)
                    draw_lines()
                    draw_figures()
                    game_over = False
                    player_turn = True
                    return
                elif buttons["no"].collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# Start everything
draw_lines()
game_over = False
player_turn = True


start_score_window()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE
            index = clicked_row * 3 + clicked_col

            if board[index] == " " and player_turn:
                board[index] = "X"
                player_turn = False
                draw_figures()

        if not player_turn and not game_over:
            pygame.time.wait(500)
            move = best_move()
            if move != -1:
                board[move] = "O"
            draw_figures()
            player_turn = True

        if check_winner(board, "X"):
            restart()
        elif check_winner(board, "O"):
            Aiscore += 1
            restart()
        elif is_draw(board):
            restart()

    pygame.display.update()
