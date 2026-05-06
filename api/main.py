from fastapi import FastAPI, Depends, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from database.models import get_db_session, MetricSnapshot, query_recent
from monitor.system_reader import get_snapshot

app = FastAPI(title="SysWatch API", version="1.0.0")

# --- Pydantic Models (Data Validation) ---
class MetricOut(BaseModel):
    id: int
    timestamp: datetime
    cpu_pct: float
    mem_pct: float
    disk_pct: float

    class Config:
        from_attributes = True # SQLAlchemy objelerini otomatik dönüştürür

class MetricSummaryOut(BaseModel):
    avg_cpu: float
    max_cpu: float
    spike_count: int
    period_minutes: int

# --- Dependency ---
def get_db():
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints ---

@app.get("/metrics/current")
def get_current():
    """Returns the immediate live results."""
    return get_snapshot()

@app.get("/metrics/history", response_model=List[MetricOut])
def get_history(last_minutes: int = 60, db: Session = Depends(get_db)):
    """Retrieves records from the database for the last N minutes."""
    return query_recent(db, last_minutes)

@app.get("/metrics/alerts", response_model=List[MetricOut])
def get_alerts(cpu_threshold: float = 80.0, db: Session = Depends(get_db)):
    """Filters history for CPU usage spikes."""
    return db.query(MetricSnapshot).filter(MetricSnapshot.cpu_pct > cpu_threshold).all()

@app.get("/metrics/summary", response_model=MetricSummaryOut)
def get_summary(last_minutes: int = 60, db: Session = Depends(get_db)):
    """Calculates basic stats for the given period."""
    data = query_recent(db, last_minutes)
    if not data:
        return {"avg_cpu": 0, "max_cpu": 0, "spike_count": 0, "period_minutes": last_minutes}
    
    cpus = [d.cpu_pct for d in data]
    return {
        "avg_cpu": sum(cpus) / len(cpus),
        "max_cpu": max(cpus),
        "spike_count": len([c for c in cpus if c > 80]),
        "period_minutes": last_minutes
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="[IP_ADDRESS]", port=8001)    

# --- Background Task Integration (Optional but professional) ---
# Normally, you'd run scheduler.py separately, but you can trigger it here too.