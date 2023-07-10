from tkinter import *
from customtkinter import *
import tkinter.messagebox as msg
import pandas as pd
import numpy as np
import pyttsx3
import smtplib
import ssl
from email.message import EmailMessage
import pandas as pd
import random as rd
import speech_recognition as sr
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
engine = pyttsx3.init()
def update_score():
    global total
       # Load the user DataFrame from CSV
    db = pd.read_csv('user.csv')

    # Filter the user for the given username
    user_data = db[db['Username'] == uname]
    highest_score = user_data['Highest_score'].iloc[0]
    if highest_score < total:
        db.loc[db['Username'] == uname, 'Highest_score'] = total
        db.to_csv('user.csv', index=False)
def exit_game():
    global score, current_question_index
    score=0
    
    # Reset variables
    current_question_index = 0
    okcancel=msg.askokcancel("Quit","All your progress will be lost. \nAre you sure you want to exit game?")
    if okcancel:
        update_score()
    # Clear the game frame
        game_frame.pack_forget()

        # Show the question type frame
        questiontype_frame.pack()

def speak(text):
    engine.say(text)
    engine.runAndWait()


# Variables
current_question_index = 0
score = 0

def submit_answer():
    global score, total,questions_df
    # Get the selected option
    selected = int(selected_option.get())
    
    # Check if the selected option is correct
    
    if (current_question_index-1)< len(questions_df):
        correct_option = int(questions_df.loc[current_question_index-1, 'correct_answer'])

        if selected == correct_option:
            score += 1
            total = score
            msg.showinfo("Answer status", f"Correct answer! Score: {score}")
        else:
            msg.showerror("Answer status", "Incorrect answer")

    show_question()

def show_question():
    global current_question_index
    
    # Check if all questions have been answered
    if current_question_index >=len(questions_df):
        msg.showinfo("Quiz Status",f"Quiz completed. Final score:{score}")
        update_score()
        return
    
    # Get the question and options for the current index
    if current_question_index < len(questions_df):
        question = questions_df.loc[current_question_index, 'question']
        options = [
            questions_df.loc[current_question_index, 'optA'],
            questions_df.loc[current_question_index, 'optB'],
            questions_df.loc[current_question_index, 'optC'],
            questions_df.loc[current_question_index, 'optD']
        ]
        
        # Clear previous selection
        selected_option.set(0)
        
        
        # Update the question label
        label_question.config(text=question)
        
        # Update the radio button options
        for i in range(len(radio_buttons)):
            radio_buttons[i].config(text=options[i])
        
        # Schedule the speech output after a delay
        label_question.after(1000, speak, question)
        for option in options:
            label_question.after(2000, speak, option)
    
    # Increment the question index
    current_question_index += 1
def signup_cancel(retrycancel):
    if retrycancel:
            signup_frame.pack()
    else:
            signup_frame.pack_forget()
            Main_frame.pack()

def frame_questiontype():
    menu_frame.pack_forget()
    questiontype_frame.pack(pady=100)


def frame_game(question_type):
    global questions_df
    questiontype_frame.pack_forget()
    game_frame.pack()
    if question_type == "IT":
        questions_df = pd.read_csv('IT.csv')
    elif question_type == "Geography":
        questions_df = pd.read_csv('geography.csv')
    elif question_type == "Science":
        questions_df = pd.read_csv('science.csv')
    elif question_type == "Sports":
        questions_df = pd.read_csv('sports.csv')
    show_question()

def logout():
    yesno=msg.askyesno("Logout","Are you sure you want to log out?")
    if yesno:
        menu_frame.pack_forget()
        main()
    else:
        frame_menu()
speak
def frame_menu():
    login_frame.pack_forget()
    menu_frame.pack(padx=25,pady=250)


def confcode():
    signup_frame.pack_forget()
    conf_frame.pack()
    global code
    code=IntVar()
    code=rd.randint(100000,999999)
    
    sender=("Enter your email here")
    sender_pw="enter your password"
    subject="verification Code"
    body=f"Your verification code is {code}" 
    em=EmailMessage()
    em['From']=sender
    em['to']=entry_semail.get()
    em['subject']=subject
    em.set_content(body)
    context=ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(sender,sender_pw)
        smtp.sendmail(sender,entry_semail.get(),em.as_string())

def confirmation():

    conf_code=IntVar()
    conf_code=int(entry_code.get())
    if conf_code!=code:
        retrycancel=msg.askretrycancel("Invalid code", "The code is invalid. Try Again")
        if retrycancel:
            conf_frame.pack()
        else:
            signup_frame.pack()  
    else:
        details={
                'Name':[entry_name.get()],
                'Userame':[entry_suname.get()],
                'Password':[str(entry_spw.get())],
                'Email':[entry_semail.get()],
                'Highest_score':0
                }
        df=pd.DataFrame(details)
        df.to_csv('user.csv', mode='a',index=False, header=False)
        conf_frame.pack_forget()
        frame_login()

def frame_signup():
    Main_frame.pack_forget()
    signup_frame.pack()

