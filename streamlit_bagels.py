import random
import streamlit as st

# ====== ORIGINAL GAME LOGIC (UNCHANGED) ======

def get_secret_num(num_digits):
    num_list = list(range(10))
    random.shuffle(num_list)
    secret_num = ""

    for i in num_list[0:num_digits]:
        secret_num += str(i)

    return secret_num


def getclues(guess, secret_num, num_digits):
    clues = []

    for i in range(num_digits):
        if guess[i] == secret_num[i]:
            clues.append("fermi")
        for y in range(num_digits):
            if guess[i] == secret_num[y] and secret_num[i] != guess[i]:
                clues.append("pico")

    if len(clues) == 0:
        clues.append("bagels")

    clues.sort()
    return clues


# ====== STREAMLIT UI HELPERS ======

def colorize_clues(clues):
    parts = []

    for p in clues:
        if p == "fermi":
            parts.append(":green[Fermi]")
        elif p == "pico":
            parts.append(":orange[Pico]")
        else:
            parts.append(":red[Bagels]")

    return " ".join(parts)


def reset_game():
    st.session_state.secret = get_secret_num(st.session_state.num_digits)
    st.session_state.history = []
    st.session_state.guess_count = 1
    st.session_state.game_over = False


# ====== APP START ======

st.set_page_config(page_title="Bagels Game", page_icon="🎯")

st.title("🕹️ Bagels – Deductive Logic Game")

# Initialize session state
if "num_digits" not in st.session_state:
    st.session_state.num_digits = 3
    st.session_state.max_guesses = 10
    reset_game()

# ====== SIDEBAR CONTROLS ======

st.sidebar.header("Game Settings")

digits = st.sidebar.selectbox(
    "Number of digits",
    [3, 4, 5, 6],
    index=[3, 4, 5, 6].index(st.session_state.num_digits),
)

if digits != st.session_state.num_digits:
    st.session_state.num_digits = digits
    reset_game()

if st.sidebar.button("Restart Game"):
    reset_game()

st.sidebar.markdown("---")

st.sidebar.markdown("""
**Rules**

- Guess the secret number  
- No repeated digits  

**Clues:**

:green[Fermi] – correct digit, correct place  
:orange[Pico] – correct digit, wrong place  
:red[Bagels] – no correct digits  
""")

# ====== MAIN GAME AREA ======

if not st.session_state.game_over:

    st.subheader(f"Guess {st.session_state.guess_count} of {st.session_state.max_guesses}")

    guess = st.text_input(
        f"Enter a {st.session_state.num_digits}-digit guess:",
        max_chars=st.session_state.num_digits,
        key="guess_input",
    )

    submit = st.button("Submit Guess")

    if submit:
        if not guess.isdigit() or len(guess) != st.session_state.num_digits:
            st.error(f"Please enter exactly {st.session_state.num_digits} digits.")
        else:
            clues = getclues(
                guess,
                st.session_state.secret,
                st.session_state.num_digits
            )

            st.session_state.history.append((guess, clues))

            if guess == st.session_state.secret:
                st.success("🎉 You got it!")
                st.session_state.game_over = True

            else:
                st.session_state.guess_count += 1

                if st.session_state.guess_count > st.session_state.max_guesses:
                    st.error(f"You ran out of guesses! The answer was {st.session_state.secret}")
                    st.session_state.game_over = True

# ====== SHOW HISTORY ======

if st.session_state.history:
    st.subheader("Guess History")

    for i, (g, clues) in enumerate(st.session_state.history, start=1):
        st.write(
            f"**{i}.** `{g}` → {colorize_clues(clues)}"
        )

# ====== GAME OVER OPTIONS ======

if st.session_state.game_over:
    if st.button("Play Again"):
        reset_game()
