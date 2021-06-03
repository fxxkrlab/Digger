import datetime
from typing import Any

from sqlalchemy import Column, ForeignKey, Integer, String, VARCHAR, DateTime, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean

from database import SESSION, BASE

class Items(BASE):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    media_name = Column(String(3000))
    file_name = Column(String(3000))
    path = Column(String(3000))
    size = Column(BigInteger)
    isdir = Column(String(250))
    type = Column(String(250))
    extension = Column(String(250))
    category = Column(String(250))
    g_drive_name = Column(String(250))
    g_drive_id = Column(String(250))
    g_folder_name = Column(String(250))
    g_folder_id = Column(String(250))
    g_endpoint_id = Column(String(250))

    def __init__(
        self,
        id,
        media_name = None,
        file_name = None,
        path = None,
        size = None,
        isdir = None,
        type = None,
        extension = None,
        category = None,
        g_drive_name = None,
        g_drive_id = None,
        g_folder_name = None,
        g_folder_id = None,
        g_endpoint_id = None,
    ):
        self.id = id,
        self.media_name = media_name,
        self.file_name = file_name,
        self.path = path,
        self.size = size,
        self.isdir = isdir,
        self.type = type,
        self.extension = extension,
        self.category = category,
        self.g_drive_name = g_drive_name,
        self.g_drive_id = g_drive_id,
        g_folder_name = g_folder_name,
        g_folder_id = g_folder_id,
        self.g_endpoint_id = g_endpoint_id

Items.__table__.create(checkfirst=True)
