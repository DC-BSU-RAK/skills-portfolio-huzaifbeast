import tkinter as tk
from tkinter import messagebox
import random

# variables 
score = 0
question_number = 0
num1 = 0
num2 = 0
operation = ''
answer = 0
attempt_count = 1
difficulty_level = ''

# main window setup
root = tk.Tk()
root.title("Arithmetic Quiz")
root.geometry("400x300")

# this shows the difficulty menu at the start
def displayMenu():
    global score, question_number, attempt_count
    
    # reset the game
    score = 0
    question_number = 0
    attempt_count = 1
    
    # remove everything from window first
    for widget in root.winfo_children():
        widget.destroy()
    
    # title at top
    title = tk.Label(root, text="ARITHMETIC QUIZ", font=("Arial", 20))
    title.pack(pady=20)
    
    # heading for difficulty options
    difficulty_text = tk.Label(root, text="DIFFICULTY LEVEL", font=("Arial", 14))
    difficulty_text.pack(pady=10)
    
    #   button for different leval
    button1 = tk.Button(root, text="1. Easy", width=20, command=lambda: startQuiz("easy"))
    button1.pack(pady=5)
    
    button2 = tk.Button(root, text="2. Moderate", width=20, command=lambda: startQuiz("moderate"))
    button2.pack(pady=5)
    
    button3 = tk.Button(root, text="3. Advanced", width=20, command=lambda: startQuiz("advanced"))
    button3.pack(pady=5)

#  gives random question based on difficulty lvl
def randomInt(difficulty):
    if difficulty == "easy":
        # single digits only
        n1 = random.randint(0, 9)
        n2 = random.randint(0, 9)
        return n1, n2
    elif difficulty == "moderate":
        # two digit numbers
        n1 = random.randint(10, 99)
        n2 = random.randint(10, 99)
        return n1, n2
    else:
        # advanced is 4 digits
        n1 = random.randint(1000, 9999)
        n2 = random.randint(1000, 9999)
        return n1, n2

#  decide to pick additon or sabtraction 
def decideOperation():
    choice = random.randint(1, 2)
    if choice == 1:
        return '+'
    else:
        return '-'

#  start quiz after picking difficulty 
def startQuiz(level):
    global difficulty_level
    difficulty_level = level
    displayProblem()

# display  each problem to the user
def displayProblem():
    global question_number, num1, num2, operation, answer, attempt_count
    
    # clear everything first
    for widget in root.winfo_children():
        widget.destroy()
    
    # done with all 10 questions?
    if question_number >= 10:
        displayResults()
        return
    
    # move to next question
    question_number = question_number + 1
    attempt_count = 1
    
    # generate new problem
    num1, num2 = randomInt(difficulty_level)
    
    # pick random operation
    operation = decideOperation()
    
    # calculate correct answer
    if operation == '+':
        answer = num1 + num2
    else:
        answer = num1 - num2
    
    # display question number
    info = tk.Label(root, text="Question " + str(question_number) + " of 10", font=("Arial", 12))
    info.pack(pady=10)
    
    score_label = tk.Label(root, text="Score: " + str(score), font=("Arial", 12))
    score_label.pack()
    
    # display the math problem
    problem = tk.Label(root, text=str(num1) + " " + operation + " " + str(num2) + " =", font=("Arial", 24))
    problem.pack(pady=30)
    
    # text box where user types answer
    global answer_box
    answer_box = tk.Entry(root, font=("Arial", 16), width=10)
    answer_box.pack(pady=10)
    
    # button to submit answer
    submit = tk.Button(root, text="Submit", command=checkAnswer)
    submit.pack(pady=10)

# checks the users answer
def checkAnswer():
    global score, attempt_count
    
    # get the answer from text box
    try:
        user_answer = int(answer_box.get())
    except:
        messagebox.showerror("Error", "Please enter a number!")
        return
    
    # see if they got it right
    if isCorrect(user_answer):
        if attempt_count == 1:
            # first try gets 10 points
            score = score + 10
            messagebox.showinfo("Correct!", "You got it right! +10 points")
        else:
            # second try gets 5 points
            score = score + 5
            messagebox.showinfo("Correct!", "You got it right! +5 points")
        displayProblem()
    else:
        if attempt_count == 1:
            # give them another chance
            attempt_count = 2
            messagebox.showwarning("Wrong", "Try again! One more chance.")
            answer_box.delete(0, tk.END)
        else:
            # no more chances, show answer
            messagebox.showerror("Wrong", "The answer was " + str(answer))
            displayProblem()

# compares user answer with correct answer
def isCorrect(user_ans):
    if user_ans == answer:
        return True
    else:
        return False

# displays final score and grade at end
def displayResults():
    global score
    
    # clear the window
    for widget in root.winfo_children():
        widget.destroy()
    
    # calculate grade based on score
    if score >= 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    else:
        grade = "D"
    
    # show final results
    result_title = tk.Label(root, text="Quiz Complete!", font=("Arial", 20))
    result_title.pack(pady=20)
    
    score_text = tk.Label(root, text="Your Score: " + str(score) + " / 100", font=("Arial", 16))
    score_text.pack(pady=10)
    
    grade_text = tk.Label(root, text="Grade: " + grade, font=("Arial", 18))
    grade_text.pack(pady=10)
    
    # buttons to play again or exit
    play_again = tk.Button(root, text="Play Again", command=displayMenu, width=15)
    play_again.pack(pady=10)
    
    exit_button = tk.Button(root, text="Exit", command=root.quit, width=15)
    exit_button.pack(pady=5)

# this starts everything
displayMenu()
root.mainloop()