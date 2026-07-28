from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class RadiusAccount(Base):
    """
    One row per RADIUS session. Nullability mirrors ``migrations/radacct.sql``:
    a session that is still open has a NULL ``acctstoptime``, which is how the
    accounting queries tell active sessions apart.
    """

    __tablename__ = "radacct"

    radius_account_id: Mapped[int] = mapped_column("radacctid", primary_key=True)
    account_session_id: Mapped[str] = mapped_column("acctsessionid")
    account_unique_id: Mapped[str] = mapped_column("acctuniqueid")
    username: Mapped[str]
    # group_name = mapped_column("groupname", String)
    realm: Mapped[str | None]
    nas_ip_address: Mapped[str] = mapped_column("nasipaddress")
    nas_port_id: Mapped[str | None] = mapped_column("nasportid")
    nas_port_type: Mapped[str | None] = mapped_column("nasporttype")
    account_start_time: Mapped[datetime | None] = mapped_column("acctstarttime")
    account_update_time: Mapped[datetime | None] = mapped_column("acctupdatetime")
    account_stop_time: Mapped[datetime | None] = mapped_column("acctstoptime")
    account_interval: Mapped[int | None] = mapped_column("acctinterval")
    account_session_time: Mapped[int | None] = mapped_column("acctsessiontime")
    account_authentic: Mapped[str | None] = mapped_column("acctauthentic")
    connectinfo_start: Mapped[str | None]
    connectinfo_stop: Mapped[str | None]
    account_input_octets: Mapped[int | None] = mapped_column("acctinputoctets")
    account_output_octets: Mapped[int | None] = mapped_column("acctoutputoctets")
    called_station_id: Mapped[str] = mapped_column("calledstationid")
    calling_station_id: Mapped[str] = mapped_column("callingstationid")
    account_terminate_cause: Mapped[str] = mapped_column("acctterminatecause")
    service_type: Mapped[str | None] = mapped_column("servicetype")
    framedprotocol: Mapped[str | None]
    framedipaddress: Mapped[str]
