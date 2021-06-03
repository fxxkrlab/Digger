import datetime
from typing import Any

from sqlalchemy import Column, ForeignKey, Integer, String, VARCHAR, DateTime, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean

from database import SESSION, BASE

class Folders(BASE):
    __tablename__ = "folders"
    id = Column(Integer, primary_key=True)
    folder_name = Column(String(3000))
    type = Column(String(250))
    g_endpoint_id = Column(String(250))

    def __init__(
        self,
        id,
        folder_name = None,
        type = None,
        g_endpoint_id = None,
    ):
        self.id = id,
        self.folder_name = folder_name,
        self.type = type,
        self.g_endpoint_id = g_endpoint_id

Folders.__table__.create(checkfirst=True)
