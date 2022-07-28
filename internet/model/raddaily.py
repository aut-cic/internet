from sqlalchemy import Column, Date, Integer, String


class RadiusDaily:
    __tablename__ = "raddaily"

    username = Column(String)
    usage_original = Column("usageorig", Integer)
    usage_discount = Column("usagediscount", Integer)
    create_date = Column("createddate", Date)
