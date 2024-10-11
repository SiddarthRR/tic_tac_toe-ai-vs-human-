import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic Tac Toe")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)
blue = (70, 130, 180)
red = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 80)
small_font = pygame.font.Font(None, 50)

# Game variables
board = [['', '', ''], ['', '', ''], ['', '', '']]
player = 'X'
game_over = False
difficulty = 'medium'  # Default difficulty

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_board():
    screen.fill(white)
    start_x = (width - 600) // 2
    start_y = (height - 600) // 2

    for i in range(3):
        for j in range(3):
            pygame.draw.rect(screen, black, (start_x + j * 200, start_y + i * 200, 200, 200), 2)
            if board[i][j] == 'X':
                pygame.draw.line(screen, black, (start_x + j * 200 + 30, start_y + i * 200 + 30), (start_x + j * 200 + 170, start_y + i * 200 + 170), 5)
                pygame.draw.line(screen, black, (start_x + j * 200 + 30, start_y + i * 200 + 170), (start_x + j * 200 + 170, start_y + i * 200 + 30), 5)
            elif board[i][j] == 'O':
                pygame.draw.circle(screen, black, (start_x + j * 200 + 100, start_y + i * 200 + 100), 70, 5)

def check_win(player):
    for i in range(3):
        if all([cell == player for cell in board[i]]):  # Check rows
            return True
        if all([board[j][i] == player for j in range(3)]):  # Check columns
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:  # Check diagonal
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:  # Check other diagonal
        return True
    return False

def check_tie():
    return all(cell != '' for row in board for cell in row)

def minimax(board, depth, is_maximizing):
    if check_win('O'):
        return 1
    if check_win('X'):
        return -1
    if check_tie():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ''
                    best_score = min(score, best_score)
        return best_score

def ai_move():
    global player
    if difficulty == 'easy':
        random_move()
    else:
        best_score = -float('inf')
        move = None

        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    score = minimax(board, 0, False)
                    board[i][j] = ''
                    if score > best_score:
                        best_score = score
                        move = (i, j)

        if move:
            board[move[0]][move[1]] = 'O'

def random_move():
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = 'O'

def animate_symbol(symbol, row, col):
    if symbol == 'X':
        for i in range(0, 101, 5):
            pygame.draw.line(screen, black, (col * 200 + 70, row * 200 + 70), (col * 200 + 70 + i, row * 200 + 70 + i), 5)
            pygame.draw.line(screen, black, (col * 200 + 70, row * 200 + 170), (col * 200 + 70 + i, row * 200 + 170 - i), 5)
            pygame.display.flip()
            pygame.time.delay(10)
    elif symbol == 'O':
        for i in range(0, 71, 5):
            pygame.draw.circle(screen, black, (col * 200 + 150, row * 200 + 150), i, 5)
            pygame.display.flip()
            pygame.time.delay(10)

def animate_win(winner):
    winning_cells = []
    if winner == 'X':
        for i in range(3):
            if all([cell == 'X' for cell in board[i]]):
                winning_cells = [(i, j) for j in range(3)]
                break
            if all([board[j][i] == 'X' for j in range(3)]):
                winning_cells = [(j, i) for j in range(3)]
                break
        if board[0][0] == board[1][1] == board[2][2] == 'X':
            winning_cells = [(i, i) for i in range(3)]
        if board[0][2] == board[1][1] == board[2][0] == 'X':
            winning_cells = [(i, 2 - i) for i in range(3)]
    else:  # For 'O'
        for i in range(3):
            if all([cell == 'O' for cell in board[i]]):
                winning_cells = [(i, j) for j in range(3)]
                break
            if all([board[j][i] == 'O' for j in range(3)]):
                winning_cells = [(j, i) for j in range(3)]
                break
        if board[0][0] == board[1][1] == board[2][2] == 'O':
            winning_cells = [(i, i) for i in range(3)]
        if board[0][2] == board[1][1] == board[2][0] == 'O':
            winning_cells = [(i, 2 - i) for i in range(3)]

    for _ in range(3):  # Flashing effect
        for cell in winning_cells:
            row, col = cell
            pygame.draw.rect(screen, red, ((col * 200 + (width - 600) // 2), (row * 200 + (height - 600) // 2), 200, 200), 0)
        pygame.display.flip()
        pygame.time.delay(200)
        draw_board()  # Redraw the board
        pygame.display.flip()
        pygame.time.delay(200)

def display_end_message(message):
    screen.fill(white)
    draw_text(message, font, black, screen, width // 2, height // 2 - 50)
    draw_text("Press -R- to Restart", small_font, red, screen, width // 2, height // 2 + 50)
    draw_text("Press -M- for Main Menu", small_font, blue, screen, width // 2, height // 2 + 100)
    pygame.display.flip()

def reset_game():
    global board, player, game_over
    board = [['', '', ''], ['', '', ''], ['', '', '']]
    player = 'X'
    game_over = False

def welcome_screen():
    screen.fill(white)
    draw_text("Tic Tac Toe", font, black, screen, width // 2, height // 2 - 50)
    draw_text("Select Difficulty:", small_font, black, screen, width // 2, height // 2 + 50)
    draw_text("1: Easy", small_font, black, screen, width // 2, height // 2 + 100)
    draw_text("2: Medium", small_font, black, screen, width // 2, height // 2 + 150)
    draw_text("3: Hard", small_font, black, screen, width // 2, height // 2 + 200)
    pygame.display.flip()

def main_menu():
    global difficulty
    welcome_screen()
    selecting_difficulty = True
    while selecting_difficulty:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = 'easy'
                    selecting_difficulty = False
                elif event.key == pygame.K_2:
                    difficulty = 'medium'
                    selecting_difficulty = False
                elif event.key == pygame.K_3:
                    difficulty = 'hard'
                    selecting_difficulty = False
    reset_game()
    game_loop()

def game_loop():
    global game_over
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX, mouseY = event.pos
                start_x = (width - 600) // 2
                start_y = (height - 600) // 2
                col = (mouseX - start_x) // 200
                row = (mouseY - start_y) // 200

                if 0 <= col < 3 and 0 <= row < 3 and board[row][col] == '':
                    board[row][col] = 'X'
                    animate_symbol('X', row, col)
                    if check_win('X'):
                        game_over = True
                        animate_win('X')
                        display_end_message("It was easy mode i guess!")
                    elif check_tie():
                        game_over = True
                        display_end_message("Tough fight!")
                    else:
                        ai_move()
                        if check_win('O'):
                            game_over = True
                            animate_win('O')
                            display_end_message("Wanna try again!")
                        elif check_tie():
                            game_over = True
                            display_end_message("tough fight!")

            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_m:
                    main_menu()

        if not game_over:
            draw_board()

        pygame.display.flip()

# Start the game
main_menu()
