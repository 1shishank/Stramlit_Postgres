from pydantic import BaseModel
from datetime import date


class BackupRecord(BaseModel):
    report_date: date
    backup_server: str
    ip_address: str
    status: str
    remarks: str