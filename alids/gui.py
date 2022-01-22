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
from pydoc import cli
import tkinter as tk
from tkinter import ttk
from urllib.request import urlopen

from alids import util
from alids.core import Client


class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        token = os.environ.get("ALIDS_TOKEN")
        self.cli = Client(access_token=token)
        self.cli.login()

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create value lists

        # Create control variables
        self.var_user_avatar = util.get_tkimage(url=self.cli.get_user_avatar())
        self.var_user_nickname = tk.StringVar()
        self.var_user_phone = tk.StringVar()

        self.var_user_nickname.set(self.cli.get_user_nickname())
        self.var_user_phone.set(self.cli.get_user_phone())

        self.var_treeview_local_path = tk.StringVar()
        self.var_treeview_local_path.set(os.path.dirname(__file__))
        self.var_treeview_cloud_path = tk.StringVar()
        self.var_treeview_cloud_path.set("/")

        self.var_log = tk.StringVar()

        # Create widgets :)
        self.setup_widgets()

    def log(self, msg):
        self.var_log.set(msg)

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

    def _on_path_local_return(self, event):
        self.var_treeview_local_path.set(event.widget.get())
        # clear treeview
        self.treeview_local.delete(*self.treeview_local.get_children())

        treeview_data = util.treeview_dir(self.var_treeview_local_path.get())

        self._insert_treeview_data(treeview_data=treeview_data, treeview=self.treeview_local)

    def _on_path_cloud_return(self, event):
        self.var_treeview_cloud_path.set(event.widget.get())
        self.treeview_cloud.delete(*self.treeview_cloud.get_children())
        items = self.cli.get_file_list(self.var_treeview_cloud_path.get())
        treeview_data = util.treeview_alidir(self.var_treeview_cloud_path.get(), items)
        self._insert_treeview_data(treeview_data=treeview_data, treeview=self.treeview_cloud)

    def setup_widgets(self):
        # Define treeview data
        treeview_data = [
            ("", 1, "Parent", ("Item 1", "Value 1")),
        ]

        self.pane_user = ttk.Frame(self, padding=5)
        self.pane_user.grid(row=0, column=0, sticky="nsew", columnspan=3)

        # avator
        self.avatar = ttk.Label(self.pane_user, image=self.var_user_avatar)
        self.avatar.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # user nickname
        self.nickname = ttk.Label(self.pane_user, textvariable=self.var_user_nickname)
        self.nickname.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # user phone
        self.phone = ttk.Label(self.pane_user, textvariable=self.var_user_phone)
        self.phone.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        # Pane #1
        self.pane_local = ttk.Frame(self, padding=5)
        self.pane_local.grid(row=1, column=0, sticky="nsew")

        # path
        self.path_local = ttk.Entry(self.pane_local, textvariable=self.var_treeview_local_path)
        self.path_local.pack(side=tk.TOP, fill=tk.X, expand=True, padx=5, pady=5)
        self.path_local.bind("<Return>", self._on_path_local_return)

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
        self.treeview_local.heading("#0", text="Path")
        self.treeview_local.column("#0", anchor="w", width=180)
        self.treeview_local.heading(1, text="Size")
        self.treeview_local.column(1, anchor="w", width=80)
        self.treeview_local.heading(2, text="Edit Time")
        self.treeview_local.column(2, anchor="w", width=80)

        self._insert_treeview_data(treeview_data=treeview_data, treeview=self.treeview_local)

        # Select and scroll
        # self.treeview_local.selection_set(10)
        # self.treeview_local.see(7)

        # Pane #2
        self.pane_opt = ttk.Frame(self, padding=5)
        self.pane_opt.grid(row=1, column=1, sticky="ne", pady=5)

        # Button
        self.button_push = ttk.Button(self.pane_opt, text="push")
        self.button_push.grid(row=0, column=0, pady=10, sticky="nsew")

        self.button_sync = ttk.Checkbutton(self.pane_opt, text="sync", style="Toggle.TButton")
        self.button_sync.grid(row=1, column=0, pady=10, sticky="nsew")

        self.button_pull = ttk.Button(self.pane_opt, text="pull")
        self.button_pull.grid(row=2, column=0, pady=10, sticky="nsew")

        # Pane #3
        self.pane_cloud = ttk.Frame(self, padding=5)
        self.pane_cloud.grid(row=1, column=2, sticky="nsew")

        # path
        self.path_cloud = ttk.Entry(self.pane_cloud, textvariable=self.var_treeview_cloud_path)
        self.path_cloud.pack(side=tk.TOP, fill=tk.X, expand=True, padx=5, pady=5)
        self.path_cloud.bind("<Return>", self._on_path_cloud_return)

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
        self.treeview_cloud.heading("#0", text="Path")
        self.treeview_cloud.column("#0", anchor="w", width=180)
        self.treeview_cloud.heading(1, text="Size")
        self.treeview_cloud.column(1, anchor="w", width=80)
        self.treeview_cloud.heading(2, text="Edit Time")
        self.treeview_cloud.column(2, anchor="w", width=80)

        self._insert_treeview_data(treeview_data=treeview_data, treeview=self.treeview_cloud)

        # Select and scroll
        # self.treeview_cloud.selection_set(10)
        # self.treeview_cloud.see(7)

        # log pane
        # self.pane_log = ttk.Frame(self, padding=5)
        # self.pane_log.grid(row=2, column=0, columnspan=3, sticky="nsew")

        # log
        self.log_entry = ttk.Entry(self, state="readonly", textvariable=self.var_log)
        self.log_entry.grid(row=2, column=0, sticky="nsew", columnspan=3, padx=5, pady=5)
        self.log("start!")

        # Sizegrip
        # self.sizegrip = ttk.Sizegrip(self)
        # self.sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))
