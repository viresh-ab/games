import streamlit as st
import pygame
import os
from streamlit.components.v1 import html

# --- Game Settings ---
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
FPS = 60
PLAYER_SIZE = 50
OBSTACLE_WIDTH = 30
OBSTACLE_HEIGHT = 50
GROUND_HEIGHT = 50

# --- Initialize pygame ---
pygame.init()
screen = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# --- Game variables ---
player_y = WINDOW_HEIGHT - PLAYER_SIZE - GROUND_HEIGHT
player_x = 50
player_vel_y = 0
gravity = 1
jump_strength = -15

obstacle_x = WINDOW_WIDTH
obstacle_speed = 5
score = 0
game_over = False

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

# --- Game loop ---
def game_loop():
    global player_y, player_vel_y, obstacle_x, score, game_over
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_y == WINDOW_HEIGHT - PLAYER_SIZE - GROUND_HEIGHT:
                player_vel_y = jump_strength

    if not game_over:
        # Player physics
        player_vel_y += gravity
        player_y += player_vel_y
        if player_y > WINDOW_HEIGHT - PLAYER_SIZE - GROUND_HEIGHT:
            player_y = WINDOW_HEIGHT - PLAYER_SIZE - GROUND_HEIGHT
            player_vel_y = 0

        # Obstacle movement
        obstacle_x -= obstacle_speed
        if obstacle_x < -OBSTACLE_WIDTH:
            obstacle_x = WINDOW_WIDTH
            score += 1

        # Collision detection
        if player_x + PLAYER_SIZE > obstacle_x and player_x < obstacle_x + OBSTACLE_WIDTH:
            if player_y + PLAYER_SIZE > WINDOW_HEIGHT - OBSTACLE_HEIGHT - GROUND_HEIGHT:
                game_over = True

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, (0, WINDOW_HEIGHT - GROUND_HEIGHT, WINDOW_WIDTH, GROUND_HEIGHT))
    pygame.draw.rect(screen, BLACK, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))
    pygame.draw.rect(screen, RED, (obstacle_x, WINDOW_HEIGHT - OBSTACLE_HEIGHT - GROUND_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
    return pygame.surfarray.array3d(screen)

# --- Streamlit frontend ---
st.title("🌙 Jump Game")
st.write("Press SPACE to jump over obstacles!")

# Placeholder for the game
game_placeholder = st.empty()

# Start game
if st.button("Start Game"):
    game_over = False
    player_y = WINDOW_HEIGHT - PLAYER_SIZE - GROUND_HEIGHT
    obstacle_x = WINDOW_WIDTH
    score = 0
    
    while not game_over:
        frame = pygame.transform.rotate(pygame.surfarray.make_surface(game_loop()), -90)
        frame = pygame.transform.flip(frame, True, False)
        game_placeholder.image(frame)
        clock.tick(FPS)

    st.write(f"Game Over! Your score: {score}")
