import threading

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean

from database import SESSION, BASE

class Items(BASE):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    path = Column(String(250))
    size = Column(String(250))
    modtime = Column(String(250))
    isdir = Column(String(250))
    g_drive_id = Column(String(250))
    g_endpoint_id = Column(String(250))

    def __init__(
        self,
        id,
        name = None,
        path = None,
        size = None,
        modtime = None,
        isdir = None,
        g_drive_id = None,
        g_endpoint_id = None,
    ):
        self.id = id,
        self.name = name,
        self.path = path,
        self.size = size,
        self.modtime = modtime,
        self.isdir = isdir,
        self.g_drive_id = g_drive_id,
        self.g_endpoint_id = g_endpoint_id
