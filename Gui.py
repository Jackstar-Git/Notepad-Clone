from tkinter import *
from pynput import mouse
from tkinter import font as ft
import keyboard

window = Tk()



def place_window():
    window_height = 470
    window_width = 1200

    screen_height = window.winfo_screenheight()
    screen_width = window.winfo_screenwidth()

    y_position = int((screen_height - window_height) / 2.35)
    x_position = int((screen_width - window_width) / 2)

    window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")


place_window()

font = ft.Font(family="Arial", size=12)


def scroll_Handler(*length):
    op, howmany = length[0], length[1]

    if op == 'scroll':
        units = length[2]
        input_label.xview_scroll(howmany, units)
    elif op == 'moveto':
        input_label.xview_moveto(howmany)


def focus_on(event):
    add_hotkeys()
    return event


def focus_off(event):
    keyboard.unhook_all_hotkeys()
    return event


for i in range(1, 26):
    window.rowconfigure(i, weight=1)
for i in range(15):
    window.columnconfigure(i, weight=1)

frame = Frame(window, width=1100, height=450)
scrollbar = Scrollbar(window, orient="vertical", command=scroll_Handler)
scrollbar_sideways = Scrollbar(window, orient="horizontal", command=scroll_Handler)
frame.pack_propagate(False)
frame.grid(column=0, row=1, columnspan=15, rowspan=25, sticky="nsew")
input_label = Text(frame, font=font, width=1, height=1, wrap=NONE, xscrollcommand=scrollbar_sideways.set,
                   yscrollcommand=scrollbar.set)
input_label.pack(expand=True, fill="both")

from main import ChangeFont
from main import *

scrollbar.grid(row=0, rowspan=26, column=15, sticky="nse")
scrollbar.config(command=input_label.yview)
scrollbar_sideways.grid(row=26, columnspan=25, column=0, sticky="wes")
scrollbar_sideways.config(command=input_label.xview)


from settings import reset_settings
menu = Menu(window)
window.config(menu=menu)
filemenu = Menu(menu, tearoff=0)
filemenu.add_command(label="New", command=new_file, accelerator="Ctrl+N")
filemenu.add_command(label="Save", command=save, accelerator="Ctrl+S")
filemenu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=lambda: window.destroy(), accelerator="Alt+F4")
editmenu = Menu(menu, tearoff=0)
editmenu.add_command(label="Cut", command=cut, accelerator="Ctrl+X")
editmenu.add_command(label="Copy", command=copy, accelerator="Ctrl+C")
editmenu.add_command(label="Paste", command=paste, accelerator="Ctrl+V")
editmenu.add_separator()
editmenu.add_command(label="Replace", command=replace, accelerator="Ctrl+R")
editmenu.add_command(label="Lorem Ipsum", command=loremipsum, accelerator="Ctrl+L")
editmenu.add_separator()
editmenu.add_command(label="Date", command=get_date, accelerator="Ctrl+Shift+D")
editmenu.add_command(label="Time", command=get_time, accelerator="Ctrl+Shift+T")
inspectmenu = Menu(menu, tearoff=0)
inspectmenu_encryption = Menu(inspectmenu, tearoff=0)
inspectmenu.add_cascade(label="File-Encryption", menu=inspectmenu_encryption)
inspectmenu_encryption.add_command(label="Encrypt File", command=encrypt)
inspectmenu_encryption.add_command(label="Decrypt File", command=decrypt)
inspectmenu.add_command(label="Count Words", command=count_words, accelerator="Ctrl+Shift+C")
viewmenu = Menu(menu, tearoff=0)
viewmenu_font = Menu(viewmenu, tearoff=0)
viewmenu.add_cascade(label="Global Font Settings", underline=0, menu=viewmenu_font)
viewmenu_font.add_command(label="Change Font Size", command=change_font_size)
viewmenu_font.add_command(label="Change Font Style", command=change_font_style)
viewmenu_font.add_command(label="Change Font Color", command=change_global_font_color)
viewmenu.add_command(label="Change Background", command=change_background)
viewmenu.add_command(label="Change Selection Color", command=change_selection_background)
viewmenu.add_separator()
viewmenu.add_command(label="Change Marked Font Color", command=ChangeFont.change_selected_color)
viewmenu.add_command(label="Highlight Marked Text", command=ChangeFont.change_selected_background)
viewmenu.add_command(label="Change Highlighted Font", command=ChangeFont.change_selected_font_style)
helpmenu = Menu(menu, tearoff=0)
helpmenu.add_command(label="Open GitHub", command=open_github)
helpmenu.add_command(label="Reset to Default-Settings", command=reset_settings, accelerator="Ctrl+Shift+R")
menu.add_cascade(label="File", menu=filemenu)
menu.add_cascade(label="Edit", menu=editmenu)
menu.add_cascade(label="Inspect", menu=inspectmenu)
menu.add_cascade(label="View", menu=viewmenu)
menu.add_cascade(label="Help", menu=helpmenu)
input_label.bind("<FocusOut>", focus_off)
input_label.bind("<FocusIn>", focus_on)
input_label.bind("<Key>", check_unsaved)


def add_hotkeys():
    from settings import reset_settings
    keyboard.add_hotkey("ctrl + n", new_file)
    keyboard.add_hotkey('ctrl + s', save)
    keyboard.add_hotkey("ctrl + o", open_file)
    keyboard.add_hotkey("ctrl + r", replace)
    keyboard.add_hotkey("ctrl + l", loremipsum)
    keyboard.add_hotkey("ctrl + shift + d", get_date)
    keyboard.add_hotkey("ctrl + shift + t", get_time)
    keyboard.add_hotkey("ctrl + shift + c", count_words)
    keyboard.add_hotkey("ctrl + shift + r", reset_settings)

    def on_scroll(x_cords, y_cords, dx, dy):
        if dy > 0 and keyboard.is_pressed("ctrl"):
            zoom()
        elif dy < 0 and keyboard.is_pressed("ctrl"):
            unzoom()
        else:
            return x_cords, y_cords, dx

    listener = mouse.Listener(on_scroll=on_scroll)
    listener.start()



window.protocol("WM_DELETE_WINDOW", on_closing)


def main_func():
    window.title("UnsavedFile")
    icon = PhotoImage(file="src/icon.png")
    window.iconphoto(False, icon)
    window.mainloop()

