from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from . import Base


# pyre-ignore[11]
class RadiusAccount(Base):
    __tablename__ = "radacct"

    radius_account_id: Mapped[int] = mapped_column(
        "radacctid", primary_key=True
    )
    account_session_id: Mapped[str] = mapped_column("acctsessionid")
    account_unique_id: Mapped[str] = mapped_column("acctuniqueid")
    username: Mapped[str]
    # group_name = mapped_column("groupname", String)
    realm: Mapped[str]
    nas_ip_address: Mapped[str] = mapped_column("nasipaddress")
    nas_port_id: Mapped[str] = mapped_column("nasportid")
    nas_port_type: Mapped[str] = mapped_column("nasporttype")
    account_start_time: Mapped[datetime] = mapped_column("acctstarttime")
    account_update_time: Mapped[datetime] = mapped_column("acctupdatetime")
    account_stop_time: Mapped[datetime] = mapped_column("acctstoptime")
    account_interval: Mapped[int] = mapped_column("acctinterval")
    account_session_time: Mapped[int] = mapped_column("acctsessiontime")
    account_authentic: Mapped[str] = mapped_column("acctauthentic")
    connectinfo_start: Mapped[str]
    connectinfo_stop: Mapped[str]
    account_input_octets: Mapped[int] = mapped_column("acctinputoctets")
    account_output_octets: Mapped[int] = mapped_column("acctoutputoctets")
    called_station_id: Mapped[str] = mapped_column("calledstationid")
    calling_station_id: Mapped[str] = mapped_column("callingstationid")
    account_terminate_cause: Mapped[str] = mapped_column("acctterminatecause")
    service_type: Mapped[str] = mapped_column("servicetype")
    framedprotocol: Mapped[str]
    framedipaddress: Mapped[str]
