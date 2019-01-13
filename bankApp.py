from tkinter import *
import csv
root = Tk()
norm_font = ("Consolas", 20)
bold_font = ("Consolas", 20, "bold")

class User():
    def __init__(self, username, password, balance=0):
        self.username = username
        self.password = password
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount
        self.balance = round(self.balance, 2)

        with open("data.csv") as file:
            reader  = csv.DictReader(file)
            rows = [row for row in reader]

        for d in rows:
            if self.username == d["username"]:
                d["balance"] = self.balance


        with open("data.csv", "w") as file:
            field_names = ["username", "password", "balance"]
            writer = csv.DictWriter(file, fieldnames = field_names)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
            


class LoginPage (Frame):
    def __init__ (self, parent,*args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        accounts = []

        with open("data.csv") as file:
            reader = csv.DictReader(file)
            for dictionary in reader:
                user = User(dictionary["username"], dictionary["password"], balance=float(dictionary["balance"]))
                accounts.append(user)
        
        self.accounts = accounts

        main_label = Label(self, text = "Aarav's Bank", font = bold_font)
        main_label.grid(row = 1, column = 1, columnspan = 2)

        self.help_label = Label(self, text="Please login with your username and password.", font = norm_font)
        self.help_label.grid(row = 2, column = 1, columnspan = 2)

        username_label = Label(self, text = "Username", font = norm_font)
        username_label.grid(row = 3, column = 1)

        self.username_entry = Entry(self, font = norm_font, width = 10)
        self.username_entry.grid(row = 3, column = 2)

        password_label = Label(self, text = "Password", font = norm_font)
        password_label.grid(row = 4, column = 1)

        self.password_entry = Entry(self, width=10, font = norm_font, show="*")
        self.password_entry.grid(row = 4, column = 2)

        button = Button(self, font = norm_font, width = 10, text = "Submit", command = self.submit)
        button.grid(row = 5, column = 1, columnspan = 2)

        create_label = Label(self, font = norm_font, text = "Or, if you don't have an account, click below")
        create_label.grid(row = 6, column = 1, columnspan = 2, pady = 20)

        sign_up_button = Button(self, font = norm_font, text = "+Sign up", fg = "blue", command = self.sign_up)
        sign_up_button.grid(row = 7, column = 1, columnspan = 2, pady = (0, 10))

    def submit(self):
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        valid_login = False

        valid_username = False
        
        valid_user = None
        
        for user in self.accounts:
            if entered_username.upper() == user.username.upper():
                valid_username = True
                if entered_password.upper() == user.password.upper():
                    valid_login = True
                    valid_user = user
                

        if valid_login:
            self.destroy()
            account_page = AccountPage(self.parent, valid_user)
            account_page.pack()
        elif valid_username:
            self.help_label.config(text = "Incorrect Password for " + entered_username + ". Try again", font = bold_font, fg = "red")
        else:
            self.help_label.config(text = "Incorrect Username. Please try again", font = bold_font, fg = "red")

    def sign_up(self):
        self.destroy()
        sign_up_page = Sign_Up_Page(self.parent)
        sign_up_page.pack()
        

 
        

class AccountPage(Frame):
    def __init__(self, parent, user, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.user = user

        username_label = Label(self, text=user.username, font=norm_font)
        username_label.grid(row=1, column=1, columnspan=2)

        detail_label = Label(self, text = "Welcome to your account.", font = norm_font)
        detail_label.grid(row = 2, column = 1, columnspan = 2)

        balance_label = Label(self, text="Balance: " + str(user.balance), font=norm_font)
        balance_label.grid(row=3, column=1, columnspan=2)

        option = StringVar()
        option.set("Withdraw")
        option_menu = OptionMenu(self, option, "Withdraw", "Deposit")
        option_menu.grid(row = 4, column = 1)

        money_entry = Entry(self, width = 10, font=norm_font)
        money_entry.grid(row = 4, column = 2)

        

        def start_change():
            try:
                amount = float(money_entry.get())
            except ValueError:
                detail_label.config(text = "Invalid Input", fg = "red")
                return
          

            if option.get() == "Withdraw":
                
                if amount > user.balance:
                    detail_label.config(text = "You don't have enough money. ", fg = "red")
                    return
                
                amount *= -1

            user.deposit(amount)
            balance_label.config(text="Balance: " + str(user.balance))
            detail_label.config(text = "Your transaction has been completed successfully.", fg = "green")
                    
        go_button = Button(self, width=10, text="Go", command=start_change)
        go_button.grid(row=5, column=1, columnspan=2)

        
        def log_out():
            self.destroy()
            logout_page = LogoutPage(self.parent, self.user)
            logout_page.pack()


        logout_button = Button(self, width=10, text="Logout", command=log_out)
        logout_button.grid(row=6, column=1, columnspan=2)

class Sign_Up_Page(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        info_label = Label(self, font = norm_font, text = "Please start by creating a username and password")
        info_label.grid(row = 1, column = 1, columnspan = 2)

        self.error_label = Label(self, text = "", font = norm_font)
        self.error_label.grid(row = 2, column = 1, columnspan = 2)

        username_label = Label(self, text = "Username", font = norm_font)
        username_label.grid(row = 3, column = 1)

        self.username_entry = Entry(self, font = norm_font, width = 10)
        self.username_entry.grid(row = 3, column = 2)

        password_label = Label(self, text = "Password", font = norm_font)
        password_label.grid(row = 4, column = 1)

        self.password_entry = Entry(self, width=10, font = norm_font, show="*")
        self.password_entry.grid(row = 4, column = 2)

        confirm_password_label = Label(self, text = "Confirm Password", font = norm_font)
        confirm_password_label.grid(row = 5, column = 1)

        self.confirm_password_entry = Entry(self, width=10, font = norm_font, show="*")
        self.confirm_password_entry.grid(row = 5, column = 2)        

        button = Button(self, font = norm_font, width = 10, text = "Submit", command = self.submit)
        button.grid(row = 6, column = 1, columnspan = 2)

        
    def submit(self):
        if self.password_entry.get() != self.confirm_password_entry.get():
            self.error_label.config(text = "The passwords don't match.", fg = "red")
            return
        elif self.username_entry.get() == "" or self.password_entry.get() == "":
            self.error_label.config(text = "Invalid username or password.", fg = "red")
            return

        with open("data.csv") as file:
            reader = csv.DictReader(file)
            rows = [row for row in reader]

        for d in rows:
            if self.username_entry.get() == d["username"]:
                self.error_label.config(text = "That Username is taken.", fg = "red")
                return

        # Entry valid; create new user.

        with open("data.csv") as file:
            reader  = csv.DictReader(file)
            rows = [row for row in reader]

        new_user = User(self.username_entry.get(), self.password_entry.get())

        new_user_dictionary = {"username": new_user.username,
                    "password": new_user.password,
                    "balance": new_user.balance}

        rows.append(new_user_dictionary)

        with open("data.csv", "w") as file:
            field_names = ["username", "password", "balance"]
            writer = csv.DictWriter(file, fieldnames = field_names)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

        self.destroy()
        account_page = AccountPage(self.parent, new_user)
        account_page.pack()

class LogoutPage(Frame):
    def __init__ (self, parent, user,*args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        main_label = Label(self, text = "Thanks for visiting us!\nHope to see you again " + str(user.username.title()) + ".", font = bold_font, fg = "green")
        main_label.pack(padx = 40, pady=40)

        self.parent.after(5000, self.load_login_page)

    def load_login_page(self):
        self.destroy()
        login_page = LoginPage(self.parent)
        login_page.pack()

login = LoginPage(root)
login.pack()

