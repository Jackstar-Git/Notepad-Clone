from Gui import window, input_label, font
from Gui import *
from settings import read_values, write

from tkinter import *

import pyperclip
from tkinter.filedialog import *
from datetime import *
from tkinter import messagebox

read_values()
path = ""


def save():
    global path
    try:
        with open(path, "w") as file:
            file.write(input_label.get("1.0", END))
    except FileNotFoundError:
        new_file()
        pass

    window.title(path)


def open_file():
    global path
    path = askopenfilename(initialdir="files/",
                           filetypes=(('Text files', "*.txt"), ("JSON files", "*json"), ('All files', '*.*')))
    with open(path, "r") as file:
        content = file.read()
    input_label.delete(1.0, END)
    input_label.insert(1.0, content)

    window.title(path)


def new_file():
    global path
    try:
        path = asksaveasfilename()
        with open(path, "w") as file:
            file.write("")
            window.title(path)
    except FileNotFoundError:
        pass


def cut():
    try:
        cut_string = input_label.selection_get()
    except TclError:
        return
    pyperclip.copy(cut_string)
    input_label.delete(f"end-{len(input_label.selection_get()) + 1}c", END)

    window.title(path)


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
    data = input_label.get("1.0", END).strip().split(" ")
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


def unzoom():
    unzoom_factor = font.cget("size")
    unzoom_factor -= 1
    font.config(size=unzoom_factor)


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


if __name__ == '__main__':
    main_func()
