import os
from datetime import datetime
from database.itemsql import Items

def pre_scanresult(len_res, drive_name_result, raw_lsjson_result, g_drive_name, g_drive_id, g_folder_name, g_folder_id):
    #global count_id
    type = ""
    extension = ""
    count_id = 0
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
            item_string = made_eachData(count_id, each, front_path, type, extension, g_drive_name, g_drive_id, g_folder_name, g_folder_id)
        elif each["Name"].endswith(sub_suffix):
            type = "subtitle"
            extension = os.path.splitext(each["Name"])[-1][1:]
            item_string = f"item{count_id}"
            item_string = made_eachData(count_id, each, front_path, type, extension, g_drive_name, g_drive_id, g_folder_name, g_folder_id)
        else:
            count_id -= 1
            continue

        many_request.append(item_string)
    
    return many_request

def made_eachData(count_id, each, front_path, type, extension, g_drive_name, g_drive_id, g_folder_name, g_folder_id):
    eachData = Items(
    id=count_id,
    name=each["Name"],
    path=f'{front_path}{each["Path"]}',
    size=int(each["Size"]),
    modtime=each["ModTime"],#datetime,#each["ModTime"],
    isdir=each["IsDir"],
    type = type,
    extension = extension,
    g_drive_name = g_drive_name,
    g_drive_id=g_drive_id,
    g_folder_name = g_folder_name,
    g_folder_id = g_folder_id,
    g_endpoint_id=each["ID"],)

    return eachData
