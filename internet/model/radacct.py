from sqlalchemy import Column, Date, DateTime, Integer, String

from . import Base


class RadiusAccount(Base):
    __tablename__ = "radacct"

    radius_account_id = Column("radacctid", Integer, primary_key=True)
    account_session_id = Column("acctsessionid", String)
    account_unique_id = Column("acctuniqueid", String)
    username = Column(String)
    group_name = Column("groupname", String)
    realm = Column(String)
    nas_ip_address = Column("nasipaddress", String)
    nas_port_id = Column("nasportid", String)
    nas_port_type = Column("nasporttype", String)
    account_start_time = Column("acctstarttime", DateTime)
    account_update_time = Column("acctupdatetime", DateTime)
    account_stop_time = Column("acctstoptime", DateTime)
    account_interval = Column("acctinterval", Integer)
    account_session_time = Column("acctsessiontime", Integer)
    account_authentic = Column("acctauthentic", String)
    connectinfo_start = Column(String)
    connectinfo_stop = Column(String)
    account_input_octets = Column("acctinputoctets", Integer)
    account_output_octets = Column("acctoutputoctets", Integer)
    called_station_id = Column("calledstationid", String)
    calling_station_id = Column("callingstationid", String)
    account_terminate_cause = Column("acctterminatecause", String)
    service_type = Column("servicetype", String)
    framedprotocol = Column(String)
    framedipaddress = Column(String)
