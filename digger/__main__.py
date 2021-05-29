import sys, json
from modules import scanner
from database.operate import operateDb
from database.itemsql import Items


def main():
    g_drive_id = sys.argv[1]
    checkers = sys.argv[2]
    transfers = sys.argv[3]

    '''
    out, err = scanner.lsjson(
        g_drive_id=g_drive_id, checkers=checkers, transfers=transfers
    )
    raw_lsjson_result = json.loads(out)
    '''
    result = scanner.lsjson(
        g_drive_id=g_drive_id, checkers=checkers, transfers=transfers
    )
    raw_lsjson_result = json.loads(result)
    count_id = 0
    many_request = []

    for each in raw_lsjson_result:
        count_id += 1

        item_string = f"item{count_id}"
        item_string = Items(
            id=count_id,
            name=each["Name"],
            path=each["Path"],

            size=each["Size"],
            modtime=each["ModTime"],
            isdir=each["IsDir"],
            g_drive_id=g_drive_id,
            g_endpoint_id=each["ID"],
        )
        #operateDb().add(item_string)
        many_request.append(item_string)
    operateDb().addmany(many_request)
    count_id = 0
    many_request = []


if __name__ == "__main__":
    main()
