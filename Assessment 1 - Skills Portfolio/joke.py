import tkinter as tk
import random

# Tell jokes from the file  
def load_jokes():
    jokes = []
    file = open("resources/randomJokes.txt", "r")
    for line in file:
        if "?" in line:
            parts = line.split("?")
            setup = parts[0] + "?"
            punchline = parts[1].strip()
            jokes.append([setup, punchline])
    file.close()
    return jokes

# Collect info of the joke 
jokes = load_jokes()
current_setup = ""
current_punchline = ""

# Picking a random joke 
def show_joke():
    global current_setup, current_punchline
    joke = random.choice(jokes)
    current_setup = joke[0]
    current_punchline = joke[1]
    
    setup_label.config(text=current_setup)
    punchline_label.config(text="")
    
    punchline_button.config(state="normal")

# The punchline
def show_punchline():
    punchline_label.config(text=current_punchline)

# Creating the window
window = tk.Tk()
window.title("Alexa Jokess")
window.geometry("500x350")

# Title at top
title = tk.Label(window, text="Alexa Jokes", font=("Arial", 20))
title.pack(pady=20)

# Where the joke setup appears
setup_label = tk.Label(window, text="Click button to hear a joke!", font=("Arial", 12), wraplength=400)
setup_label.pack(pady=20)

# Where the punchline appears
punchline_label = tk.Label(window, text="", font=("Arial", 12), wraplength=400, fg="blue")
punchline_label.pack(pady=10)

# Here are all buttons 
joke_button = tk.Button(window, text=" Tell me a Joke", command=show_joke, width=20, height=2, bg="green", fg="white")
joke_button.pack(pady=5)

punchline_button = tk.Button(window, text="Show Punchline", command=show_punchline, width=20, height=2, bg="blue", fg="white")
punchline_button.pack(pady=5)

next_button = tk.Button(window, text="Next Joke", command=show_joke, width=20, height=2, bg="orange", fg="white")
next_button.pack(pady=5)

quit_button = tk.Button(window, text="Quit", command=window.quit, width=20, height=2, bg="red", fg="white")
quit_button.pack(pady=5)

# To start app
window.mainloop()