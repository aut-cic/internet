from sqlalchemy.orm import Mapped, mapped_column

from . import Base


# pyre-ignore[11]
class RadiusUserGroup(Base):
    __tablename__ = "radusergroup"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    group_name: Mapped[str] = mapped_column("groupname")
    priority: Mapped[int]
    # update_time: Mapped[datetime]
