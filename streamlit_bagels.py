import random
import streamlit as st

# ===== GAME LOGIC =====

def get_secret_num(num_digits):
    num_list = list(range(10))
    random.shuffle(num_list)
    return "".join(str(i) for i in num_list[:num_digits])

def getclues(guess, secret_num, num_digits):
    clues = []
    for i in range(num_digits):
        if guess[i] == secret_num[i]:
            clues.append("fermi")
        elif guess[i] in secret_num:
            clues.append("pico")
    return clues if clues else ["bagels"]

def reset_game():
    st.session_state.secret = get_secret_num(st.session_state.num_digits)
    st.session_state.history = []
    st.session_state.guess_count = 1
    st.session_state.game_over = False

def colorize(clues):
    icons = {"fermi": "🟢 Fermi", "pico": "🟡 Pico", "bagels": "🔴 Bagels"}
    return " ".join(icons[c] for c in clues)

# ===== PAGE SETUP =====

st.set_page_config(page_title="Bagels Game", page_icon="🥯", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&display=swap');

.stApp {
    background-color: #E8D7C3;
    background-image:
        repeating-linear-gradient(45deg, transparent, transparent 35px,
            rgba(139, 90, 60, 0.1) 35px, rgba(139, 90, 60, 0.1) 70px),
        repeating-linear-gradient(-45deg, transparent, transparent 35px,
            rgba(139, 90, 60, 0.1) 35px, rgba(139, 90, 60, 0.1) 70px);
    font-family: 'Fredoka', cursive;
}

#MainMenu, footer, header {visibility: hidden;}

h1, h2, h3 {
    font-family: 'Fredoka', cursive !important;
    color: #5D4037 !important;
}

.history-item {
    background: #FFFFFF;
    padding: 1rem 1.5rem;
    border-radius: 12px;
    margin: 0.6rem 0;
    border: 3px solid #D7A86E;
    box-shadow: 0 4px 0px rgba(139, 90, 60, 0.3);
    color: #5D4037;
}

.stTextInput > label {display: none !important;}
.stTextInput > div {margin: 0 0 1rem 0 !important;}

.stTextInput input {
    background: #FFFFFF !important;
    border: 4px solid #8B5A3C !important;
    border-radius: 12px !important;
    padding: 1rem 1.5rem !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    text-align: center !important;
    color: #5D4037 !important;
    letter-spacing: 8px !important;
    box-shadow: 0 4px 0px rgba(139, 90, 60, 0.3) !important;
}

.stTextInput input::placeholder {
    color: #A0785A !important;
    opacity: 0.6 !important;
    letter-spacing: 2px !important;
    font-size: 1rem !important;
}

.stButton > button {
    background: #D7A86E !important;
    color: #3E2723 !important;
    border: 4px solid #8B5A3C !important;
    border-radius: 15px !important;
    padding: 1.2rem 3rem !important;
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    box-shadow: 0 6px 0px rgba(139, 90, 60, 0.6) !important;
    cursor: pointer !important;
    font-family: 'Fredoka', cursive !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 0px rgba(139, 90, 60, 0.6) !important;
}

.stButton > button:active {
    transform: translateY(3px) !important;
    box-shadow: 0 3px 0px rgba(139, 90, 60, 0.6) !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #6D4C41 0%, #5D4037 100%) !important;
    border-right: 5px solid #8B5A3C !important;
    min-width: 280px !important;
    max-width: 280px !important;
}

[data-testid="stSidebar"] > div {
    overflow-y: auto !important;
    max-height: 100vh !important;
}

[data-testid="stSidebar"] * {
    color: #FEFAE0 !important;
}

/* Fix sidebar collapse button */
[data-testid="collapsedControl"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ===== INITIALIZE STATE =====

if "num_digits" not in st.session_state:
    st.session_state.num_digits = 3
    st.session_state.max_guesses = 10
    reset_game()

# ===== TITLE =====

st.title("🥯 BAGELS - The Deductive Logic Game")

# ===== SIDEBAR =====

st.sidebar.header("Game Settings")

digits = st.sidebar.selectbox(
    "Difficulty (Number of Digits)",
    [3, 4, 5, 6],
    index=[3, 4, 5, 6].index(st.session_state.num_digits)
)

if digits != st.session_state.num_digits:
    st.session_state.num_digits = digits
    reset_game()

if st.sidebar.button("New Game", use_container_width=True):
    reset_game()
    st.rerun()

st.sidebar.markdown("""
### How to Play

**Clues:**
- 🟢 **Fermi** - Right digit, right spot
- 🟡 **Pico** - Right digit, wrong spot
- 🔴 **Bagels** - No correct digits

**Rules:**
- No repeated digits
- Use logic to deduce
- Beat it before running out!
""")

# ===== MAIN GAME =====

game_col, history_col = st.columns([1, 1])

with game_col:
    st.markdown("### Place Your Guess")

    if not st.session_state.game_over:
        st.markdown(f"**Guess {st.session_state.guess_count} of {st.session_state.max_guesses}**")

        guess = st.text_input(
            "guess",
            max_chars=st.session_state.num_digits,
            key="guess_input",
            label_visibility="collapsed",
            placeholder=f"Enter {st.session_state.num_digits} digits"
        )

        if st.button("Submit Guess", use_container_width=True, type="primary"):
            if not guess.isdigit() or len(guess) != st.session_state.num_digits:
                st.error("Please enter a valid numeric guess!")
            else:
                clues = getclues(guess, st.session_state.secret, st.session_state.num_digits)
                st.session_state.history.append((guess, clues))

                if guess == st.session_state.secret:
                    st.balloons()
                    st.success("🎉 YOU GOT IT!")
                    st.session_state.game_over = True
                    st.rerun()
                else:
                    st.session_state.guess_count += 1
                    if st.session_state.guess_count > st.session_state.max_guesses:
                        st.error(f"Out of guesses! Answer: **{st.session_state.secret}**")
                        st.session_state.game_over = True
                        st.rerun()

with history_col:
    st.markdown("### Guess History")

    if st.session_state.history:
        for i, (g, clues) in enumerate(st.session_state.history, start=1):
            st.markdown(
                f"<div class='history-item'><strong>#{i}</strong> &nbsp; "
                f"<code style='font-size:1.3rem;letter-spacing:4px;color:#8B5A3C;font-weight:700;'>{g}</code> "
                f"&nbsp;→&nbsp; {colorize(clues)}</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("Your guesses will appear here")

# ===== GAME OVER =====

if st.session_state.game_over:
    st.markdown("---")
    st.markdown("### 🎮 Game Over!")
    st.info(f"Solved in {st.session_state.guess_count} guesses!")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Play Again", use_container_width=True, type="primary"):
            reset_game()
            st.rerun()
