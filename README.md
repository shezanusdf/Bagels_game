# Bagels Game 🥯

A classic deductive logic number-guessing game with a cozy checkered tablecloth design!

## Features

- **Classic Bagels Gameplay**: Guess the secret number using logical deduction
- **Multiple Difficulty Levels**: Choose between 3-6 digit numbers
- **Side-by-Side Layout**: See your guesses and clues in real-time
- **Clean UI**: Beautiful checkered tablecloth aesthetic
- **Instant Feedback**: Get clues after each guess

## Game Rules

Guess the secret number (no repeated digits allowed). After each guess, you'll get clues:

- 🟢 **Fermi**: Right digit in the right position
- 🟡 **Pico**: Right digit but wrong position
- 🔴 **Bagels**: No correct digits

Use logic to deduce the secret number before running out of guesses!

## Quick Start

### 1. Install Dependencies

```bash
pip install streamlit
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. Run the Game

```bash
streamlit run streamlit_bagels.py
```

The game will open in your browser at `http://localhost:8501`

## Deployment to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy!

That's it - no configuration needed!

## How to Play

1. **Choose Difficulty**: Select 3, 4, 5, or 6 digits in the sidebar
2. **Make a Guess**: Enter a number with unique digits
3. **Read the Clues**: Use Fermi, Pico, and Bagels to deduce the answer
4. **Win the Game**: Guess the correct number before running out of attempts!

## Strategy Tips

- Start with numbers that cover different digits (like 0, 1, 2, 3...)
- Track which digits you've eliminated
- Use Fermi clues to lock in correct positions
- Pay attention to Pico patterns to figure out placement

## Technologies Used

- **Streamlit**: Web app framework
- **Python**: Game logic and backend
- **CSS**: Custom styling for the checkered tablecloth theme

## Game Mechanics

- **No Repeated Digits**: The secret number never has duplicate digits
- **Limited Guesses**: You have 10 attempts to guess correctly
- **Smart Clues**: Clues are sorted and always honest
- **Fresh Start**: Click "New Game" anytime to start over

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve the documentation

## License

MIT License - feel free to use and modify!

## About Bagels

Bagels (also known as "Bulls and Cows" or "Mastermind with numbers") is a classic deductive reasoning game. This digital version brings the fun of the original game with a modern, user-friendly interface.

---

Built with ☕ and 🥯 | Enjoy the game!
