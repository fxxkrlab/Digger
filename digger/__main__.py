import sys, json
from modules import scanner
from database.operate import operateDb
from database.itemsql import Items
from database.foldersql import Folders
from modules.drive import GoogleDrive
from modules import predata, load, get_folders

LOG = load.logger

def main():
    if sys.argv[1] == 'getfolder':
        count_now, = operateDb().get_id(Folders)[0]
        if count_now is not None:
            count_id = count_now
        else:
            count_id = 0

        return get_folders.get_folders(count_id)
    
    else:

        drive_id = sys.argv[1]
        checkers = sys.argv[2]
        transfers = sys.argv[3]

        count_now, = operateDb().get_id(Items)[0]
        if count_now is not None:
            count_id = count_now
        else:
            count_id = 0

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

            many_request = predata.pre_scanresult(count_id, len_res, drive_name_result, raw_lsjson_result, g_drive_name, g_drive_id)

        if len(drive_name_result) == 1:
            drive_num = len(drive_name_result) - 1
            len_res = len(drive_name_result)

            g_drive_name = drive_name_result[0]['name']
            g_drive_id = drive_id

            many_request = predata.pre_scanresult(count_id, len_res, drive_name_result, raw_lsjson_result, g_drive_name, g_drive_id)

        operateDb().addmany(many_request)

if __name__ == "__main__":
    main()
