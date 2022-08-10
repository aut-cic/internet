from sqlalchemy import Column, Integer, String

from . import Base


class RadiusPackages(Base):
    __tablename__ = "radpackages"

    id = Column("id", Integer, primary_key=True)
    group_name = Column("groupname", String)
    daily_volume = Column("daily_volume", Integer)
    weekly_volume = Column("weekly_volume", Integer)
    monthly_volume = Column("monthly_volume", Integer)
    priority = Column("priority", Integer)
    session = Column("session", Integer)
