#!/usr/bin/env python
# -*- encoding: utf-8 -*-
""" 
@File    :   alids\gui.py 
@Time    :   2022-01-20 13:38:45 
@Author  :   Bingjie Yan 
@Email   :   bj.yan.pa@qq.com 
@License :   Apache License 2.0 
"""

import os
import tkinter as tk
from tkinter import ttk


class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create value lists

        # Create control variables

        # Create widgets :)
        self.setup_widgets()

    def _insert_treeview_data(self, treeview_data, treeview):
        # Insert treeview data
        for item in treeview_data:
            treeview.insert(parent=item[0],
                            index="end",
                            iid=item[1],
                            text=item[2],
                            values=item[3])
            if item[0] == "" or item[1] in {8, 21}:
                treeview.item(item[1], open=True)  # Open parents

    def setup_widgets(self):
        # Define treeview data
        treeview_data = [
            ("", 1, "Parent", ("Item 1", "Value 1")),
            (1, 2, "Child", ("Subitem 1.1", "Value 1.1")),
            (1, 3, "Child", ("Subitem 1.2", "Value 1.2")),
            (1, 4, "Child", ("Subitem 1.3", "Value 1.3")),
            (1, 5, "Child", ("Subitem 1.4", "Value 1.4")),
            ("", 6, "Parent", ("Item 2", "Value 2")),
            (6, 7, "Child", ("Subitem 2.1", "Value 2.1")),
            (6, 8, "Sub-parent", ("Subitem 2.2", "Value 2.2")),
            (8, 9, "Child", ("Subitem 2.2.1", "Value 2.2.1")),
            (8, 10, "Child", ("Subitem 2.2.2", "Value 2.2.2")),
            (8, 11, "Child", ("Subitem 2.2.3", "Value 2.2.3")),
            (6, 12, "Child", ("Subitem 2.3", "Value 2.3")),
            (6, 13, "Child", ("Subitem 2.4", "Value 2.4")),
            ("", 14, "Parent", ("Item 3", "Value 3")),
            (14, 15, "Child", ("Subitem 3.1", "Value 3.1")),
            (14, 16, "Child", ("Subitem 3.2", "Value 3.2")),
            (14, 17, "Child", ("Subitem 3.3", "Value 3.3")),
            (14, 18, "Child", ("Subitem 3.4", "Value 3.4")),
            ("", 19, "Parent", ("Item 4", "Value 4")),
            (19, 20, "Child", ("Subitem 4.1", "Value 4.1")),
            (19, 21, "Sub-parent", ("Subitem 4.2", "Value 4.2")),
            (21, 22, "Child", ("Subitem 4.2.1", "Value 4.2.1")),
            (21, 23, "Child", ("Subitem 4.2.2", "Value 4.2.2")),
            (21, 24, "Child", ("Subitem 4.2.3", "Value 4.2.3")),
            (19, 25, "Child", ("Subitem 4.3", "Value 4.3")),
        ]

        # Panedwindow
        self.paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned.grid(row=0, column=0, padx=(5, 5), sticky="nsew")

        # Pane #1
        self.pane_local = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_local, weight=2)

        # Scrollbar
        self.scrollbar_local = ttk.Scrollbar(self.pane_local)
        self.scrollbar_local.pack(side="right", fill="y")

        # Treeview
        self.treeview_local = ttk.Treeview(
            self.pane_local,
            selectmode="browse",
            yscrollcommand=self.scrollbar_local.set,
            columns=(1, 2),
            height=10,
        )
        self.treeview_local.pack(expand=True, fill="both")
        self.scrollbar_local.config(command=self.treeview_local.yview)

        # Treeview columns
        self.treeview_local.column("#0", anchor="w", width=120)
        self.treeview_local.column(1, anchor="w", width=120)
        self.treeview_local.column(2, anchor="w", width=120)

        self._insert_treeview_data(treeview_data=treeview_data, treeview=self.treeview_local)

        # Select and scroll
        self.treeview_local.selection_set(10)
        self.treeview_local.see(7)

        # Pane #2
        self.pane_options = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_options, weight=1)

        # Label
        self.label_options = ttk.Label(self.pane_options, text="Options")
        self.label_options.pack(side="top", fill="y")

        # Button
        self.button_options = ttk.Button(self.pane_options, text="Options")
        self.button_options.pack(side="top", fill="y")

        # Pane #3
        self.pane_cloud = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_cloud, weight=2)

        # Scrollbar
        self.scrollbar_cloud = ttk.Scrollbar(self.pane_cloud)
        self.scrollbar_cloud.pack(side="right", fill="y")

        # Treeview
        self.treeview_cloud = ttk.Treeview(
            self.pane_cloud,
            selectmode="browse",
            yscrollcommand=self.scrollbar_cloud.set,
            columns=(1, 2),
            height=10,
        )
        self.treeview_cloud.pack(expand=True, fill="both")
        self.scrollbar_cloud.config(command=self.treeview_cloud.yview)

        # Treeview columns
        self.treeview_cloud.column("#0", anchor="w", width=120)
        self.treeview_cloud.column(1, anchor="w", width=120)
        self.treeview_cloud.column(2, anchor="w", width=120)

        self._insert_treeview_data(treeview_data=treeview_data, treeview=self.treeview_cloud)

        # Select and scroll
        self.treeview_cloud.selection_set(10)
        self.treeview_cloud.see(7)

        # Sizegrip
        # self.sizegrip = ttk.Sizegrip(self)
        # self.sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simple example")

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