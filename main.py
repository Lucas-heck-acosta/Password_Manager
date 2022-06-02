from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

BLACK = "#000000"
PURPLE = "#5800FF"
ORANGE = "#FFA500"
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
# These characters will be used to create the random password
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)
# random amount of each
    password_letters = [random.choice(letters) for _ in range(0, nr_letters)]
    password_numbers = [random.choice(numbers) for _ in range(0, nr_numbers)]
    password_symbols = [random.choice(symbols) for _ in range(0, nr_symbols)]
    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)

    password = "".join(password_list)
    txt_password.delete(0, 'end')
    txt_password.insert(0, f"{password}")
    pyperclip.copy(password)  # copy to clipboard
# on press the random characters are selected, joined together and shuffled. result is printed on the password entry box
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_data():

    # save the given data on a json file
    website = txt_website.get().lower()
    email = txt_email.get().lower()
    password = txt_password.get()
    new_entry = {
        website: {
            "email": email,
            "password": password
        }
    }
    # getting inputs and making a dictionary format

    # check for empty fields
    if txt_website.get() == '' or txt_password.get() == '':
        messagebox.showwarning(title="Warning", message="Empty fields.")
    else:
        cont = messagebox.askokcancel(title="Confirmation" , message=f"Data entered:\n Website: {website} Email: {email}\n"
                                                              f" Password: {password}")
        # check with user if values are correct
        if cont:
            try:
                with open("data.json", "r") as file:  # try to open file
                    data = json.load(file)

            except FileNotFoundError:
                with open("data.json", 'w') as file:  # if not found, create it
                    json.dump(new_entry, file, indent=4)

            else:
                data.update(new_entry)
                with open("data.json", 'w') as file:  # if found, load entry at json file
                    json.dump(data, file, indent=4)

            finally:                                  # clear entry fields
                txt_website.delete(0, 'end')
                txt_password.delete(0, 'end')

# ---------------------------- SEARCH ------------------------------- #


def search():
    # search on file for a website and return values if found
    website = txt_website.get().lower()  # user input
    with open("data.json", 'r') as file:  # open file
        data = json.load(file)
        try:                                # try to find matching website
            messagebox.showinfo(title=f"Login for {website}:", message=f"Email: {data[website]['email']}\n"
                                                                        f"Password: {data[website]['password']}")
        except KeyError or FileNotFoundError:       # print error if not found
            messagebox.showerror(title="Error", message="Website not found")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(pady=45, padx=45, bg=BLACK)

canvas = Canvas(width=145, height=145, bg=BLACK, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(65, 65, image=logo)
canvas.grid(column=1, row=0)

lbl_website = Label(text="Website:", fg=PURPLE, bg=BLACK)
lbl_website.grid(column=0, row=1)


lbl_email = Label(text="Email/Username:", fg=PURPLE, bg=BLACK)
lbl_email.grid(column=0, row=2)


lbl_password = Label(text="Password:", fg=PURPLE, bg=BLACK)
lbl_password.grid(column=0, row=3)


txt_website = Entry(fg=ORANGE, bg=PURPLE, width=21)
txt_website.grid(column=1, row=1)
txt_website.focus()

txt_email = Entry(fg=ORANGE, bg=PURPLE,  width=40)
txt_email.grid(column=1, row=2, columnspan=2)
txt_email.insert(0, "lucas.heck@live.com")

txt_password = Entry(fg=ORANGE, bg=PURPLE,  width=21)
txt_password.grid(column=1, row=3)

btn_search = Button(text="Search", bg=ORANGE, fg=PURPLE, command=search, width=15)
btn_search.grid(column=2, row=1)

btn_generate = Button(text="Generate Password", bg=ORANGE, fg=PURPLE, command=generate_pass, width=15)
btn_generate.grid(column=2, row=3)

btn_add = Button(text="Add", bg=ORANGE, fg=PURPLE, width=33, command=save_data)
btn_add.grid(column=1, row=4, columnspan=2)


window.mainloop()