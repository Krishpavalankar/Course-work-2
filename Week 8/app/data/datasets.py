import pandas as pd
from app.data.db import connect_database

# -----------------------------------
# CREATE
# -----------------------------------
def insert_dataset(dataset_name, category, source, last_updated, record_count, file_size_mb):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO datasets_metadata
        (dataset_name, category, source, last_updated, record_count, file_size_mb)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_name, category, source, last_updated, record_count, file_size_mb))

    conn.commit()
    dataset_id = cursor.lastrowid
    conn.close()

    return dataset_id


# -----------------------------------
# READ
# -----------------------------------
def get_all_datasets():
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM datasets_metadata ORDER BY id DESC", conn)
    conn.close()
    return df


# -----------------------------------
# UPDATE
# -----------------------------------
def update_dataset_last_updated(dataset_id, new_date):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE datasets_metadata
        SET last_updated = ?
        WHERE id = ?
    """, (new_date, dataset_id))

    conn.commit()
    updated_rows = cursor.rowcount
    conn.close()
    return updated_rows


# -----------------------------------
# DELETE
# -----------------------------------
def delete_dataset(dataset_id):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM datasets_metadata WHERE id = ?", (dataset_id,))

    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()
    return deleted_rows
