import tkinter.colorchooser

import keyboard
from cryptography.fernet import Fernet
from Gui import window, font, input_label
from Gui import *
from settings import read_values, write

from tkinter import *

import pyperclip
from tkinter.filedialog import *
from datetime import *
from tkinter import messagebox
from tkinter.colorchooser import askcolor

read_values()
path = ""


class ChangeFont:
    tag_number = 0

    @classmethod
    def load(cls, num):
        cls.tag_number = num

    @classmethod
    def add_tag(cls):
        try:
            input_label.tag_add(f"tag{cls.tag_number}", "sel.first", "sel.last")
            cls.tag_number += 1
        except TclError:
            return

    @classmethod
    def change_selected_color(cls):
        try:
            input_label.selection_get()
        except TclError:
            return
        try:
            color = askcolor(color=input_label.cget("foreground"))
            font_color = color[1]
            cls.add_tag()
            tag_name = input_label.tag_names()[cls.tag_number]
            input_label.tag_configure(tag_name, foreground=font_color)
        except TclError:
            return

    @classmethod
    def change_selected_background(cls):
        try:
            input_label.selection_get()
        except TclError:
            return
        try:
            color = askcolor(color=input_label.cget("background"))
            bg_color = color[1]
            cls.add_tag()
            tag_name = input_label.tag_names()[cls.tag_number]
            input_label.tag_configure(tag_name, background=bg_color)
        except TclError:
            return

    @classmethod
    def change_selected_font_style(cls):
        try:
            input_label.selection_get()
        except TclError:
            return
        try:
            temp_font = ft.Font(family="Arial", size=12)
            cls.add_tag()
            tag_name = input_label.tag_names()[cls.tag_number]

            def set_font_style(f):
                temp_font.config(family=font_list.get(font_list.curselection()))
                return f

            def ok():
                input_label.tag_configure(tag_name, font=temp_font)
                write()
                top.destroy()

            def cancel():
                font.config(family=old_value)
                top.destroy()

            old_value = font.cget("family")

            top = Toplevel(window)
            top.resizable(False, False)
            font.config(size=15)

            font_container_frame = Frame(top, width=440, height=125)
            font_container_frame.grid(column=0, row=0, rowspan=3, columnspan=4)
            font_container_frame.grid_propagate(False)

            my_text = Text(font_container_frame, font=temp_font)
            my_text.grid(row=0, column=0)
            my_text.delete(1.0, END)
            my_text.insert(END,
                           "The big brown fox jumps over the lazy "
                           "dog!\n\nabcdefghijklmnopqrstuvwxyz\nABCDEFGHIJKLMNOPQRSTUVWXYZ "
                           "\n0123456789")
            my_text.config(state="disabled")

            font_list = Listbox(top, selectmode=SINGLE)

            scrollbar_fonts = Scrollbar(top)
            scrollbar_fonts.grid(row=3, column=3, rowspan=3, columnspan=1, sticky="nse")

            font_list.grid(columnspan=4, rowspan=3, column=0, row=3, sticky="we")
            font_list.config(yscrollcommand=scrollbar_fonts.set)

            scrollbar_fonts.config(command=font_list.yview)

            ok_button = Button(top, text="OK", command=ok)
            ok_button.grid(row=7, column=0, columnspan=2, sticky="we")
            cancel_button = Button(top, text="Cancel", command=cancel)
            cancel_button.grid(row=7, column=2, columnspan=2, sticky="we")

            for fonts in ft.families():
                font_list.insert(END, fonts)

            font_list.bind("<<ListboxSelect>>", set_font_style)
        except TclError:
            return



def save():
    from custom_files import save_custom
    global path
    temp_path = path
    try:
        try:
            file_ending = str(temp_path.split(".")[1])
        except IndexError:
            file_ending = ""
            new_file()

        if file_ending == "own":
            save_custom(temp_path)
            window.title(path)
        else:
            try:
                with open(path, "w") as file:
                    file.write(input_label.get("1.0", END))
                window.title(path)
            except FileNotFoundError:
                new_file()
                with open(path, "w") as file:
                    file.write(input_label.get("1.0", END))
                window.title("UnsavedFile")
    except Exception:
        pass


