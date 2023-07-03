from json import JSONDecodeError
from tkinter import messagebox
from random import shuffle, randint, choice
import tkinter as tk
import pyperclip
import json


# Password Generator
def generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters = [choice(letters) for char in range(randint(8, 10))]
    symbols = [choice(symbols) for sym in range(randint(2, 4))]
    numbers = [choice(numbers) for num in range(randint(2, 4))]

    password_list = letters + symbols + numbers
    shuffle(password_list)
    passcode = "".join(password_list)
    if len(password_entry.get()) > 0:
        password_entry.delete(0, tk.END)

    password_entry.insert(0, passcode)
    pyperclip.copy(passcode)


# past_mail method checks for any persisting previously used emails and returns them if present of None if none
def past_mail():
    try:
        with open("data.json", mode="r") as k:
            data_file = json.load(k)

            if len(data_file) < 1:
                return None
            else:
                keys = [i for i in data_file]
                return data_file[keys[-1]]["email"]

    except FileNotFoundError or JSONDecodeError :
        with open("data.json", mode="w") as file:
            json.dump({}, file)

# rep_check ensures that there are no duplicate entries
def rep_check(data):
    try:
        with open("data.json", mode="r") as file:
            file = json.load(file)
            for i in file:
                if [i, file[i]["email"]] == data:
                    return True
    except FileNotFoundError or JSONDecodeError:
        with open("data.json", mode="w") as file:
            json.dump({}, file)


def store_pass(website_name, user, password):
    if len(website_name) == 0 or len(user) == 0 or len(password) == 0:
        messagebox.showinfo(title="Blank Space", message="Please fill out all entries")
    else:
        x = rep_check([website_name, user])

        if x:
            override = messagebox.askyesno(title="Password Exists", message=f'User Info already has an assigned '
                                                                            f'password\n\n 'f'Do wish wish to '
                                                                            f'override password')
            if override:
                with open("data.json", mode="r") as g:
                    data = json.load(g)
                    for i in data:
                        if (i, data[i]["email"]) == (website_name, user):
                            data.pop(i)
                            n_data = {
                                website_name: {
                                    "email": user,
                                    "password": password
                                }
                            }
                            data.update(n_data)
                with open("data.json", mode="w") as g:
                    json.dump(data, g, indent=4)

                override_info = messagebox.showinfo(title=website_name,
                                                    message=f'Password Override:\n\n Successful !')
            else:
                override_info = messagebox.showinfo(title=website_name,
                                                    message=f'Password Maintained!')
            return True

        else:
            new_entry= {
                website_name: {
                    "email": user,
                    "password": password
                }
            }
            with open("data.json", mode="r") as d:
                new_data = json.load(d)
                new_data.update(new_entry)

            with open("data.json", mode="w") as d:
                msg = messagebox.askyesno(title=website_name,
                                          message=f'Your password is ready\n\nEmail: {user}\nPassword: {password}\n'
                                                  f'\nCan we '
                                                  f'proceed ')
                if msg is True:
                    json.dump(new_data, d, indent=4)
                    return True


def search():
    try:
        with open("data.json", mode="r") as d:
            new_data = json.load(d)
    except FileNotFoundError:
        with open("data.json", mode="w") as file:
            messagebox.showinfo(title="Nay", message=f"Passcode not found!")
    except JSONDecodeError:
        with open("data.json", mode="w") as file:
            messagebox.showinfo(title="Nay", message=f"Passcode not found!")

    else:
        user = username_entry.get()
        website = web_entry.get().title()
        if len(new_data) == 0 or website not in new_data:
            messagebox.showinfo(title="Nay", message=f"Data not found!")
        else:
            for i in new_data:
                if (i, new_data[i]["email"]) == (website, user):
                    passcode = new_data[i]["password"]
                    messagebox.showinfo(title=website, message=f"\tEmail: {user}\n\nPassword: {passcode}")
                    pyperclip.copy(passcode)


def upload():
    website1 = web_entry.get().strip().title()
    username1 = username_entry.get().strip()
    password1 = password_entry.get().strip()

    if store_pass(website1, username1, password1) is True:

        web_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)


FONT_NAME = "Courier"
back_ground = "#000000"

# Window set-up
window = tk.Tk()
window.title("Password Manager")
window.config(padx=30, pady=45, bg=back_ground)

canvas = tk.Canvas(height=250, width=200, bg=back_ground, highlightthickness=0)
image = tk.PhotoImage(file="ghost_10.png")
canvas.create_image(98, 125, image=image)

canvas.grid(column=1, row=0)

txt = """
    I am Pass Keeper
 what password do you seek?
"""

greeting = tk.Label(text=txt, font=(FONT_NAME, 13, "bold"), fg="Green", bg=back_ground)
greeting.grid(column=0, row=0)

website = tk.Label(text="Website:", bg=back_ground, highlightthickness=0, font=(FONT_NAME, 12, "bold"), fg="Green")
website.config(padx=8, pady=8)
website.grid(column=0, row=1)

web_entry = tk.Entry(width=32)
web_entry.grid(column=1, row=1, )
web_entry.focus()

username = tk.Label(text="Email/Username:", bg=back_ground, font=(FONT_NAME, 12, "bold"), highlightthickness=0,
                    fg="Green")
username.grid(column=0, row=2)

username_entry = tk.Entry(width=67)
username_entry.grid(column=1, row=2, columnspan=2)

# past_mail inserts previously used emails 
if past_mail():
    username_entry.insert(0, past_mail())

password = tk.Label(text="Password:", bg=back_ground, highlightthickness=0, font=(FONT_NAME, 12, "bold"), fg="Green")
password.config(pady=8, padx=8)
password.grid(column=0, row=3)

password_entry = tk.Entry(width=32)
password_entry.grid(column=1, row=3)

generate_button = tk.Button(text="Generate Password", width=19, bg=back_ground, highlightthickness=0, fg="Green",
                            font=(FONT_NAME, 12, "bold"), command=generator)
generate_button.grid(column=2, row=3)

add_button = tk.Button(text=" Add", width=40, highlightthickness=0, fg="Green", bg=back_ground,
                       font=(FONT_NAME, 12, "bold"), command=upload)
add_button.grid(column=1, row=4, columnspan=2)


search_button = tk.Button(text="Search", width=19, highlightthickness=0, fg="Green", bg=back_ground,
                       font=(FONT_NAME, 12, "bold"), command=search)
search_button.grid(column=2, row=1)

window.mainloop()

"""
░█▀█░█▀█░█░█
░█▀▀░█▀▀░░█░
░▀░░░▀░░░░▀░
"""