def SignUp():    
    user=pd.read_csv('user.csv')
    db=pd.DataFrame(user)
    entry = str(entry_spw.get())
    contains_alpha = any(c.isalpha() for c in entry)
    contains_numeric = any(c.isnumeric() for c in entry)
    sign_name=StringVar()
    sign_email=StringVar()
    sign_uname=StringVar()
    sign_pw=StringVar()
    sign_confpw=StringVar()
    
    sign_name=entry_name.get()
    sign_uname=entry_suname.get()
    sign_pw=entry_spw.get()
    sign_email=entry_semail.get()
    sign_confpw=entry_confpw.get()

    if not all([sign_name, sign_uname, sign_pw, sign_email, sign_confpw]):
        retrycancel=msg.askretrycancel("Empty","Please Fill all the boxes")
        signup_cancel(retrycancel)
    else:
        if  (entry_suname.get() in db['Username'].values)or(entry_semail.get() in db['Emails'].values):
           retrycancel=msg.askokcancel("Uname Error",f"{sign_email} or {sign_uname} already exists")
           signup_cancel(retrycancel)
        else:
            if not (contains_alpha and contains_numeric):
                retrycancel=msg.askretrycancel("Password Error","The passwords must contain an alphabet and a number")
                signup_cancel(retrycancel)
            else:
                if sign_pw!=sign_confpw:
                    retrycancel=msg.askretrycancel("Password Error","The passwords doesnt match")
                    signup_cancel(retrycancel)
                else:
                    confcode()
def frame_login():
    Main_frame.pack_forget()
    login_frame.pack(padx=100, pady=100) 
    
def Login():
    user=pd.read_csv('user.csv')
    db=pd.DataFrame(user)
    global uname
    uname = entry_uname.get()
    pw = entry_pw.get()

    if not all([uname, pw]):
        msg.showerror("Missing Information", "Please enter both username and password.")
    elif uname not in db['Username'].values:
        msg.showerror("Login Error", "Sorry, you are not registered.")
    elif pw != db.loc[db['Username'] == uname, 'Password'].iloc[0]:
        msg.showerror("Login Error", "Invalid password.")
    else:
        msg.showinfo("Login Successful", "You have successfully logged in.")
        login_frame.pack_forget()
        menu_frame.pack(padx=25, pady=250)

def main():
    signup_frame.pack_forget()
    Main_frame.pack(padx=20,pady=20)
window=Tk()
window.title("Voice Assisted Quiz Game")
selected_option = IntVar()

#Main Frame==========
Main_frame=Frame(window)
Label(Main_frame,text="Welcome To Voice Assisted Quiz Game", foreground="black", background="Yellow",font=('Aerial bold',20)).pack(pady=30)
Button(Main_frame, text="Sign Up",command=frame_signup).pack(pady=10)
Button(Main_frame, text="Login",command=frame_login).pack(pady=10)

#signup Frame======================================================================================================
signup_frame=Frame(window)
Label(signup_frame,text="REGISTER", foreground="black", background="Yellow",font=('Aerial bold',20)).pack(pady=30)

Name=Label(signup_frame, text='Full Name',font=13).pack()
entry_name = Entry(signup_frame)
entry_name.pack()

semail=Label(signup_frame, text='Email:',font=13).pack()
entry_semail = Entry(signup_frame)
entry_semail.pack()

suname=Label(signup_frame, text='Username:',font=13).pack()
entry_suname = Entry(signup_frame)
entry_suname.pack()

spw=Label(signup_frame, text='Password:',font=13).pack()
entry_spw = Entry(signup_frame, show='*')
entry_spw.pack()

confpw=Label(signup_frame, text='Confirm Password:',font=13).pack()
entry_confpw = Entry(signup_frame, show='*')
entry_confpw.pack()

Submit_butn=Button(signup_frame, text="Register",command=SignUp).pack(pady=20)

#Login Frame =========================================================================================
login_frame=Frame(window)
Label(login_frame,text="LOGIN", foreground="black", background="Yellow",font=('Aerial bold',20)).pack(pady=30)

uname=Label(login_frame, text='Username:',font=13).pack()
entry_uname = Entry(login_frame)
entry_uname.pack()

pw=Label(login_frame, text='Password:',font=13).pack()
entry_pw = Entry(login_frame,show='*')
entry_pw.pack()
Submit_butn=Button(login_frame, text="Login",command=Login).pack(pady=50)

#Confirmation code frame======================================================================
conf_frame=Frame(window)
Label(conf_frame, text="A 6 digit code has been sent into your gmail account. Please enter the code to confirm your gmail.", font=13).pack(pady=50)
entry_code = Entry(conf_frame)
entry_code.pack()
code_butn=Button(conf_frame, text="OK", command=confirmation).pack(pady=50)

#Menu frame ======================================================================================
menu_frame=Frame(window)
Playquiz_butn=Button(menu_frame, text="Play Quiz", command=frame_questiontype).pack(pady=20)
leader_butn=Button(menu_frame, text="See Leaderboard").pack(pady=20)
Logout_butn=Button(menu_frame, text="Logout", command=logout).pack(pady=20)
quit_butn=Button(menu_frame, text="Quit Game", command=quit).pack(pady=20)

#select question type frame
questiontype_frame=Frame(window)
Label(questiontype_frame,text="Choose question types", background="yellow",font=13).pack(padx=45, pady=50)
IT=Button(questiontype_frame, text="IT", command=lambda:frame_game("IT")).pack(pady=20)
geography=Button(questiontype_frame, text="Geography", command=lambda:frame_game("Geography")).pack(pady=20)
sports=Button(questiontype_frame, text="Sports", command=lambda:frame_game("Sports")).pack(pady=20)
Science=Button(questiontype_frame, text="Science", command=lambda:frame_game("Science")).pack(pady=20)



# Radio buttons for options

game_frame=Frame(window)
#Play quiz frame=====================================================================================
label_question = Label(game_frame, text="Question goes here")
label_question.pack(pady=20)
radio_buttons = []
for i in range(4):
    radio_button = Radiobutton(game_frame, text="", variable=selected_option, value=str(i+1))
    radio_button.pack(pady=5)
    radio_buttons.append(radio_button)


button_submit = Button(game_frame, text="Submit", command=submit_answer)
button_submit.pack(pady=10)
button_exit = Button(game_frame, text="Exit Game", command=exit_game)
button_exit.pack(pady=10)
main()
window.mainloop()