def open_file():
    from Gui import inspectmenu
    from custom_files import open_custom
    global path
    try:
        path = askopenfilename(initialdir="files/",
                               filetypes=(('Text files', "*.txt"), ("JSON files", "*json"), ("Custom Files", "*.own"),
                                          ('All files', '*.*')))
        file_ending = ""
        try:
            file_ending = str(path.split(".")[1])
        except IndexError:
            path += ".txt"
        if file_ending == "own":
            open_custom(path)
            inspectmenu.entryconfig("File-Encryption", state="disabled")
        else:
            inspectmenu.entryconfig("File-Encryption", state="normal")
            with open(path, "r") as file:
                content = file.read()
            input_label.delete(1.0, END)
            input_label.insert(1.0, content)

        window.title(path)
    except FileNotFoundError:
        pass


def new_file():
    from Gui import inspectmenu
    from custom_files import create_file
    global path
    try:
        path = asksaveasfilename()
        file_ending = ""
        if path == "":
            return
        try:
            file_ending = str(path.split(".")[1])
        except IndexError:
            new_file()

        if file_ending == "own":
            create_file(path)
            inspectmenu.entryconfig("File-Encryption", state="disabled")

        elif file_ending == "txt":
            inspectmenu.entryconfig("File-Encryption", state="normal")
            with open(path, "w") as file:
                file.write("")
        window.title(path)
        input_label.delete(1.0, END)
    except FileNotFoundError:
        pass


def cut():
    try:
        cut_string = input_label.selection_get()
        pyperclip.copy(cut_string)
        input_label.delete("sel.first", "sel.last")
    except TclError:
        return


def copy():
    try:
        copy_string = input_label.selection_get()
    except TclError:
        return
    pyperclip.copy(copy_string)


def paste():
    input_label.insert(END, pyperclip.paste())


def replace():
    def ok():
        replacement = replacement_input.get(1.0, END).replace("\n", "")
        replace_to = replacement_to_input.get(1.0, END).replace("\n", "")

        data = input_label.get(1.0, END)
        new_data = data.replace(replacement, replace_to)
        input_label.delete(1.0, END)
        input_label.insert(END, new_data)

    def cancel():
        top.destroy()

    top = Toplevel(window)
    replacement_label = Label(top, text="Replace: ", width=10, anchor="w")
    replacement_label.grid(columnspan=1, rowspan=1, row=0, column=0, sticky=W)
    replacement_input = Text(top, width=40, height=2)
    replacement_input.grid(row=1, rowspan=2, columnspan=4, column=0)
    replacement_to_label = Label(top, text="With: ", width=10, anchor="w")
    replacement_to_label.grid(columnspan=1, rowspan=1, row=3, column=0, sticky=W)
    replacement_to_input = Text(top, width=40, height=2)
    replacement_to_input.grid(row=4, rowspan=2, columnspan=4, column=0)

    button_ok = Button(top, text="OK", width=22, command=ok)
    button_ok.grid(row=6, columnspan=2, column=0, sticky=W)
    button_cancel = Button(top, text="Cancel", width=22, command=cancel)
    button_cancel.grid(row=6, columnspan=2, column=2, sticky=E)


def get_date():
    current_date = date.today()
    current_date = current_date.strftime("%d. %B %Y")
    input_label.insert(END, current_date)


def get_time():
    current_time = datetime.now()
    current_time = current_time.strftime("%H:%M:%S")
    input_label.insert(END, current_time)


def count_words():
    data = input_label.get("1.0", END).strip().replace("\n", "").split(" ")
    symbols = list(input_label.get("1.0", END).strip())
    messagebox.showinfo("Count", f"Word Count:\n{len(data)}\n\n Symbol Count\n{len(symbols)}")


