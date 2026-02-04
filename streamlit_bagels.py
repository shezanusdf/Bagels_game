import random
import streamlit as st
import json
import os
import requests
from datetime import datetime
from urllib.parse import urlencode

# ===== CONFIGURATION =====

# Load from Streamlit secrets or environment variables
if hasattr(st, "secrets"):
    HACKCLUB_CLIENT_ID = st.secrets.get("HACKCLUB_CLIENT_ID", os.getenv("HACKCLUB_CLIENT_ID", ""))
    HACKCLUB_CLIENT_SECRET = st.secrets.get("HACKCLUB_CLIENT_SECRET", os.getenv("HACKCLUB_CLIENT_SECRET", ""))
    REDIRECT_URI = st.secrets.get("REDIRECT_URI", os.getenv("REDIRECT_URI", "http://localhost:8501"))
else:
    HACKCLUB_CLIENT_ID = os.getenv("HACKCLUB_CLIENT_ID", "")
    HACKCLUB_CLIENT_SECRET = os.getenv("HACKCLUB_CLIENT_SECRET", "")
    REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8501")

LEADERBOARD_FILE = "leaderboard.json"

# ===== GAME LOGIC =====

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

def reset_game():
    st.session_state.secret = get_secret_num(st.session_state.num_digits)
    st.session_state.history = []
    st.session_state.guess_count = 1
    st.session_state.game_over = False
    st.session_state.score = None

def calculate_score(num_digits, guess_count, max_guesses):
    """Calculate score based on difficulty and efficiency"""
    base_score = num_digits * 100
    efficiency_bonus = ((max_guesses - guess_count + 1) / max_guesses) * base_score
    return int(base_score + efficiency_bonus)

def colorize(clues):
    parts = []
    for p in clues:
        if p == "fermi":
            parts.append("🟢 Fermi")
        elif p == "pico":
            parts.append("🟡 Pico")
        else:
            parts.append("🔴 Bagels")
    return " ".join(parts)

# ===== OAUTH FUNCTIONS =====

def get_authorization_url():
    """Generate Hack Club OAuth authorization URL"""
    params = {
        "client_id": HACKCLUB_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid profile email name"
    }
    return f"https://auth.hackclub.com/oauth/authorize?{urlencode(params)}"

def exchange_code_for_token(code):
    """Exchange authorization code for access token"""
    try:
        response = requests.post(
            "https://auth.hackclub.com/oauth/token",
            json={
                "client_id": HACKCLUB_CLIENT_ID,
                "client_secret": HACKCLUB_CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "code": code,
                "grant_type": "authorization_code"
            }
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error exchanging code: {str(e)}")
        return None

def get_user_info(access_token):
    """Get user information from Hack Club Auth"""
    try:
        response = requests.get(
            "https://auth.hackclub.com/api/v1/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error getting user info: {str(e)}")
        return None

# ===== LEADERBOARD FUNCTIONS =====

def load_leaderboard():
    """Load leaderboard from JSON file"""
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'r') as f:
            return json.load(f)
    return []

def save_leaderboard(leaderboard):
    """Save leaderboard to JSON file"""
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(leaderboard, f, indent=2)

def add_to_leaderboard(user_name, score, num_digits, guess_count):
    """Add a score to the leaderboard"""
    leaderboard = load_leaderboard()
    entry = {
        "name": user_name,
        "score": score,
        "difficulty": num_digits,
        "guesses": guess_count,
        "timestamp": datetime.now().isoformat()
    }
    leaderboard.append(entry)
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    save_leaderboard(leaderboard[:100])  # Keep top 100

def get_top_scores(limit=10):
    """Get top N scores from leaderboard"""
    leaderboard = load_leaderboard()
    return leaderboard[:limit]

# ===== PAGE SETUP =====

st.set_page_config(page_title="Bagels Game", page_icon="🥯", layout="wide")

# ===== CLEAN TABLECLOTH DESIGN =====

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Comic+Neue:wght@400;700&display=swap');

