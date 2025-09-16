import streamlit as st
import random
import time

st.set_page_config(page_title="🍎 Catch the Apples", page_icon="🍎", layout="centered")
st.title("🍎 Catch the Apples Game")
st.write("Move the basket left/right using buttons and catch the apples!")

# --- Game settings ---
GRID_WIDTH = 10
GRID_HEIGHT = 10

basket_pos = GRID_WIDTH // 2
apple_pos = [random.randint(0, GRID_WIDTH - 1), 0]  # x, y
score = 0
missed = 0
game_over = False

# --- Streamlit placeholders ---
game_placeholder = st.empty()
score_placeholder = st.empty()

# --- Draw the game frame ---
def draw_frame(basket_x, apple_xy):
    frame = ""
    for y in range(GRID_HEIGHT):
        line = ""
        for x in range(GRID_WIDTH):
            if [x, y] == apple_xy:
                line += "🍎"
            elif y == GRID_HEIGHT - 1 and x == basket_x:
                line += "🧺"
            else:
                line += "⬜"
        frame += line + "\n"
    return frame

# --- Control buttons ---
col1, col2 = st.columns(2)
if col1.button("⬅️ Left"):
    if basket_pos > 0:
        basket_pos -= 1
if col2.button("➡️ Right"):
    if basket_pos < GRID_WIDTH - 1:
        basket_pos += 1

# --- Game loop ---
start_button = st.button("Start Game")

if start_button:
    basket_pos = GRID_WIDTH // 2
    apple_pos = [random.randint(0, GRID_WIDTH - 1), 0]
    score = 0
    missed = 0
    game_over = False

    while not game_over:
        # Draw frame
        game_placeholder.text(draw_frame(basket_pos, apple_pos))
        score_placeholder.write(f"Score: {score} | Missed: {missed}")

        time.sleep(0.5)

        # Move apple down
        apple_pos[1] += 1

        # Check collision
        if apple_pos[1] == GRID_HEIGHT - 1:
            if apple_pos[0] == basket_pos:
                score += 1
            else:
                missed += 1
            apple_pos = [random.randint(0, GRID_WIDTH - 1), 0]

        if missed >= 3:
            game_over = True
            game_placeholder.text(draw_frame(basket_pos, apple_pos))
            score_placeholder.write(f"Game Over! Final Score: {score}")
            break