def change_font_size():
    def ok():
        try:
            size = int(size_label.get())
            font.config(size=size)
            write()
            top.destroy()
        except ValueError:
            messagebox.showerror("Error!", "The entered Value must be a whole number!")
            change_font_size()

    def cancel():
        font.config(size=old_value)
        top.destroy()

    def increase():
        try:
            size = int(size_label.get())
            size += 1
            size_label.delete(0, END)
            size_label.insert(END, str(size))
            font.config(size=size)
        except ValueError:
            messagebox.showerror("Error!", "The entered Value must be a whole number!")
            change_font_size()

    def decrease():
        try:
            size = int(size_label.get())
            size -= 1
            size_label.delete(0, END)
            size_label.insert(END, str(size))
            font.config(size=size)
        except ValueError:
            messagebox.showerror("Error!", "The entered Value must be a whole number!")
            change_font_size()

    top = Toplevel(window)

    size_label = Entry(top, width=12, font=("Arial", 13))
    size_label.grid(column=0, row=0, columnspan=3, rowspan=2, sticky="ns")
    size_label.insert(END, font.cget("size"))

    button_up = Button(top, text="\u25B2", width=4, command=increase)
    button_up.grid(row=0, column=3)

    button_down = Button(top, text="\u25BC", width=4, command=decrease)
    button_down.grid(row=1, column=3)

    ok_button = Button(top, text="OK", command=ok)
    ok_button.grid(row=2, column=0, columnspan=2, sticky="we")
    cancel_button = Button(top, text="Cancel", command=cancel)
    cancel_button.grid(row=2, column=2, columnspan=2, sticky="we")

    old_value = int(size_label.get())


def change_font_style():
    temp_font = ft.Font(family="Arial", size=12)

    def set_font_style(f):
        temp_font.config(family=font_list.get(font_list.curselection()))
        return f

    def ok():
        font.config(family=str(temp_font.cget("family")))
        write()
        top.destroy()

    def cancel():
        font.config(family=old_value)
        top.destroy()

    old_value = font.cget("family")

    top = Toplevel(window)
    top.resizable(False, False)
    font.config(size=15)

    font_container_frame = Frame(top, width=440, height=125)
    font_container_frame.grid(column=0, row=0, rowspan=3, columnspan=4)
    font_container_frame.grid_propagate(False)

    my_text = Text(font_container_frame, font=temp_font)
    my_text.grid(row=0, column=0)
    my_text.delete(1.0, END)
    my_text.insert(END,
                   "The big brown fox jumps over the lazy "
                   "dog!\n\nabcdefghijklmnopqrstuvwxyz\nABCDEFGHIJKLMNOPQRSTUVWXYZ "
                   "\n0123456789")
    my_text.config(state="disabled")

    font_list = Listbox(top, selectmode=SINGLE)

    scrollbar_fonts = Scrollbar(top)
    scrollbar_fonts.grid(row=3, column=3, rowspan=3, columnspan=1, sticky="nse")

    font_list.grid(columnspan=4, rowspan=3, column=0, row=3, sticky="we")
    font_list.config(yscrollcommand=scrollbar_fonts.set)

    scrollbar_fonts.config(command=font_list.yview)

    ok_button = Button(top, text="OK", command=ok)
    ok_button.grid(row=7, column=0, columnspan=2, sticky="we")
    cancel_button = Button(top, text="Cancel", command=cancel)
    cancel_button.grid(row=7, column=2, columnspan=2, sticky="we")

    for fonts in ft.families():
        font_list.insert(END, fonts)

    font_list.bind("<<ListboxSelect>>", set_font_style)


def zoom():
    zoom_factor = font.cget("size")
    zoom_factor += 1
    font.config(size=zoom_factor)

    for tag in input_label.tag_names(index=None):
        input_label.tag_configure(tag, font=font)


def unzoom():
    unzoom_factor = font.cget("size")
    unzoom_factor -= 1
    font.config(size=unzoom_factor)

    for tag in input_label.tag_names(index=None):
        input_label.tag_configure(tag, font=font)


