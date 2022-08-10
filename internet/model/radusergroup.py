from sqlalchemy import Column, DateTime, Integer, String

from . import Base


class RadiusUserGroup(Base):
    __tablename__ = "radusergroup"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    group_name = Column("groupname", String)
    priority = Column(Integer)
    update_time = Column(DateTime)