/* Checkered Tablecloth Background */
.stApp {
    background-color: #E8D7C3;
    background-image:
        repeating-linear-gradient(45deg,
            transparent,
            transparent 35px,
            rgba(139, 90, 60, 0.1) 35px,
            rgba(139, 90, 60, 0.1) 70px),
        repeating-linear-gradient(-45deg,
            transparent,
            transparent 35px,
            rgba(139, 90, 60, 0.1) 35px,
            rgba(139, 90, 60, 0.1) 70px);
    font-family: 'Fredoka', cursive;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Typography - NO SHADOWS */
h1, h2, h3, .stMarkdown {
    font-family: 'Fredoka', cursive !important;
    color: #5D4037 !important;
}

h1 {
    font-size: 3rem !important;
    font-weight: 700 !important;
    text-align: center;
    color: #5D4037 !important;
    margin-bottom: 0.5rem !important;
}

h2, h3 {
    color: #6D4C41 !important;
}

/* Game Cards */
.game-card {
    background: #FEFAE0;
    border-radius: 20px;
    padding: 2rem;
    margin: 1.5rem 0;
    box-shadow: 0 8px 0px rgba(139, 90, 60, 0.3);
    border: 5px solid #8B5A3C;
    color: #5D4037;
}

.leaderboard-card {
    background: #FFF8E1;
    border-radius: 18px;
    padding: 1.8rem;
    margin: 1rem 0;
    box-shadow: 0 6px 0px rgba(139, 90, 60, 0.25);
    border: 4px solid #A0785A;
    color: #5D4037;
}

.history-item {
    background: #FFFFFF;
    padding: 1rem 1.5rem;
    border-radius: 12px;
    margin: 0.8rem 0;
    border: 3px solid #D7A86E;
    box-shadow: 0 4px 0px rgba(139, 90, 60, 0.3);
    color: #5D4037;
}

.leaderboard-item {
    background: #FFFFFF;
    padding: 0.8rem 1.2rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    border: 2px solid #D7A86E;
    color: #5D4037;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.leaderboard-item.top-1 {
    border-color: #FFD700;
    background: linear-gradient(135deg, #FFF9E6 0%, #FFE8CC 100%);
}

.leaderboard-item.top-2 {
    border-color: #C0C0C0;
}

.leaderboard-item.top-3 {
    border-color: #CD7F32;
}

/* Input Styling */
.stTextInput > label {
    display: none !important;
}

.stTextInput > div {
    margin-top: 0 !important;
}

.stTextInput > div > div > input {
    background: #FFFFFF !important;
    border: 5px solid #8B5A3C !important;
    border-radius: 15px !important;
    padding: 1.3rem !important;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    text-align: center !important;
    color: #5D4037 !important;
    letter-spacing: 10px !important;
    font-family: 'Comic Neue', cursive !important;
}

.stTextInput > div > div > input::placeholder {
    color: #D7A86E !important;
    opacity: 0.5 !important;
    letter-spacing: 4px !important;
}

/* Button Styling */
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
    transition: all 0.1s ease !important;
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

/* Sidebar Styling */
.css-1d391kg, [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #6D4C41 0%, #5D4037 100%) !important;
    border-right: 5px solid #8B5A3C !important;
}

.css-1d391kg h2, [data-testid="stSidebar"] h2,
.css-1d391kg h3, [data-testid="stSidebar"] h3,
.css-1d391kg p, [data-testid="stSidebar"] p,
.css-1d391kg label, [data-testid="stSidebar"] label,
.css-1d391kg .stMarkdown, [data-testid="stSidebar"] .stMarkdown {
    color: #FEFAE0 !important;
}

/* Alert Styling */
.stAlert {
    border-radius: 15px !important;
    border: 4px solid #8B5A3C !important;
    box-shadow: 0 5px 0px rgba(139, 90, 60, 0.3) !important;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 14px;
}

::-webkit-scrollbar-track {
    background: #E8D7C3;
}

::-webkit-scrollbar-thumb {
    background: #8B5A3C;
    border-radius: 7px;
    border: 2px solid #E8D7C3;
}

::-webkit-scrollbar-thumb:hover {
    background: #6D4C41;
}
</style>
""", unsafe_allow_html=True)

# ===== OAUTH HANDLING =====

# Check for OAuth code in URL parameters
query_params = st.query_params
if "code" in query_params and "user" not in st.session_state:
    code = query_params["code"]
    token_data = exchange_code_for_token(code)
    if token_data:
        access_token = token_data.get("access_token")
        user_info = get_user_info(access_token)
        if user_info:
            st.session_state.user = user_info
            st.session_state.access_token = access_token
    # Clear the code from URL
    st.query_params.clear()
    st.rerun()

# ===== INITIALIZE STATE =====

if "num_digits" not in st.session_state:
    st.session_state.num_digits = 3
    st.session_state.max_guesses = 10
    reset_game()

# ===== TITLE =====

st.markdown("<br>", unsafe_allow_html=True)
st.title("BAGELS - The Deductive Logic Game")

# Show login/user info
col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    if "user" in st.session_state:
        user_name = st.session_state.user.get("name", "Player")
        st.markdown(f"<p style='text-align:center; font-size:1.1rem; color:#6D4C41;'>Logged in as <strong>{user_name}</strong></p>", unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True):
            del st.session_state.user
            del st.session_state.access_token
            st.rerun()
    else:
        st.markdown("<p style='text-align:center; font-size:1.1rem; color:#6D4C41;'>Login to save your scores to the leaderboard</p>", unsafe_allow_html=True)
        if HACKCLUB_CLIENT_ID and HACKCLUB_CLIENT_SECRET:
            auth_url = get_authorization_url()
            st.markdown(f"<a href='{auth_url}' target='_self'><button style='background:#D7A86E; color:#3E2723; border:4px solid #8B5A3C; border-radius:15px; padding:0.8rem 2rem; font-size:1.1rem; font-weight:700; cursor:pointer; width:100%;'>Login with Hack Club</button></a>", unsafe_allow_html=True)
        else:
            st.info("OAuth not configured. Set HACKCLUB_CLIENT_ID and HACKCLUB_CLIENT_SECRET")

st.markdown("<br>", unsafe_allow_html=True)

# ===== SIDEBAR SETTINGS =====

st.sidebar.header("Game Settings")

digits = st.sidebar.selectbox(
    "Difficulty (Number of Digits)",
    [3, 4, 5, 6],
    index=[3,4,5,6].index(st.session_state.num_digits)
)

if digits != st.session_state.num_digits:
    st.session_state.num_digits = digits
    reset_game()

st.sidebar.markdown("<br>", unsafe_allow_html=True)

if st.sidebar.button("Start Fresh Game", use_container_width=True):
    reset_game()
    st.rerun()

st.sidebar.markdown("""
### How to Play

Guess the secret number!

🟢 **Fermi** - Right digit, right spot
🟡 **Pico** - Right digit, wrong spot
🔴 **Bagels** - No correct digits

**Rules:**
- No repeated digits in the secret
- Use logic to deduce from your clues
- Beat it before running out of guesses!

### Scoring

Score = (Digits × 100) + Efficiency Bonus
- Higher difficulty = Higher score
- Fewer guesses = Higher bonus

---

Made with ☕ by Hack Club Community
""")

# ===== MAIN GAME AREA - SIDE BY SIDE LAYOUT =====

game_col, history_col = st.columns([1, 1])

# Left Column: Gameplay
with game_col:
    if not st.session_state.game_over:
        st.markdown("<div class='game-card'>", unsafe_allow_html=True)

        st.markdown("### Place Your Guess")
        st.markdown(f"**Guess {st.session_state.guess_count} of {st.session_state.max_guesses}**")
        st.markdown("<br>", unsafe_allow_html=True)

        guess = st.text_input(
            "guess",
            max_chars=st.session_state.num_digits,
            key="guess_input",
            label_visibility="collapsed",
            placeholder=f"{st.session_state.num_digits} digits..."
        )

        submit_clicked = st.button("Submit Guess", use_container_width=True)

        if submit_clicked:
            if not guess.isdigit() or len(guess) != st.session_state.num_digits:
                st.error("Please enter a valid numeric guess!")
            else:
                clues = getclues(
                    guess,
                    st.session_state.secret,
                    st.session_state.num_digits
                )

                st.session_state.history.append((guess, clues))

                if guess == st.session_state.secret:
                    st.balloons()
                    st.success("YOU GOT IT!")

                    # Calculate score
                    score = calculate_score(
                        st.session_state.num_digits,
                        st.session_state.guess_count,
                        st.session_state.max_guesses
                    )
                    st.session_state.score = score
                    st.session_state.game_over = True

                    # Add to leaderboard if logged in
                    if "user" in st.session_state:
                        user_name = st.session_state.user.get("name", "Anonymous")
                        add_to_leaderboard(
                            user_name,
                            score,
                            st.session_state.num_digits,
                            st.session_state.guess_count
                        )

                    st.rerun()

                else:
                    st.session_state.guess_count += 1

                    if st.session_state.guess_count > st.session_state.max_guesses:
                        st.error(f"Out of guesses! The answer was **{st.session_state.secret}**")
                        st.session_state.game_over = True
                        st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# Right Column: Guess History
with history_col:
    st.markdown("<div class='game-card'>", unsafe_allow_html=True)
    st.markdown("### Guess History")

    if st.session_state.history:
        for i, (g, clues) in enumerate(st.session_state.history, start=1):
            st.markdown(
                f"<div class='history-item'><strong>#{i}</strong> &nbsp;&nbsp; <code style='font-size:1.4rem;letter-spacing:6px;color:#8B5A3C;font-weight:700;'>{g}</code> &nbsp;&nbsp;→&nbsp;&nbsp; {colorize(clues)}</div>",
                unsafe_allow_html=True
            )
    else:
        st.markdown("<p style='text-align:center; color:#8B5A3C; padding:2rem 0;'>Your guesses will appear here</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ===== GAME OVER =====

if st.session_state.game_over:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='game-card' style='text-align:center;'>", unsafe_allow_html=True)
        st.markdown("### Game Over!")

        if st.session_state.score:
            st.markdown(f"### Your Score: {st.session_state.score}")
            st.markdown(f"*Solved in {st.session_state.guess_count} guesses with {st.session_state.num_digits} digits*")

        if st.button("Play Again", use_container_width=True):
            reset_game()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ===== LEADERBOARD =====

st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("<div class='leaderboard-card'>", unsafe_allow_html=True)
    st.markdown("### 🏆 Top 10 Leaderboard")

    top_scores = get_top_scores(10)

    if top_scores:
        for idx, entry in enumerate(top_scores, 1):
            rank_class = f"top-{idx}" if idx <= 3 else ""
            medal = ["🥇", "🥈", "🥉"][idx-1] if idx <= 3 else f"#{idx}"

            st.markdown(
                f"""<div class='leaderboard-item {rank_class}'>
                    <div><strong>{medal} {entry['name']}</strong></div>
                    <div>{entry['score']} pts | {entry['difficulty']}D in {entry['guesses']} guesses</div>
                </div>""",
                unsafe_allow_html=True
            )
    else:
        st.info("No scores yet. Be the first to set a record!")

    st.markdown("</div>", unsafe_allow_html=True)
