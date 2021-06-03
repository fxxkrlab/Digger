import os, re
from datetime import datetime
from database.itemsql import Items
from database.foldersql import Folders
from modules import load

def pre_scanresult(count_id, len_res, drive_name_result, raw_lsjson_result, g_drive_name, g_drive_id):
    type = ""
    extension = ""
    count_id = count_id
    many_request = []
    video_suffix = ('mkv', 'ts', 'iso', 'm2ts', 'mp4', 'avi', 'rmvb', 'flv')
    sub_suffix = ('ass', 'vtt', 'ssa', 'srt')

    front_path = ""
    while len_res > 0:
        front_path += f"{drive_name_result[(len_res - 1)]['name']}/"
        len_res -= 1

    for each in raw_lsjson_result:
        count_id += 1
        if each["Name"].endswith(video_suffix):
            type = "video"
            extension = os.path.splitext(each["Name"])[-1][1:]
            item_string = f"item{count_id}"
            item_string = made_eachData(count_id, each, front_path, type, extension, g_drive_name, g_drive_id)
        elif each["Name"].endswith(sub_suffix):
            type = "subtitle"
            extension = os.path.splitext(each["Name"])[-1][1:]
            item_string = f"item{count_id}"
            item_string = made_eachData(count_id, each, front_path, type, extension, g_drive_name, g_drive_id)
        else:
            count_id -= 1
            continue

        many_request.append(item_string)
    
    return many_request

def made_eachData(count_id, each, front_path, type, extension, g_drive_name, g_drive_id):
    eachData = Items(
    id=count_id,
    file_name=each["Name"],
    path=f'{front_path}{each["Path"]}'.replace(each["Name"],""),
    size=int(each["Size"]),
    isdir=each["IsDir"],
    type = type,
    extension = extension,
    g_drive_name = g_drive_name,
    g_drive_id=g_drive_id,
    g_endpoint_id=each["ID"],)

    return eachData

def pre_folderlist(count_id, path):
    count_id = count_id
    many_request = []
    for e in path:
        count_id += 1
        folder_string = f"folder{count_id}"
        match_tv_folder = re.search(load.tv_folders,e, flags=re.I)
        if match_tv_folder is not None:
            type = "tv"
        else:
            type = None
        folder_string = made_eachFolder(count_id, type, e)

        many_request.append(folder_string)

    return many_request

def made_eachFolder(count_id, type, e):
    eachData = Folders(
    id=count_id,
    folder_name=e,
    type=type,)

    return eachData