import random
import time
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from pyfiglet import Figlet

console = Console()
console.clear()

# Default settings (changed by menu)
NUM_DIGITS = 3
MAX_GUESS = 10


# ======== RETRO EFFECTS ========

def crt_scanlines(text):
    """Add fake CRT scanlines"""
    lines = text.split("\n")
    out = []
    for i, line in enumerate(lines):
        if i % 2 == 0:
            out.append(f"[dim]{line}[/dim]")
        else:
            out.append(line)
    return "\n".join(out)


def loading_screen():
    console.clear()
    title = Figlet(font="slant").renderText("BAGELS")
    console.print(Align.center(crt_scanlines(title)))

    console.print("\n[bold cyan]Initializing Retro Game Engine...[/bold cyan]\n")

    for i in range(20):
        console.print("[green]█[/green]" * i)
        time.sleep(0.05)
        console.clear()
        console.print(Align.center(crt_scanlines(title)))

    time.sleep(0.3)


# ======== MENU SYSTEM ========

def main_menu():
    global NUM_DIGITS

    while True:
        console.clear()

        title = Figlet(font="big").renderText("BAGELS")
        console.print(Align.center(crt_scanlines(title)))

        menu = Panel(
            "[1] Start Game\n"
            "[2] Difficulty\n"
            "[3] Quit",
            title="Main Menu",
            border_style="bright_blue"
        )

        console.print(Align.center(menu))

        choice = console.input("\n> ")

        if choice == "1":
            loading_screen()
            return
        elif choice == "2":
            difficulty_menu()
        elif choice == "3":
            console.clear()
            console.print("[bold red]Goodbye!<3[/bold red]")
            sys.exit()


def difficulty_menu():
    global NUM_DIGITS

    console.clear()

    console.print(Panel(
        "Select number length:\n\n"
        "[1] Easy   – 3 digits\n"
        "[2] Normal – 4 digits\n"
        "[3] Hard   – 5 digits\n"
        "[4] Insane – 6 digits",
        title="Difficulty",
        border_style="yellow"
    ))

    choice = console.input("> ")

    if choice == "1":
        NUM_DIGITS = 3
    elif choice == "2":
        NUM_DIGITS = 4
    elif choice == "3":
        NUM_DIGITS = 5
    elif choice == "4":
        NUM_DIGITS = 6


# ======== MAIN GAME ========

def main():

    main_menu()

    console.clear()

    console.print(
        Panel.fit(
            "[bold cyan]BAGELS – Deductive Logic Game[/bold cyan]",
            border_style="bright_blue",
        )
    )

    console.print(f"""
[bold]Rules:[/bold]
I'm thinking of a [yellow]{NUM_DIGITS}-digit[/yellow] number with no repeated digits.

[green]Fermi[/green] – One digit is correct and in the right position.
[yellow]Pico[/yellow]  – One digit is correct but in the wrong position.
[red]Bagels[/red] – No digits are correct.
""")

    while True:
        secret_num = get_secret_num()
        history = []

        num_guesses = 1

        while num_guesses <= MAX_GUESS:

            draw_ui(history, num_guesses)

            guess = ""

            while len(guess) != NUM_DIGITS or not guess.isnumeric():
                console.print(f"[bold]Enter Guess #{num_guesses}[/bold]")
                guess = console.input("> ")

            clues = getclues(guess, secret_num)

            colored = colorize_clues(clues)

            history.append((guess, colored))

            if guess == secret_num:
                draw_ui(history, num_guesses)
                console.print(Panel("[bold green]🎉 You got it![/bold green]"))
                break

            num_guesses += 1

            if num_guesses > MAX_GUESS:
                draw_ui(history, num_guesses - 1)
                console.print(
                    Panel(
                        f"[red]You ran out of guesses![/red]\n"
                        f"The answer was: [bold]{secret_num}[/bold]"
                    )
                )

        console.print("\nDo you want to play again? (yes or no)")
        if not console.input("> ").lower().startswith("y"):
            console.clear()
            console.print("[bold cyan]Thanks for playing![/bold cyan]")
            break

        # NEW CLEAR ADDED HERE – ensures next game starts fresh
        console.clear()


# ======== UI RENDERING ========

def draw_ui(history, current_guess):
    console.clear()

    title = Figlet(font="small").renderText("Bagels")
    console.print(Align.center(crt_scanlines(title)))

    console.print(
        f"[bold]Guess {current_guess} of {MAX_GUESS}[/bold]\n"
    )

    table = Table(title="Guess History", border_style="bright_white")

    table.add_column("#", justify="center")
    table.add_column("Guess", justify="center")
    table.add_column("Clues", justify="center")

    for i, (guess, clues) in enumerate(history, start=1):
        table.add_row(str(i), guess, clues)

    panel = Panel(table, title="Game Board", border_style="cyan")

    console.print(panel)


# ======== COLORIZED CLUES ========

def colorize_clues(clues):
    parts = clues.split()
    out = []

    for p in parts:
        if p == "fermi":
            out.append("[green]Fermi[/green]")
        elif p == "pico":
            out.append("[yellow]Pico[/yellow]")
        else:
            out.append("[red]Bagels[/red]")

    return " ".join(out)


# ======== ORIGINAL LOGIC (UNCHANGED) ========

def get_secret_num():
    num_list = list(range(10))
    random.shuffle(num_list)
    secret_num = ""

    for i in num_list[0:NUM_DIGITS]:
        secret_num += str(i)

    return secret_num


def getclues(guess, secret_num):
    clues = []

    for i in range(NUM_DIGITS):
        if guess[i] == secret_num[i]:
            clues.append("fermi")
        for y in range(NUM_DIGITS):
            if guess[i] == secret_num[y] and secret_num[i] != guess[i]:
                clues.append("pico")

    if len(clues) == 0:
        clues.append("bagels")

    clues.sort()
    return " ".join(clues)


if __name__ == '__main__':
    main()
