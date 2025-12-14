from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file

from app.data.incidents import insert_incident, get_all_incidents, update_incident_status, delete_incident
from app.data.datasets import insert_dataset, get_all_datasets, update_dataset_last_updated, delete_dataset
from app.data.tickets import insert_ticket, get_all_tickets, update_ticket_status, delete_ticket

import pandas as pd
from pathlib import Path

DATA_DIR = Path("DATA")


# ---------------------------------------------------------------------
# LOAD CSV HELPER
# ---------------------------------------------------------------------
def load_csv_to_table(conn, csv_filename, table_name):
    csv_path = DATA_DIR / csv_filename

    if not csv_path.exists():
        print(f"⚠️ CSV not found: {csv_path}")
        return 0

    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists="append", index=False)

    print(f"✅ Loaded {len(df)} rows into {table_name}")
    return len(df)


# ---------------------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------------------
def main():
    print("=" * 60)
    print("🚀 WEEK 8 — DATABASE SYSTEM DEMO")
    print("=" * 60)

    # 1. Connect
    print("\n[1/6] Connecting to database...")
    conn = connect_database()
    print("   ✔ Connected")

    # 2. Create tables
    print("\n[2/6] Creating database tables...")
    create_all_tables(conn)

    # 3. Migrate users
    print("\n[3/6] Migrating users from users.txt...")
    migrate_users_from_file(conn)

    # 4. Load CSVs
    print("\n[4/6] Loading CSV files into database...")
    load_csv_to_table(conn, "cyber_incidents.csv", "cyber_incidents")
    load_csv_to_table(conn, "datasets_metadata.csv", "datasets_metadata")
    load_csv_to_table(conn, "it_tickets.csv", "it_tickets")

    # 5. Test CRUD
    print("\n[5/6] Running CRUD tests...")

    # ---------------- INCIDENT CRUD ----------------
    print("\n   🔹 Testing cyber_incidents CRUD")
    incident_id = insert_incident(
        "2024-12-10", "Phishing", "High", "Open",
        "Fake login email detected", "admin"
    )
    print("     ✔ Inserted incident:", incident_id)

    update_incident_status(incident_id, "Resolved")
    print("     ✔ Updated status → Resolved")

    delete_incident(incident_id)
    print("     ✔ Deleted test incident")

    # ---------------- DATASET CRUD -----------------
    print("\n   🔹 Testing datasets CRUD")
    dataset_id = insert_dataset(
        "Firewall Logs", "Network Logs", "Cisco",
        "2024-12-01", 50000, 12.5
    )
    print("     ✔ Inserted dataset:", dataset_id)

    update_dataset_last_updated(dataset_id, "2024-12-05")
    print("     ✔ Updated last_updated date")

    delete_dataset(dataset_id)
    print("     ✔ Deleted test dataset")

    # ---------------- TICKET CRUD ------------------
    print("\n   🔹 Testing IT tickets CRUD")
    ticket_entry_id = insert_ticket(
        "T-9001", "Medium", "Open", "Software",
        "System crash", "User reports frequent crashes",
        "2024-11-01"
    )
    print("     ✔ Inserted ticket:", ticket_entry_id)

    update_ticket_status("T-9001", "In Progress")
    print("     ✔ Updated ticket status")

    delete_ticket("T-9001")
    print("     ✔ Deleted test ticket")

    # 6. Final summary
    print("\n[6/6] Database Summary:")
    cursor = conn.cursor()
    tables = ["users", "cyber_incidents", "datasets_metadata", "it_tickets"]

    print(f"\n{'Table Name':<25} {'Row Count':<10}")
    print("-" * 35)

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<10}")

    conn.close()

    print("\n🎉 DATABASE SETUP & CRUD TESTS COMPLETE!")
    print("=" * 60)


# Run main
if __name__ == "__main__":
    main()
