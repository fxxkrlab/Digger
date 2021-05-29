#!/usr/bin/python3
# -*- coding: utf-8 -*-

from modules import load

from threading import Thread
import subprocess
from telegram import ParseMode
from telegram.utils.request import Request as TGRequest
from telegram import Bot
from multiprocessing import Manager

text = b'''
goodbye
'''
def lsjson(drive_id, checkers, transfers):
    cloner = "fclone"
    option = "lsjson"
    stats = "-R"
    filter = "--files-only"
    configuration = load._cfg["extension"]["cloner"]["configuration"]
    src_block = configuration + ":" + "{" + drive_id + "}"
    checkers = f"--checkers={str(checkers)}"
    transfers = f"--transfers={str(transfers)}"
    flags = "--check-first"
    sa_sleep = "--drive-pacer-min-sleep=1ms"

    command = [
        cloner,
        option,
        stats,
        filter,
        src_block,
        flags,
        checkers,
        transfers,
        sa_sleep,
    ]

    result = lsjson_run(command)

    #return (out,err)
    return result

def lsjson_run(command):
    scanning = subprocess.check_output(command)
    result = scanning.decode('utf-8')
    '''
    scanning = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=False,
        errors="ignore",
        universal_newlines=True,
    )
    stdout, stderr = scanning.communicate(text)
    out = stdout
    err = stderr

    return (out,err)
    '''
    return result
