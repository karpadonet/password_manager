from tkinter import *
from  tkinter import messagebox
from random import choice, shuffle, randint
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# this function generates a 15 characters password which contains letters,symbols and numbers
def generate_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]# picking 8 or 10 letters
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]# picking 2-4 symbols
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]# picking 2-4 numbers

    # list that contains all of the possible password characters from above, combining those lists
    password_list = password_letters + password_symbols + password_numbers
    # randomizing the list, making a mix
    shuffle(password_list)
    # creating a string from the password list
    generated_password = "". join(password_list)
    # the password appears in the password entry for the user to see
    pass_input.insert(0, generated_password)
    # passing the password string straight into the clipboard
    pyperclip.copy(generated_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
# this function saves user's input
def save():
    website = web_input.get()
    email = email_input.get()
    password = pass_input.get()
    new_data = { website:{
        "email": email,
        "password": website,

        }
    }
    # checking if there was an input
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="You left an empty field")
    # making sure the details are correct
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details enetered:\n Email: {email}\n"
                                                              f"password: {password}\nIs it ok to save? ")
    if is_ok:
        # if the data is correct we add the new password to a file
        try:# if there is no such a file we will create a new one
            with open("password_manager.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        # creating a new file
        except FileNotFoundError:
            with open("password_manager.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        #if there is no error
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("password_manager.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        # we aleays at the end will delete user's input
        finally:
            web_input.delete(0, END)
            pass_input.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #
# this function finds the assword of a given website in the file
def find_password():
    website = web_input.get()# the value of user's entry
    # if there is no such file we will give the user a message
    try:
        with open("password_manager.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    # if there is no problem we will look for the website in the file
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            # showing the details in the file of a given website
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        # if the file doesn't contain the website
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #
# creating a window
window = Tk()
# creating a title for the window
window.title("Password Manager")
window.config(padx = 50, pady = 50)

# creating a canvas
canvas = Canvas(width=200, height=200)
# adding an image to the canvas
pass_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=pass_img)
# the image appears on our screen
canvas.grid(row = 0, column=1)

# creating a website label
web_label = Label(text="website")
# placing the label
web_label.grid(row =1, column= 0)

# creating a user label
user_label = Label(text="Email/Username")
# placing the label
user_label.grid(row =2, column= 0)

# creating a password label
pass_label = Label(text="password")
# placing the label
pass_label.grid(row =3, column= 0)

# creating an input windows for each label
web_input = Entry(width= 40)
web_input.grid(row=1, column =1, columnspan =2)
web_input.focus()



email_input = Entry(width=40)
email_input.grid(row=2, column=1, columnspan=2)
email_input.insert(0, "shuraspivak@gmail.com")# the entry is prepopulated with my email


pass_input = Entry(width=40)
pass_input.grid(row=3, column = 1, columnspan=2)


#Creating buttons
gen_button = Button(text= "Generate password", command=generate_pass)
# placing the button
gen_button.grid(row=3, column=3)

add_button = Button(text= "Add", width=36, command=save)
# placing the button
add_button.grid(row=4, column=1,columnspan=2)

search_button = Button(text= "Search", width =13, command=find_password)
# placing the button
search_button.grid(row=1, column=3)

window.mainloop()