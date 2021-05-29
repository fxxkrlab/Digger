import sys, json
from modules import scanner
from database.operate import operateDb
from database.itemsql import Items
from modules.drive import GoogleDrive

def main():
    drive_id = sys.argv[1]
    checkers = sys.argv[2]
    transfers = sys.argv[3]
    count_id = 0
    many_request = []

    scan_result = scanner.lsjson(
        drive_id=drive_id, checkers=checkers, transfers=transfers
    )
    raw_lsjson_result = json.loads(scan_result)
    drive_name_result = GoogleDrive.get_file_path_from_id(GoogleDrive(),drive_id)
    if len(drive_name_result) >= 2:
        drive_num = len(drive_name_result) - 1
        len_res = len(drive_name_result)
        g_drive_name = drive_name_result[drive_num]['name']
        g_drive_id = drive_name_result[drive_num]['folder_id']
        g_folder_name = drive_name_result[0]['name']
        g_folder_id = drive_id
        front_path = ""
        while len_res > 0:
            front_path += f"{drive_name_result[(len_res - 1)]['name']}/"
            len_res -= 1

        for each in raw_lsjson_result:
            count_id += 1

            item_string = f"item{count_id}"
            item_string = Items(
                id=count_id,
                name=each["Name"],
                path=f'{front_path}{each["Path"]}',
                size=each["Size"],
                modtime=each["ModTime"],
                isdir=each["IsDir"],
                g_drive_name = g_drive_name,
                g_drive_id=g_drive_id,
                g_folder_name = g_folder_name,
                g_folder_id = g_folder_id,
                g_endpoint_id=each["ID"],
            )
            
            many_request.append(item_string)

    if len(drive_name_result) == 1:
        g_drive_name = drive_name_result[0]['name']
        g_drive_id = drive_id
    
        for each in raw_lsjson_result:
            count_id += 1

            item_string = f"item{count_id}"
            item_string = Items(
                id=count_id,
                name=each["Name"],
                path=f'{g_drive_name}/{each["Path"]}',
                size=each["Size"],
                modtime=each["ModTime"],
                isdir=each["IsDir"],
                g_drive_name = g_drive_name,
                g_drive_id=g_drive_id,
                g_folder_name = None,
                g_folder_id = None,
                g_endpoint_id=each["ID"],
            )
            
            many_request.append(item_string)

    operateDb().addmany(many_request)
    count_id = 0
    many_request = []


if __name__ == "__main__":
    main()
