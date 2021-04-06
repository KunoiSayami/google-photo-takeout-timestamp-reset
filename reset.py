#!/usr/bin/env python
# -*- coding: utf-8 -*-
# main.py
# Copyright (C) 2021 KunoiSayami
#
# This module is part of google-photo-takeout-timestamp-reset and is released under
# the AGPL v3 License: https://www.gnu.org/licenses/agpl-3.0.txt
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
import os
import json


def get_file_json_object(root: str, file: str, json_filename: str) -> dict:
    # print(file)
    try:
        with open(os.path.join(root, json_filename), encoding='utf8') as fin:
            return json.load(fin)
    except FileNotFoundError:
        try:
            with open(os.path.join(root, f'{file}.json'), encoding='utf8') as fin:
                return json.load(fin)
        except FileNotFoundError:
            pass

    for cut in range(len(file) - 1, 10, -1):
        try:
            with open(os.path.join(root, f'{file[:cut]}.json'), encoding='utf8') as fin:
                obj = json.load(fin)
        except FileNotFoundError:
            if cut == 10:
                raise

    return obj


def main():
    for root, dirs, files in os.walk("."):
        if root == '.' or root == 'skipped':
            continue
        for file in files:
            try:
                if file.endswith(".json"):
                    continue
                json_filename = f'{file}.json'
                if len(seq := file.rsplit(').', 2)) > 1:
                    index = int((ori := seq[0].rsplit('(', 2))[1])
                    json_filename = f'{ori[0]}.{seq[1]}({index}).json'
                obj = get_file_json_object(root, file, json_filename)
                atime = obj.get("photoTakenTime", obj.get("creationTime"))
                if atime is None:
                    print(f"Error in get file {file}")
                atime = int(atime.get("timestamp"))
                os.utime(os.path.join(root, file), (atime, atime))
            except UnboundLocalError:
                print(f'skip file {file}')
                os.rename(os.path.join(root, file), os.path.join("skipped", file))


if __name__ == '__main__':
    main()

