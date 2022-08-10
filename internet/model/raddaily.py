from sqlalchemy import Column, Date, Integer, String

from . import Base


# pyre-ignore[11]
class RadiusDaily(Base):
    __tablename__ = "raddaily"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    usage_original = Column("usageorig", Integer)
    usage_discount = Column("usagediscount", Integer)
    create_date = Column("createddate", Date)
