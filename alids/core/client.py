#!/usr/bin/env python
# -*- encoding: utf-8 -*-
""" 
@File    :   alids\core\client.py 
@Time    :   2022-01-20 10:11:33 
@Author  :   Bingjie Yan 
@Email   :   bj.yan.pa@qq.com 
@License :   Apache License 2.0 
"""

import os
import requests


class Client(object):
    def __init__(self,
                 access_token: str = None,
                 refresh_token: str = None,
                 driver_id: str = None):
        self.token = access_token
        self.refresh_token = refresh_token
        self.driver_id = driver_id
        self.session = requests.session()

        self.file_tree = {}

    def _get_token(self):
        return self.token

    def _check_token(self):
        api_url = "https://api.aliyundrive.com/v2/user/get"
        headers = {"authorization": self.token}
        response = self.session.post(api_url, headers=headers, json={})
        if response.status_code == 200:
            return True
        else:
            return False

    def _update_info(self, info: dict):
        self.info = info
        # print(self.info)
        self.user_id = info["user_id"]
        self.nick_name = info["nick_name"]
        self.avatar = info["avatar"]
        self.phone = info["phone"]
        self.driver_id = info["default_drive_id"]

    def _get_user_info(self):
        if not self.check_token():
            raise Exception("token is invalid")

        api_url = "https://api.aliyundrive.com/v2/user/get"
        headers = {"Authorization": self.token}
        response = self.session.post(api_url, headers=headers, json={})

        self._update_info(response.json())
        return self.info

    def login(self):
        if self.token:
            if not self._check_token():
                raise Exception("token is invalid")
        else:
            self._get_qrcode()

    def _get_qrcode(self):
        pass

    def _refresh_token(self):
        api_url = "https://api.aliyundrive.com/token/refresh"

        headers = {"refresh_token": self.refresh_token}
        response = self.session.post(api_url, headers=headers, json={})

        if response.status_code == 200:
            resp_data = response.json()
            self._update_info(resp_data)
            return True
        else:
            return False

    def _get_file(self, file_id: str, drive_id: str = ''):
        if not self.check_token():
            raise Exception("token is invalid")

        api_url = "https://api.aliyundrive.com/v2/file/get"
        headers = {"authorization": self.token}
        response = self.session.post(api_url,
                                     headers=headers,
                                     json={
                                         "driver_id": self.driver_id,
                                         "file_id": file_id
                                     })

        return response.json()

    def _get_file_id(file_path: str = '/'):
        pass

    def _update_file_tree(self, parent_path: str, file_list: list):
        pass

    def _get_file_list(self, parent_file_id: str = 'root'):
        if not self.check_token():
            raise Exception("token is invalid")

        api_url = "https://api.aliyundrive.com/adrive/v3/file/list"
        headers = {
            "Authorization": self.token,
        }
        payload = {
            "drive_id": self.driver_id,
            "parent_file_id": "root",
            "limit": 100,
            "all": False,
            "url_expire_sec": 1600,
            "image_thumbnail_process": "image/resize,w_400/format,jpeg",
            "image_url_process": "image/resize,w_1920/format,jpeg",
            "video_thumbnail_process": "video/snapshot,t_1000,f_jpg,ar_auto,w_300",
            "fields": "*",
            "order_by": "updated_at",
            "order_direction": "DESC"
        }
        response = self.session.post(api_url, headers=headers, json=payload)
        # print(response)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_file_list(self, parent_file_path: str = '/'):
        parent_file_id = self._get_file_id(parent_file_path)
        json = self._get_file_list(parent_file_id)

    def _get_download_url(self, file_id: str, drive_id: str = ''):
        pass

    def __str__(self) -> str:
        self.str = f"<Client: "
        # check self have info attribute
        if hasattr(self, "info"):
            self.str += f"user_id: {self.user_id}, "
            self.str += f"nick_name: {self.nick_name}, "
            self.str += f"avatar: {self.avatar}, "
            self.str += f"phone: {self.phone}, "
            self.str += f"driver_id: {self.driver_id}"

        self.str += ">"
        return self.str