def loremipsum():
    def copy_to_clip():
        try:
            amount = int(character_input.get())
            with open("src/loremipsum.txt", "r") as f:
                data = f.read()
                data_string = data[0:amount]
                pyperclip.copy(data_string)
                messagebox.showinfo("Info", "Copied to Clipboard!")
            top.destroy()
        except ValueError:
            messagebox.showerror("Error!", "Your input must be a number!")
            top.destroy()
            loremipsum()

    def insert():
        try:
            amount = int(character_input.get())
            with open("src/loremipsum.txt", "r") as f:
                data = f.read()
                data_string = data[0:amount]
                input_label.insert(END, data_string)
            top.destroy()
        except ValueError:
            messagebox.showerror("Error!", "Your input must be a number!")
            top.destroy()
            loremipsum()

    def cancel():
        top.destroy()

    top = Toplevel(window)

    text_label = Label(top, text="Number of characters:", font=("Arial", 13))
    text_label.grid(column=0, row=0, columnspan=3, sticky="w")

    character_input = Entry(top, font=("Arial", 15))
    character_input.grid(row=1, column=0, columnspan=3, sticky="we")

    button_copy = Button(top, text="Copy to Clipboard", command=copy_to_clip)
    button_copy.grid(row=2, column=0, sticky="we")

    button_insert = Button(top, text="Insert", command=insert)
    button_insert.grid(row=2, column=1, sticky="we")

    button_cancel = Button(top, text="Cancel", command=cancel)
    button_cancel.grid(row=2, column=2, sticky="we")


def change_global_font_color():
    color = askcolor(color=input_label.cget("foreground"))
    try:
        font_color = color[1]
        input_label.config(fg=font_color, insertbackground=font_color)
        write()
    except TclError:
        pass


def change_background():
    color = askcolor(color=input_label.cget("background"))
    try:
        background_color = color[1]
        input_label.config(bg=background_color)
        write()
    except TclError:
        pass


def change_selection_background():
    color = askcolor(color=input_label.cget("selectbackground"))
    try:
        selection_color = color[1]
        input_label.config(selectbackground=selection_color)
        write()
    except TclError:
        pass


def check_unsaved(x):
    try:
        with open(path, "r") as file:
            old_content = file.read()

        new_content = input_label.get(1.0, END)[:-1]

        if old_content != new_content:
            window.title(f"* {path}")
        else:
            window.title(f"{path}")

    except FileNotFoundError:
        pass


def encrypt():
    fernet = Fernet(b'7ECn-fAsAZKZCX24dZKSoGd0uWy7eO6expx1aDn7Tyk=')

    with open(path, "rb") as check:
        check_message = check.read().decode()
    with open(path, "r") as check:
        check_message1 = check.read()

    if check_message1 == check_message:
        messagebox.showerror("Error!", "You cannot encrypt an already encrypted file!")
    else:
        with open(path, "r") as file:
            message = file.read()
        encrypted_message = fernet.encrypt(message.encode())
        with open(path, "wb") as file:
            file.write(encrypted_message)
        with open(path, "r") as enc_file:
            encrypted = enc_file.read()
        input_label.delete(1.0, END)
        input_label.insert(END, encrypted)


def decrypt():
    fernet = Fernet(b'7ECn-fAsAZKZCX24dZKSoGd0uWy7eO6expx1aDn7Tyk=')

    with open(path, "rb") as check:
        check_message = check.read().decode()
    with open(path, "r") as check:
        check_message1 = check.read()

    if check_message1 != check_message:
        messagebox.showerror("Error!", "This file is already decrypted!")
    else:

        with open(path, "rb") as enc_file:
            encrypted = enc_file.read()

        decrypted = fernet.decrypt(encrypted)
        decrypted = decrypted.decode()

        input_label.delete(1.0, END)
        input_label.insert(END, decrypted)

        with open(path, "w") as file:
            file.write(decrypted)


def open_github():
    import webbrowser
    webbrowser.open("https://github.com/Jackstar-Git")


def on_closing():
    global path

    def dialog():
        answer = messagebox.askyesnocancel("Unsaved Changes", "You have unsaved changes!\n Do you want to save them?",
                                           icon="warning")
        if answer:
            save()
            window.destroy()
        elif answer is None:
            pass
        else:
            window.destroy()

    try:
        with open(path, "r") as file:
            old_content = file.read()
        new_content = input_label.get(1.0, END)[:-1]

        if old_content != new_content:
            dialog()
        else:
            window.destroy()

    except FileNotFoundError:
        dialog()
    except UnicodeDecodeError:
        window.destroy()
    else:
        pass


if __name__ == '__main__':
    main_func()
