import json
from Gui import font, input_label


file = "src/settings.json"


def write():
    with open(file, "w") as f:
        data = {"font_size": font.cget("size"),
                "font_style": font.cget("family"),
                "background_color": input_label.cget("background"),
                "foreground_color": input_label.cget("foreground"),
                "selection_background": input_label.cget("selectbackground")
                }

        json.dump(data, f, indent=4)


def read_values():
    try:
        with open(file, "r") as f:
            jsonObject = json.load(f)

            font_size = jsonObject["font_size"]
            font_style = jsonObject["font_style"]
        font.config(size=font_size, family=font_style)

        background_color = jsonObject["background_color"]
        foreground_color = jsonObject["foreground_color"]
        select_background = jsonObject["selection_background"]
        input_label.config(bg=background_color, fg=foreground_color, insertbackground=foreground_color,
                           selectbackground=select_background)

    except:
        write()
        read_values()
