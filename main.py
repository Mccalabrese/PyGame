import random
import time
import pygame
from button import Button

pygame.init()

pygame.font.init()
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

GREEN_ON = (0, 255, 0)
GREEN_OFF = (0, 227, 0)
RED_ON = (255, 0, 0)
RED_OFF = (227, 0, 0)
BLUE_ON = (0, 0, 255)
BLUE_OFF = (0, 0, 227)
YELLOW_ON = (255, 255, 0)
YELLOW_OFF = (227, 227, 0)

# Sounds
GREEN_SOUND = pygame.mixer.Sound("bell1.mp3")
RED_SOUND = pygame.mixer.Sound("bell2.mp3")
BLUE_SOUND = pygame.mixer.Sound("bell3.mp3")
YELLOW_SOUND = pygame.mixer.Sound("bell4.mp3")

# Button Sprite Objects
green = Button(GREEN_ON, GREEN_OFF, GREEN_SOUND, 20, 10)
red = Button(RED_ON, RED_OFF, RED_SOUND, 140, 10)
blue = Button(BLUE_ON, BLUE_OFF, BLUE_SOUND, 260, 10)
yellow = Button(YELLOW_ON, YELLOW_OFF, YELLOW_SOUND, 380, 10)

# Variables
colors = ["green", "red", "blue", "yellow"]
cpu_sequence = []
score = 0
game_over_state = False
TIMER_DURATION = 3  # Duration of each turn
remaining_time = TIMER_DURATION
player_turn_active = False

def draw_board():
    SCREEN.fill((0, 0, 0))
    green.draw(SCREEN)
    red.draw(SCREEN)
    blue.draw(SCREEN)
    yellow.draw(SCREEN)

    # Render score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    SCREEN.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT - 50))

    # Render timer as text
    timer_text = font.render(f"Time: {remaining_time:.1f}", True, (255, 255, 255))
    SCREEN.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, SCREEN_HEIGHT - 80))

def cpu_turn():
    if not game_over_state:
        choice = random.choice(colors)
        cpu_sequence.append(choice)
        button = {"green": green, "red": red, "blue": blue, "yellow": yellow}[choice]
        button.update(SCREEN)

def repeat_cpu_sequence():
    if cpu_sequence and not game_over_state:
        for color in cpu_sequence:
            button = {"green": green, "red": red, "blue": blue, "yellow": yellow}[color]
            button.update(SCREEN)
            pygame.time.wait(500)

def start_player_turn():
    global player_turn_active, remaining_time
    player_turn_active = True
    remaining_time = TIMER_DURATION  # Reset timer at the start of player turn

def player_turn():
    global score, remaining_time, player_turn_active
    players_sequence = []
    start_time = pygame.time.get_ticks()

    while len(players_sequence) < len(cpu_sequence) and not game_over_state and player_turn_active:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        remaining_time = max(0, TIMER_DURATION - elapsed_time)

        draw_board()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                if green.selected(pos):
                    players_sequence.append("green")
                    if not check_sequence(players_sequence):
                        return
                    green.update(SCREEN)
                elif red.selected(pos):
                    players_sequence.append("red")
                    if not check_sequence(players_sequence):
                        return
                    red.update(SCREEN)
                elif blue.selected(pos):
                    players_sequence.append("blue")
                    if not check_sequence(players_sequence):
                        return
                    blue.update(SCREEN)
                elif yellow.selected(pos):
                    players_sequence.append("yellow")
                    if not check_sequence(players_sequence):
                        return
                    yellow.update(SCREEN)

        # End the turn if time runs out
        if remaining_time <= 0:
            game_over()
            return

        if len(players_sequence) == len(cpu_sequence):
            score += 1
            player_turn_active = False  # End player turn
            return

def check_sequence(players_sequence):
    if players_sequence != cpu_sequence[:len(players_sequence)]:
        game_over()
        return False
    return True

def game_over():
    global game_over_state, player_turn_active
    print("Game Over! Final Score:", score)
    game_over_state = True
    player_turn_active = False

def reset_game():
    global cpu_sequence, score, game_over_state
    cpu_sequence.clear()
    score = 0
    game_over_state = False
    print("Game restarted.")

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN and game_over_state:
            if event.key == pygame.K_SPACE:
                reset_game()

    if not game_over_state:
        draw_board()
        repeat_cpu_sequence()
        cpu_turn()
        start_player_turn()
        player_turn()
        pygame.display.update()
        clock.tick(60)
    else:
        # Display Game Over message
        SCREEN.fill((0, 0, 0))
        game_over_text = font.render("Game Over! Press SPACE to Restart", True, (255, 0, 0))
        SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.update()
