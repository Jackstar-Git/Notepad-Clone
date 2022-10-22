from tkinter import *
from pynput import mouse
from tkinter import font as ft
import keyboard


window = Tk()
window.title("UnsavedFile")

font = ft.Font(family="Arial", size=12)





def add_hotkeys():
    keyboard.add_hotkey('ctrl + s', save)
    keyboard.add_hotkey("ctrl + o", open_file)
    keyboard.add_hotkey("ctrl + r", replace)
    keyboard.add_hotkey("ctrl + shift + d", get_date)
    keyboard.add_hotkey("ctrl + shift + t", get_time)
    keyboard.add_hotkey("ctrl + 2", unzoom)

    def on_scroll(x_cords, y_cords, dx, dy):
        if dy > 0 and keyboard.is_pressed("ctrl"):
            zoom()
        elif dy < 0 and keyboard.is_pressed("ctrl"):
            unzoom()
        else:
            return x_cords, y_cords, dx

    listener = mouse.Listener(on_scroll=on_scroll)
    listener.start()


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

from main import *

scrollbar.grid(row=0, rowspan=26, column=15, sticky="nse")
scrollbar.config(command=input_label.yview)
scrollbar_sideways.grid(row=26, columnspan=25, column=0, sticky="wes")
scrollbar_sideways.config(command=input_label.xview)
menu = Menu(window)
window.config(menu=menu)
filemenu = Menu(menu, tearoff=0)
filemenu.add_command(label="New", command=new_file)
filemenu.add_command(label="Save", command=save)
filemenu.add_command(label="Open", command=open_file)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit)
editmenu = Menu(menu, tearoff=0)
editmenu.add_command(label="Cut", command=cut)
editmenu.add_command(label="Copy", command=copy)
editmenu.add_command(label="Paste", command=paste)
editmenu.add_separator()
editmenu.add_command(label="Replace", command=replace)
editmenu.add_command(label="Lorem Ipsum", command=loremipsum)
editmenu.add_separator()
editmenu.add_command(label="Date", command=get_date)
editmenu.add_command(label="Time", command=get_time)
inspectmenu = Menu(menu, tearoff=0)
inspectmenu.add_command(label="Count Words", command=count_words)
viewmenu = Menu(menu, tearoff=0)
viewmenu_font = Menu(viewmenu, tearoff=0)
viewmenu_font.add_command(label="Change Font Size", command=change_font_size)
viewmenu_font.add_command(label="Change Font Style", command=change_font_style)
viewmenu.add_cascade(label="Change Font", underline=0, menu=viewmenu_font)
menu.add_cascade(label="File", menu=filemenu)
menu.add_cascade(label="Edit", menu=editmenu)
menu.add_cascade(label="Inspect", menu=inspectmenu)
menu.add_cascade(label="View", menu=viewmenu)
input_label.bind("<FocusOut>", focus_off)
input_label.bind("<FocusIn>", focus_on)


def main_func():
    window.mainloop()
