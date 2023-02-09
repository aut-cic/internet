from sqlalchemy.orm import Mapped, mapped_column
from datetime import date

from . import Base


# pyre-ignore[11]
class RadiusDaily(Base):
    __tablename__ = "raddaily"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    usage_original: Mapped[int] = mapped_column("usageorig")
    usage_discount: Mapped[int] = mapped_column("usagediscount")
    create_date: Mapped[date] = mapped_column("createddate")
