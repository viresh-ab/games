import streamlit as st
import random
import time

st.set_page_config(page_title="🍎 Catch the Apples", page_icon="🍎", layout="centered")
st.title("🍎 Catch the Apples Game")
st.write("Move the basket left/right using buttons and catch the apples!")

# --- Game settings ---
GRID_WIDTH = 10
GRID_HEIGHT = 10
TICK_SPEED = 0.3  # seconds per frame

# --- Initialize session state ---
if "basket_pos" not in st.session_state:
    st.session_state.basket_pos = GRID_WIDTH // 2
if "apple_pos" not in st.session_state:
    st.session_state.apple_pos = [random.randint(0, GRID_WIDTH - 1), 0]
if "score" not in st.session_state:
    st.session_state.score = 0
if "missed" not in st.session_state:
    st.session_state.missed = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "running" not in st.session_state:
    st.session_state.running = False

# --- Draw the game frame ---
def draw_frame():
    frame = ""
    for y in range(GRID_HEIGHT):
        line = ""
        for x in range(GRID_WIDTH):
            if [x, y] == st.session_state.apple_pos:
                line += "🍎"
            elif y == GRID_HEIGHT - 1 and x == st.session_state.basket_pos:
                line += "🧺"
            else:
                line += "⬜"
        frame += line + "\n"
    return frame

# --- Control buttons ---
col1, col2 = st.columns(2)
if col1.button("⬅️ Left"):
    if st.session_state.basket_pos > 0:
        st.session_state.basket_pos -= 1
if col2.button("➡️ Right"):
    if st.session_state.basket_pos < GRID_WIDTH - 1:
        st.session_state.basket_pos += 1

# --- Game placeholders ---
game_placeholder = st.empty()
score_placeholder = st.empty()

# --- Start button ---
if st.button("Start Game"):
    st.session_state.running = True
    st.session_state.basket_pos = GRID_WIDTH // 2
    st.session_state.apple_pos = [random.randint(0, GRID_WIDTH - 1), 0]
    st.session_state.score = 0
    st.session_state.missed = 0
    st.session_state.game_over = False

# --- Game loop ---
while st.session_state.running and not st.session_state.game_over:
    # Draw
    game_placeholder.text(draw_frame())
    score_placeholder.write(f"Score: {st.session_state.score} | Missed: {st.session_state.missed}")

    time.sleep(TICK_SPEED)

    # Move apple
    st.session_state.apple_pos[1] += 1

    # Check collision
    if st.session_state.apple_pos[1] == GRID_HEIGHT - 1:
        if st.session_state.apple_pos[0] == st.session_state.basket_pos:
            st.session_state.score += 1
        else:
            st.session_state.missed += 1
        st.session_state.apple_pos = [random.randint(0, GRID_WIDTH - 1), 0]

    # Check game over
    if st.session_state.missed >= 3:
        st.session_state.game_over = True
        game_placeholder.text(draw_frame())
        score_placeholder.write(f"Game Over! Final Score: {st.session_state.score}")
        st.session_state.running = False
        break
