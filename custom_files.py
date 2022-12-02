import os
import shutil
import zipfile
import json
from Gui import *
from main import ChangeFont

directory = "temp"
parent_dir = "files/temp"
path = os.path.join(parent_dir, directory)


def create_file(pth):
    path = str(pth.rsplit("/", 1)[0])
    file_name = str(pth.split("/")[-1]).replace(".own", "")
    working_path = path + "/temp"

    try:
        os.mkdir(working_path)
    except Exception:
        pass
    with open(f"{working_path}/text.txt", "w") as file:
        file.write("")
    with open(f"{working_path}/options.json", "w"):
        pass

    shutil.make_archive(f"{path}/{file_name}", format='zip', root_dir=working_path)
    shutil.rmtree(working_path)

    name = os.path.splitext(f"{path}/{file_name}.zip")[0]
    os.rename(f"{path}/{file_name}.zip", name + ".own")


def unpack():
    with zipfile.ZipFile("Z:/test.own", 'r') as zip_ref:
        zip_ref.extractall("Z:/")


def open_custom(pth):
    def load_content():
        with open(f"{working_path}/text.txt", "r") as file:
            data = file.read()
            input_label.delete(1.0, END)
            input_label.insert(END, data)

    def load_styles():
        try:
            with open(f"{working_path}/options.json", "r") as f:
                jsonObject = json.load(f)
                tag_names = jsonObject["tags"]
                start_indices = jsonObject["start_index"]
                end_indices = jsonObject["end_index"]
                background_colors = jsonObject["background_colors"]
                foreground_colors = jsonObject["foreground_colors"]
        except Exception:
            return

        for idx, item in enumerate(end_indices):
            try:
                end_indices[idx] = float(end_indices[idx])
            except ValueError:
                pass

        for idx, item in enumerate(start_indices):
            try:
                start_indices[idx] = float(start_indices[idx])
            except ValueError:
                pass

        for index, tag in enumerate(tag_names):
            if tag == "sel":
                continue
            else:
                input_label.tag_add(tag, start_indices[index], end_indices[index])

        try:
            for index, tag in enumerate(input_label.tag_names(index=None)):
                if tag == "sel":
                    continue
                else:
                    input_label.tag_configure(tag, selectbackground=input_label.cget("selectbackground"))
                    if foreground_colors[index] != "":
                        input_label.tag_configure(tag, foreground=foreground_colors[index])
                    if background_colors[index] != "":
                        input_label.tag_configure(tag, background=background_colors[index])

        except IndexError:
            pass

        ChangeFont.load(len(tag_names) - 1)

    path = str(pth.rsplit("/", 1)[0])
    file_name = str(pth.split("/")[-1]).replace(".own", "")
    working_path = path + "/temp"


    with zipfile.ZipFile(f"{path}/{file_name}.own", 'r') as zip_ref:
        os.mkdir(working_path)
        zip_ref.extractall(path=working_path)
    os.remove(f"{path}/{file_name}.own")

    load_content()
    load_styles()

    shutil.make_archive(f"{path}/{file_name}", format='zip', root_dir=working_path)
    shutil.rmtree(working_path)

    name = os.path.splitext(f"{path}/{file_name}.zip")[0]
    os.rename(f"{path}/{file_name}.zip", name + ".own")


def save_custom(pth):
    def save_content():
        with open(f"{working_path}/text.txt", "w") as file:
            file.write(input_label.get(1.0, END))

    def save_styles():
        tags = input_label.tag_names(index=None)
        tag_names = []
        start_indices = []
        end_indices = []
        background_colors = []
        fg_colors = []
        for tag in tags:
            try:
                tag_name = tag
                index_start = input_label.tag_ranges(tag)[0]
                end_index = input_label.tag_ranges(tag)[1]
                background_color = input_label.tag_cget(tag_name, "background")
                foreground_color = input_label.tag_cget(tag_name, "foreground")

            except IndexError:
                tag_name = tag
                index_start = input_label.tag_ranges(tag)
                end_index = input_label.tag_ranges(tag)
                background_color = input_label.tag_cget(tag_name, "background")
                foreground_color = input_label.tag_cget(tag_name, "foreground")

            tag_names.append(tag_name)
            start_indices.append(str(index_start))
            end_indices.append(str(end_index))
            background_colors.append(background_color)
            fg_colors.append(foreground_color)

        with open(f"{working_path}/options.json", "w") as f:
            data = {"tags": tag_names,
                    "start_index": start_indices,
                    "end_index": end_indices,
                    "background_colors": background_colors,
                    "foreground_colors": fg_colors
                    }
            json.dump(data, f, indent=4)

    path = str(pth.rsplit("/", 1)[0])
    file_name = str(pth.split("/")[-1]).replace(".own", "")
    working_path = path + "/temp"

    with zipfile.ZipFile(f"{path}/{file_name}.own", 'r') as zip_ref:
        os.mkdir(working_path)
        zip_ref.extractall(path=working_path)
    os.remove(f"{path}/{file_name}.own")

    save_styles()
    save_content()

    shutil.make_archive(f"{path}/{file_name}", format='zip', root_dir=working_path)
    shutil.rmtree(working_path)

    name = os.path.splitext(f"{path}/{file_name}.zip")[0]
    os.rename(f"{path}/{file_name}.zip", name + ".own")


if __name__ == '__main__':
    pass
