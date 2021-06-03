import re

from database.operate import operateDb
from database.itemsql import Items
from database.foldersql import Folders
from modules.drive import GoogleDrive
from modules import predata, load

LOG = load.logger

def get_folders(count_id):
    results = operateDb().group_by(Items)

    path = []
    for e in results:
        a, = e
        match_path = re.search(load.path_regex_1,a)
        if match_path is not None:
            path.append(match_path.group(2))
    
    print(path)
    LOG.info("send path_list to get Folders Detail list")
    many_request = predata.pre_folderlist(count_id, path)
    LOG.info("get Folders list and request DB")
    operateDb().addmany(many_request)
    LOG.info("Inserted db")
