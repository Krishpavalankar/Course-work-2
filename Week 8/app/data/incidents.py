import pandas as pd
from app.data.db import connect_database


# ------------------------------
# CREATE
# ------------------------------
def insert_incident(date, incident_type, severity, status, description, reported_by=None):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cyber_incidents
        (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, incident_type, severity, status, description, reported_by))

    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()

    return incident_id


# ------------------------------
# READ
# ------------------------------
def get_all_incidents():
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM cyber_incidents ORDER BY id DESC", conn)
    conn.close()
    return df


# ------------------------------
# UPDATE
# ------------------------------
def update_incident_status(incident_id, new_status):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE cyber_incidents
        SET status = ?
        WHERE id = ?
    """, (new_status, incident_id))

    conn.commit()
    affected_rows = cursor.rowcount
    conn.close()

    return affected_rows


# ------------------------------
# DELETE
# ------------------------------
def delete_incident(incident_id):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))

    conn.commit()
    affected_rows = cursor.rowcount
    conn.close()

    return affected_rows
