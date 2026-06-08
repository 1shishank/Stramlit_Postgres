from fastapi import FastAPI, HTTPException
from database import get_connection
from models import BackupRecord

app = FastAPI(
    title="Backup Health API"
)


@app.get("/")
def home():

    return {
        "message": "Backup Health API Running"
    }


@app.post("/upload")
def upload_report(records: list[BackupRecord]):

    conn = get_connection()
    cur = conn.cursor()

    try:

        for row in records:

            cur.execute(
                """
                INSERT INTO backup_status
                (
                    report_date,
                    backup_server,
                    ip_address,
                    status,
                    remarks
                )
                VALUES (%s,%s,%s,%s,%s)
                """,
                (
                    row.report_date,
                    row.backup_server,
                    row.ip_address,
                    row.status,
                    row.remarks
                )
            )

        conn.commit()

        return {
            "message": "Report Uploaded Successfully"
        }

    except Exception as e:

        conn.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        conn.close()


@app.get("/report/{report_date}")
def get_report(report_date: str):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT
                backup_server,
                ip_address,
                status,
                remarks
            FROM backup_status
            WHERE report_date = %s
            ORDER BY backup_server
            """,
            (report_date,)
        )

        rows = cur.fetchall()

        result = []

        for row in rows:

            result.append(
                {
                    "backup_server": row[0],
                    "ip_address": row[1],
                    "status": row[2],
                    "remarks": row[3]
                }
            )

        return result

    finally:

        conn.close()