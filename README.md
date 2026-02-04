# Bagels Game 🥯

A deductive logic number-guessing game with Hack Club OAuth authentication and competitive leaderboards!

## Features

- **Classic Bagels Game**: Guess the secret number using logical deduction
- **Multiple Difficulty Levels**: 3-6 digit numbers
- **Hack Club OAuth**: Login with your Hack Club account
- **Global Leaderboard**: Compete with the Hack Club community
- **Score System**: Points based on difficulty and efficiency
- **Clean UI**: Cozy checkered tablecloth design

## Game Rules

- Guess the secret number (no repeated digits)
- Get clues for each guess:
  - 🟢 **Fermi**: Right digit, right spot
  - 🟡 **Pico**: Right digit, wrong spot
  - 🔴 **Bagels**: No correct digits
- Win before running out of guesses!

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Register Your App with Hack Club Auth

1. Go to [Hack Club Auth Developer Apps](https://auth.hackclub.com/apps)
2. Click "app me up!" and fill out the form
3. Set your redirect URI (e.g., `http://localhost:8501` for local development)
4. Copy your Client ID and Client Secret

### 3. Configure Environment Variables

Create a `.env` file or set environment variables:

```bash
export HACKCLUB_CLIENT_ID="your_client_id_here"
export HACKCLUB_CLIENT_SECRET="your_client_secret_here"
export REDIRECT_URI="http://localhost:8501"
```

Or use Streamlit secrets (`.streamlit/secrets.toml`):

```toml
HACKCLUB_CLIENT_ID = "your_client_id_here"
HACKCLUB_CLIENT_SECRET = "your_client_secret_here"
REDIRECT_URI = "http://localhost:8501"
```

### 4. Run the App

```bash
streamlit run streamlit_bagels.py
```

## Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add your secrets in the Streamlit Cloud dashboard:
   - `HACKCLUB_CLIENT_ID`
   - `HACKCLUB_CLIENT_SECRET`
   - `REDIRECT_URI` (your deployed URL, e.g., `https://your-app.streamlit.app`)
5. Update your Hack Club OAuth app redirect URI to match your deployed URL

## Scoring System

```
Score = (Digits × 100) + Efficiency Bonus
```

- **Base Score**: Difficulty level × 100 points
- **Efficiency Bonus**: Based on how few guesses you used
- Higher difficulty + fewer guesses = higher score!

## Leaderboard

- Login with Hack Club to save your scores
- Top 100 scores are saved
- Compete with the Hack Club community
- Top 3 players get special medals 🥇🥈🥉

## Technologies Used

- **Streamlit**: Web app framework
- **Hack Club Auth**: OAuth 2.0 authentication
- **Python**: Game logic and backend
- **JSON**: Leaderboard storage

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

MIT License - feel free to use and modify!

## Credits

Built with ☕ by the Hack Club community

---

### OAuth Documentation

For more details on Hack Club OAuth integration, see:
- [OAuth Guide](https://auth.hackclub.com/docs/oauth-guide)
- [API Documentation](https://auth.hackclub.com/docs/api)
