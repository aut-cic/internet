from sqlalchemy.orm import Mapped, mapped_column

from . import Base


# pyre-ignore[11]
class RadiusPackages(Base):
    __tablename__ = "radpackages"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_name: Mapped[str] = mapped_column("groupname")
    daily_volume: Mapped[int] = mapped_column("daily_volume")
    weekly_volume: Mapped[int] = mapped_column("weekly_volume")
    monthly_volume: Mapped[int] = mapped_column("monthly_volume")
    priority: Mapped[int] = mapped_column("priority")
    session: Mapped[int] = mapped_column("session")
