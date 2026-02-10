from flask import Flask,render_template,request,session,redirect,url_for
import random

NUM_DIGITS = 3
MAX_GUESS = 10

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def get_secret_num(num_digits):
    num_list = list(range(10))
    random.shuffle(num_list)
    secret_num = ""

    for i in num_list[0:num_digits]:
        secret_num += str(i)

    return secret_num

def getclues(guess, secret_num):
    clues = []
    for i in range(NUM_DIGITS) :
        if guess[i] == secret_num[i]:
            clues.append("fermi")
        for y in range(NUM_DIGITS) :
            if guess[i] == secret_num[y] and secret_num[i] != guess[i]:
                clues.append("pico")
    
    if len(clues) == 0:
        clues.append("bagels")
    clues.sort()
    return ' '.join(clues)

def colorize(clues):
    icons = {"fermi": "🟢 Fermi", "pico": "🟡 Pico", "bagels": "🔴 Bagels"}
    return " ".join(icons[word] for word in clues.split())
    
def reset_game(num_digits):
    session['secret'] = get_secret_num(num_digits)
    session['history'] = []
    session['guess_count'] = 1
    session['game_over'] = False
    session['num_digits'] = num_digits
    session['max_guesses'] = MAX_GUESS
    
@app.route('/', methods=['GET','POST'])
def index():
    if 'secret' not in session:
        reset_game(NUM_DIGITS)
        
    message = ''
    
    if request.method == 'POST':
        
        if 'new_game' in request.form:
            reset_game(session.get('num_digits',3))
            return redirect(url_for("index"))
        
        if 'change_digits' in request.form:
            digits = int(request.form['digits'])
            reset_game(digits)
            return redirect(url_for("index"))
        
        guess = request.form.get("guess", '')
        
        if not guess.isdecimal() or len(guess) != session['num_digits']:
            message = 'Please Enter a valid number'
        else:
            clues = getclues(guess, session['secret'])
            session['history'].append((guess,clues))
            session['guess_count'] += 1
            
            if guess == session['secret']:
                session['game_over'] = True
                message = 'YOU GOT IT!!'
                
            elif session['guess_count'] > session['max_guesses']:
                session['game_over'] = True
                message = f'Out of guesses! Answer was {session['secret']}'
                
            session.modified = True
    return render_template(
        'index.html',
        history=session.get("history", []),
        message=message,
        guess_count=session.get("guess_count", 1),
        max_guesses=session.get("max_guesses", 10),
        num_digits=session.get("num_digits", 3),
        game_over=session.get("game_over", False),
        colorize=colorize)
        
if __name__ == '__main__':
    app.run(debug = True)
    
    
    
    
