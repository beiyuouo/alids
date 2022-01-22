import os
import io
from PIL import Image, ImageTk
from urllib.request import urlopen


def get_path(path: str):
    if path.startswith("~"):
        return os.path.expanduser(path)
    else:
        return path


def list_dir(path: str):
    return os.listdir(get_path(path))


def treeview_dir(path: str):
    dirs = list_dir(path)

    treeview_data = [("", 1, path, ("", ""))]

    for index, dir in enumerate(dirs):
        if os.path.isdir(os.path.join(path, dir)):
            treeview_data.append((1, index + 2, dir, ("", "")))
        else:
            # file size
            size = os.path.getsize(os.path.join(path, dir))
            # file edit time
            time = os.path.getmtime(os.path.join(path, dir))
            treeview_data.append((1, index + 2, dir, (size, time)))

    return treeview_data


def treeview_alidir(path: str, items):
    treeview_data = [("", 1, path, ("", ""))]

    for item in items:
        if item["type"] == "folder":
            treeview_data.append((1, len(treeview_data) + 1, item["name"], ("", "")))
        else:
            # file size
            size = "unknown"
            # file edit time
            time = item["updated_at"].split("T")[0]
            treeview_data.append((1, len(treeview_data) + 1, item["name"], (size, time)))

    return treeview_data


def get_tkimage(url: str):
    image_bytes = urlopen(url).read()
    data_stream = io.BytesIO(image_bytes)
    pil_image = Image.open(data_stream)
    tk_image = ImageTk.PhotoImage(pil_image)
    tk_image = ImageTk.PhotoImage(pil_image.resize((30, 30)))
    return tk_image