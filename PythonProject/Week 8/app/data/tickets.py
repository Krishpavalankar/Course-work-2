import pandas as pd
from app.data.db import connect_database

# -----------------------------------
# CREATE
# -----------------------------------
def insert_ticket(ticket_id, priority, status, category, subject, description, created_date, resolved_date=None, assigned_to=None):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO it_tickets
        (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to))

    conn.commit()
    entry_id = cursor.lastrowid
    conn.close()

    return entry_id


# -----------------------------------
# READ
# -----------------------------------
def get_all_tickets():
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM it_tickets ORDER BY id DESC", conn)
    conn.close()
    return df


# -----------------------------------
# UPDATE
# -----------------------------------
def update_ticket_status(ticket_id, new_status):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE it_tickets
        SET status = ?
        WHERE ticket_id = ?
    """, (new_status, ticket_id))

    conn.commit()
    updated_rows = cursor.rowcount
    conn.close()
    return updated_rows


# -----------------------------------
# DELETE
# -----------------------------------
def delete_ticket(ticket_id):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM it_tickets WHERE ticket_id = ?", (ticket_id,))

    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()
    return deleted_rows
