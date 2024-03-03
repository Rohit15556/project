from tkinter import *
from tkinter import messagebox
import sqlite3
import tkinter.font as font
# from PIL import Image, ImageTk

register = {}

a = Tk()
a.attributes("-fullscreen",True)
bg=Image.open("page.jpg")
bg=bg.resize((1600,1000))
# my_label=ImageTk.PhotoImage(bg)
# mylabel=Label(a,image=my_label)
# mylabel.place(x=0,y=0)

screen_width = a.winfo_screenwidth()
screen_height= a.winfo_screenheight()

def min():
    a.iconify()
def enter(i):
    btn2['background']="red"
def leave(i):
    btn2['background']="#b6ac89"
def max():
    msg_box =messagebox.askquestion('Exit Application', 'Are you sure you want to close the application?',icon='warning')
    if msg_box == 'yes':
        a.destroy()
label1=LabelFrame(a,height=35,fg="blue",bg="#57a1f8").place(x=0,y=0)
buttonFont = font.Font(size=14)

btn2=Button(a,text="✕", command=max,width=4,bg="#b6ac89",border=0,font=buttonFont)
btn2.pack(anchor="ne")
btn2.bind('<Enter>',enter)
btn2.bind('<Leave>',leave)

btn=Button(a,text="-", command=min,width=4,bg="#b6ac89",border=0,font=buttonFont)
btn.place(x=screen_width-100,y=0)
def enter(i):
    btn['background']="red"
def leave(i):
    btn['background']="#b6ac89"
btn.bind('<Enter>',enter)
btn.bind('<Leave>',leave)


def login():
    store_username = e1.get()
    store_password = e2.get()
    if store_username in register and register[store_username] == store_password:
        a.destroy()
        import main
    else:
        messagebox.showerror("Login Error", "Invalid username or password.")

