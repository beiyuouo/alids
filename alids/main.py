#!/usr/bin/env python
# -*- encoding: utf-8 -*-
""" 
@File    :   alids\main.py 
@Time    :   2022-01-20 00:44:48 
@Author  :   Bingjie Yan 
@Email   :   bj.yan.pa@qq.com 
@License :   Apache License 2.0 
"""

import os
import tkinter as tk

from alids.gui import App
from alids.core import Client


def launch_app():
    root = tk.Tk()
    root.title("Alids")

    # Simply set the theme
    root.tk.call("source", os.path.join('.', 'alids', 'ui', 'sun_valley', 'sun-valley.tcl'))
    root.tk.call("set_theme", "dark")

    app = App(root)
    app.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate))

    root.mainloop()


if __name__ == "__main__":
    launch_app()
