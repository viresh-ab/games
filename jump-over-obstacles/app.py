import streamlit as st
import time

st.set_page_config(page_title="🌙 Jump Game", page_icon="🌙", layout="centered")
st.title("🌙 Jump Over Obstacles Game")
st.write("Press SPACE to jump! Avoid the red obstacles.")

# --- Game settings ---
WINDOW_HEIGHT = 10      # Number of vertical blocks
WINDOW_WIDTH = 30       # Number of horizontal blocks
GROUND_LEVEL = WINDOW_HEIGHT - 1

player_pos = 0          # Vertical position (0 = top)
player_jump = False
jump_height = 3
jump_counter = 0

obstacle_pos = WINDOW_WIDTH - 1
obstacle_speed = 1      # Blocks per frame

score = 0
game_over = False

# --- Streamlit placeholders ---
game_placeholder = st.empty()
score_placeholder = st.empty()
start_button = st.button("Start Game")

# --- Draw the game frame ---
def draw_frame(player_y, obstacle_x):
    frame = ""
    for y in range(WINDOW_HEIGHT):
        line = ""
        for x in range(WINDOW_WIDTH):
            if y == GROUND_LEVEL:
                line += "🟩"  # Ground
            elif x == 2 and y == player_y:
                line += "🙂"  # Player
            elif x == obstacle_x and y == GROUND_LEVEL - 1:
                line += "🟥"  # Obstacle
            else:
                line += "⬜"  # Empty space
        frame += line + "\n"
    return frame

# --- Game loop ---
if start_button:
    player_pos = GROUND_LEVEL - 1
    obstacle_pos = WINDOW_WIDTH - 1
    score = 0
    jump_counter = 0
    game_over = False

    st.info("Press SPACE in your keyboard to jump (focus must be on the browser)")

    # We need JS to capture SPACE key
    st.markdown(
        """
        <script>
        const playerJump = () => {
            const input = window.parent.document.querySelector('body');
            input.addEventListener('keydown', (e) => {
                if (e.code === 'Space') {
                    fetch("/jump");
                }
            });
        };
        playerJump();
        </script>
        """,
        unsafe_allow_html=True,
    )

    while not game_over:
        # Jump logic
        if jump_counter > 0:
            player_pos = GROUND_LEVEL - 1 - jump_height
            jump_counter -= 1
        else:
            player_pos = GROUND_LEVEL - 1

        # Draw frame
        frame_text = draw_frame(player_pos, obstacle_pos)
        game_placeholder.text(frame_text)
        score_placeholder.write(f"Score: {score}")

        # Update obstacle
        obstacle_pos -= obstacle_speed
        if obstacle_pos < 0:
            obstacle_pos = WINDOW_WIDTH - 1
            score += 1

        # Collision detection
        if obstacle_pos == 2 and player_pos == GROUND_LEVEL - 1:
            game_over = True
            game_placeholder.text(draw_frame(player_pos, obstacle_pos))
            score_placeholder.write(f"Game Over! Your Score: {score}")
            break

        time.sleep(0.15)  # Control game speed

        # Handle jump (simulate pressing SPACE)
        if st.session_state.get("jump", False):
            jump_counter = 3
            st.session_state["jump"] = False

# --- Jump Button for browsers that can't capture key ---
if st.button("Jump"):
    st.session_state["jump"] = True
