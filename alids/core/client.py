#!/usr/bin/env python
# -*- encoding: utf-8 -*-
""" 
@File    :   alids\core\client.py 
@Time    :   2022-01-20 10:11:33 
@Author  :   Bingjie Yan 
@Email   :   bj.yan.pa@qq.com 
@License :   Apache License 2.0 
"""

from distutils import filelist
import os
import requests


class Client(object):
    def __init__(self,
                 access_token: str = None,
                 refresh_token: str = None,
                 drive_id: str = None):
        self.token = access_token
        self.refresh_token = refresh_token
        self.drive_id = drive_id
        self.session = requests.session()

        self.token_checked = False

        self.file_tree = {}
        self.filepath2id = {}

    def _get_token(self):
        return self.token

    def _check_token(self):
        if self.token_checked:
            return True
        api_url = "https://api.aliyundrive.com/v2/user/get"
        headers = {"authorization": self.token}
        response = self.session.post(api_url, headers=headers, json={})
        if response.status_code == 200:
            self.token_checked = True
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
        self.drive_id = info["default_drive_id"]

    def _get_user_info(self):
        api_url = "https://api.aliyundrive.com/v2/user/get"
        headers = {"Authorization": self.token}
        response = self.session.post(api_url, headers=headers, json={})

        self._update_info(response.json())
        return self.info

    def get_user_avatar(self):
        if hasattr(self, "avatar"):
            return self.avatar
        return None

    def get_user_nickname(self):
        if hasattr(self, "nick_name"):
            return self.nick_name
        return None

    def get_user_id(self):
        if hasattr(self, "user_id"):
            return self.user_id
        return None

    def get_user_phone(self):
        if hasattr(self, "phone"):
            return self.phone
        return None

    def login(self):
        if self.token:
            if not self._check_token():
                raise Exception("token is invalid")
            self._get_user_info()
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

    def _get_file(self, file_id: str):
        if not self._check_token():
            raise Exception("token is invalid")

        api_url = "https://api.aliyundrive.com/v2/file/get"
        headers = {"authorization": self.token}
        response = self.session.post(api_url,
                                     headers=headers,
                                     json={
                                         "drive_id": self.drive_id,
                                         "file_id": file_id
                                     })

        return response.json()

    def _update_filetree(self, parent_path: str, file_list: list):
        """ update file tree

        Args:
            parent_path (str): [description]
            file_list (list): [description]
        """
        path_list = os.path.split(parent_path)
        _file_tree = self.file_tree
        for path_item in path_list:
            if path_item not in _file_tree:
                _file_tree[path_item] = {}
            _file_tree = _file_tree[path_item]

        for file_item in file_list:
            _file_tree[file_item['name']] = file_item
            self.filepath2id[os.path.normpath(os.path.join(
                parent_path, file_item['name']))] = file_item['file_id']

    def _get_file_id_by_path(self, file_path: str):
        """
        get file id by file path
        if you want to get file id of root, you should use '/'
        if you want to use this method, you should get file list first
        """
        if file_path == '/':
            return 'root'
        else:
            # format file path
            file_path = os.path.normpath(file_path)
            return self.filepath2id[file_path]

    def _get_file_download_url(self, file_id: str):
        """ get file download url

        Args:
            file_id (str): [description]
        """
        if not self._check_token():
            raise Exception("token is invalid")

        # print(file_id, self.drive_id)

        api_url = "https://api.aliyundrive.com/v2/file/get_download_url"
        headers = {"authorization": self.token}
        response = self.session.post(api_url,
                                     headers=headers,
                                     json={
                                         "drive_id": self.drive_id,
                                         "file_id": file_id
                                     })

        return response.json()

    def get_file_download_url(self, file_path: str):
        """ get file download url

        Args:
            file_id (str): [description]
        """
        file_id = self._get_file_id_by_path(file_path)
        json = self._get_file_download_url(file_id)
        # print(json)
        if json.get("steams_url"):
            return json["steams_url"]["jpeg"]
        else:
            return json["url"]

    def download_file(self, file_path: str, save_path: str):
        """ download file

        Args:
            file_path (str): [description]
            save_path (str): [description]
        """
        url = self.get_file_download_url(file_path)
        response = self.session.get(url, headers={"Referer": "https://www.aliyundrive.com/"})
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
        else:
            raise Exception("download file failed")

    def _get_file_id(self, file_path: str = '/'):
        """[summary]

        Args:
            file_path (str, optional): [description]. Defaults to '/'.

        Returns:
            [type]: [description]
        """
        if file_path == '/':
            return 'root'
        else:
            # split path
            _path_list = os.path.split(file_path)

            # get file id step by step
            _path = '/'
            _fileid = 'root'
            for path_item in _path_list:
                _path = os.path.join(_path, path_item)
                _fileid = self._get_file_id_by_path(_path)
                # print(_path, _fileid)
                _filetree = self._get_file_list(_fileid)['items']
                self._update_filetree(_path, _filetree)

            return _fileid

    def _get_file_list(self, parent_file_id: str = 'root'):
        """ get file list by parent file id using aliyun api

        Args:
            parent_file_id (str, optional): [description]. Defaults to 'root'.

        Raises:
            Exception: [description]

        Returns:
            [type]: [description]
        """
        if not self._check_token():
            raise Exception("token is invalid")

        api_url = "https://api.aliyundrive.com/adrive/v3/file/list"
        headers = {
            "Authorization": self.token,
        }
        payload = {
            "drive_id": self.drive_id,
            "parent_file_id": parent_file_id,
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
        """ extenal method to get file list

        Args:
            parent_file_path (str, optional): [description]. Defaults to '/'.

        Returns:
            [type]: [description]
        """
        parent_file_id = self._get_file_id(parent_file_path)
        json = self._get_file_list(parent_file_id)

        return json['items']

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
            self.str += f"drive_id: {self.drive_id}"

        self.str += ">"
        return self.str