#Function to create new account
def new():
    #Database connection
    con = sqlite3.connect('info_database.db')
    cursor = con.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS info(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    uname TEXT,
    pass TEXT
    confirmpass TEXT,
    email  TEXT
    )''')
    con.commit()
    con.close()
    #Function to create account
    def createaccount():
        
        new_username = new_usernameentry.get()
        new_password = new_passwordentry.get()
        c=confirmpasswordentry.get()
        emailget=email_entry.get()
        if new_password!=c:
            messagebox.showerror("Error","Password do not match")
        elif "@" not in emailget or emailget.endswith(".com")==False:
            messagebox.showerror("Error","Enter a Valid Email")
        elif new_username=="" or new_password=="" or c=="" or emailget=="":
            messagebox.showerror("Error", "Please fill all the form")
        else:
            #Add user to resister dictionary
            register[new_username] = new_password
            messagebox.showinfo("Success", "Account created successfully.")
            con = sqlite3.connect('info_database.db')
            c = con.cursor()
            #Insert data into database
            c.execute('INSERT INTO info(uname, pass) VALUES(?,?)',
                      (new_usernameentry.get(), new_passwordentry.get()))
            con.commit()
            con.close()
            #clear empty field
            new_usernameentry.delete(0, END)
            new_passwordentry.delete(0, END)
            new_accountwindow.destroy()
        

    #Create new account window
    new_accountwindow = Toplevel(a)
    new_accountwindow.title("Create New Account")
    new_accountwindow.attributes("-fullscreen",True)
    #Load and configure background image
    global bgimggg
    bgimg=(Image.open("page.jpg"))
    bgimg=bgimg.resize((1600,1000))
    # bgimggg=ImageTk.PhotoImage(bgimg)
    # mylabel=Label(new_accountwindow,image=bgimggg)
    # mylabel.place(x=0,y=0)
    #Function to go back to main login screen
    def back():
        new_accountwindow.destroy()
    #Create back button    
    btn4=Button(new_accountwindow,text="Back",width=4,bg="#b6ac89",border=0,font=buttonFont,command=back)
    btn4.pack(anchor="ne")
    def enter(i):
        btn4['background']="red"
    def leave(i):
        btn4['background']="#b6ac89"
    btn4.bind('<Enter>',enter)
    btn4.bind('<Leave>',leave)
    
    def toggle1_password():
        if show_password1.get():
            new_passwordentry.config(show="")
        else:
            new_passwordentry.config(show="*")

    def toggle_pass():
        if show_pass.get():
            confirmpasswordentry.config(show="")
        else:
            confirmpasswordentry.config(show="*")
    #Create entry fields and label
    new_username_label = Label(new_accountwindow, text="Username:", font=('Arial', '18', ''),bg="#f9d8a8")
    new_username_label.place(x=510, y=310)
    new_usernameentry = Entry(new_accountwindow, bg='#FFE1FF')
    new_usernameentry.place(x=510, y=345)

    new_password_label = Label(new_accountwindow, text="Create Password:", font=('Arial', '18', ''),bg="#f9d8a8")
    new_password_label.place(x=510, y=380)
    new_passwordentry = Entry(new_accountwindow, bg='#FFE1FF', show='*')
    new_passwordentry.place(x=510, y=415)
    
    confirmpassword_label = Label(new_accountwindow, text="Confirm Password:", font=('Arial', '18', ''),bg="#f9d8a8")
    confirmpassword_label.place(x=510, y=450)
    confirmpasswordentry = Entry(new_accountwindow, bg='#FFE1FF', show='*')
    confirmpasswordentry.place(x=510, y=485)

    email=Label(new_accountwindow,text="EMAIL:", font=('Arial', '18', ''),bg="#f9d8a8")
    email.place(x=510,y=520)
    email_entry=Entry(new_accountwindow, bg='#FFE1FF')
    email_entry.place(x=510,y=555)

    sign_up = Button(new_accountwindow, text='          Sign Up          ', bg='red', fg='white',
                     font=('Arial', '12', ''), command=createaccount).place(x=510, y=590)
    
    Createnewaccount = Label(new_accountwindow, text='CREATE NEW ACCOUNT', font=('Arial', '22', 'bold'),bg="#f9d8a8").place(x=680, y=250)
    #Checkbax to show password
    show_password1 = BooleanVar()
    show_password1_checkbutton = Checkbutton(new_accountwindow, text="Show",bg="#f9d8a8",font=('Arial', '11', ''), variable=show_password1, command=toggle1_password)
    show_password1_checkbutton.place(x=640, y=410)

    show_pass = BooleanVar()
    show_pass_checkbutton = Checkbutton(new_accountwindow, text="Show",bg="#f9d8a8",font=('Arial', '11', ''), variable=show_pass, command=toggle_pass)
    show_pass_checkbutton.place(x=640, y=480)

    

Login = Label(a, text='LOGIN', font=('Arial', '22', 'bold'),bg="#f9d8a8").place(x=720, y=250)

Username = Label(a, text='Username', font=('Arial', '18', ''),bg="#f9d8a8").place(x=510, y=310)
e1 = Entry(a, bg='#FFE1FF')
e1.place(x=510, y=345)

def toggle2_password():
    if show_password2.get():
        e2.config(show="")
    else:
        e2.config(show="*")

Password = Label(a, text='Password', font=('Arial', '18', ''),bg="#f9d8a8").place(x=510, y=380)
e2 = Entry(a, bg='#FFE1FF', show='*')
e2.place(x=510, y=415)

show_password2 = BooleanVar()
show_password2_checkbutton = Checkbutton(a, text="Show",bg="#f9d8a8",font=('Arial', '11', ''), variable=show_password2, command=toggle2_password)
show_password2_checkbutton.place(x=640, y=410)

Login_Button = Button(a, text='LOGIN', bg='red', fg='white', font=('Arial', '12', ''), command=login).place(x=510, y=460)

Or = Label(a, text="---------------or---------------",bg="#f9d8a8",font=('Arial', '12', '')).place(x=510, y=540)

account = Button(a, text='Create New Account', bg='red', fg='white', font=('Arial', '12', ''), command=new)
account.place(x=510, y=575)

# Function to retrieve passwords from database
def forgetpassword_database():
    con = sqlite3.connect('info_database.db')
    cursor = con.cursor()
    cursor.execute('SELECT uname, pass FROM info')
    data = cursor.fetchall()
    for username, password in data:
        register[username] = password
    con.close()
forgetpassword_database()
# Function to handle forgotten passwords
def forget():
    def reset_password():
        username = forget_username.get()
        new_password = forget_new_password.get()
        con = sqlite3.connect('info_database.db')
        cursor = con.cursor()
        cursor.execute('SELECT * FROM info WHERE uname = ?', (username,))
        result = cursor.fetchone()
        con.close()
        if result:
            con = sqlite3.connect('info_database.db')
            cursor = con.cursor()
            cursor.execute('UPDATE info SET pass = ? WHERE uname = ?', (new_password, username))
            con.commit()
            con.close()
            register[username] = new_password 
            messagebox.showinfo("Password Reset", "Your password has been reset successfully.")
        else:
            messagebox.showerror("Username Error", "Username not found.")
        forget_passwordwindow.destroy()
    # Create forget password window
    forget_passwordwindow = Toplevel(a)
    forget_passwordwindow.title("Forgot Password")
    forget_passwordwindow.attributes("-fullscreen",True)
    # Load and configure background image
    global backg
    bgimg=(Image.open("page.jpg"))
    bgimg=bgimg.resize((1600,1000))
    # backg=ImageTk.PhotoImage(bgimg)
    # mylabel=Label(forget_passwordwindow,image=backg)
    # mylabel.place(x=0,y=0)
    def back():
        forget_passwordwindow.destroy()
    # Create back button
    btn4=Button(forget_passwordwindow,text="Back",width=4,bg="#b6ac89",border=0,font=buttonFont,command=back)
    btn4.pack(anchor="ne")
    def enter(i):
        btn4['background']="red"
    def leave(i):
        btn4['background']="#b6ac89"
    btn4.bind('<Enter>',enter)
    btn4.bind('<Leave>',leave)
    # Entry fields and labels for forgotten password
    forget_username_label = Label(forget_passwordwindow, text="Enter Username:", font=('Arial', '18', ''),bg="#f9d8a8")
    forget_username_label.place(x=510, y=310)
    forget_username = Entry(forget_passwordwindow, bg='#FFE1FF')
    forget_username.place(x=510, y=345)
    forget_new_password_label = Label(forget_passwordwindow, text="Enter New Password:", font=('Arial', '18', ''),bg="#f9d8a8")
    forget_new_password_label.place(x=510, y=380)
    forget_new_password = Entry(forget_passwordwindow, bg='#FFE1FF', show='*')
    forget_new_password.place(x=510, y=415)

    def toggle3_password():
        if show_password3.get():
            forget_new_password.config(show="")
        else:
            forget_new_password.config(show="*")
    # Checkbox to show password
    show_password3 = BooleanVar()
    show_password3_checkbutton = Checkbutton(forget_passwordwindow, text="Show",bg="#f9d8a8",font=('Arial', '11', ''), variable=show_password3, command=toggle3_password)
    show_password3_checkbutton.place(x=640, y=410)
    # Button to reset password
    reset_password_button = Button(forget_passwordwindow, text='Reset Password', bg='red', fg='white',font=('Arial', '12', ''), command=reset_password)
    reset_password_button.place(x=510, y=460)
    # Label for "Forget Password"
    forgetpassword = Label(forget_passwordwindow, text='FORGET PASSWORD', font=('Arial', '22', ''), bg="#f9d8a8").place(x=680, y=250)



forget_pass = Button(a, text='Forgotten password?', fg='blue', font=('Arial', '12', ''), command=forget)
forget_pass.place(x=510, y=505)

a.mainloop()

