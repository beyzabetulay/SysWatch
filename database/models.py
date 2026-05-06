from sqlalchemy import Column, Integer, Float, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

Base = declarative_base()

class MetricSnapshot(Base):
    __tablename__ = "metric_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # index=True makes time-based queries much faster
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    cpu_pct = Column(Float, nullable=False)
    mem_pct = Column(Float, nullable=False)
    disk_pct = Column(Float, nullable=False)
    net_sent_mb = Column(Float, nullable=False)
    net_recv_mb = Column(Float, nullable=False)

def bulk_save(session: Session, snapshots: list[dict]):
    """
    Saves multiple snapshots in a single transaction for high performance.
    """
    try:
        session.bulk_insert_mappings(MetricSnapshot, snapshots)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

def query_recent(session: Session, minutes: int) -> list[MetricSnapshot]:
    """
    Retrieves snapshots from the last N minutes.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=minutes)
    return session.query(MetricSnapshot).filter(MetricSnapshot.timestamp > cutoff).all()