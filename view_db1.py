import sqlite3


def display_table_format():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # --- 1. ICCC ANALYTICS TABLE ---
    print("\n" + "=" * 65)
    print(" 📋 TABLE: iccc_analytics ".center(65, " "))
    print("=" * 65)
    print(f"{'ID':<6} | {'Total Revenue':<15} | {'Active Challans':<18} | {'Accidents':<10}")
    print("-" * 65)
    try:
        cursor.execute("SELECT id, total_revenue, challans, accidents FROM iccc_analytics")
        for row in cursor.fetchall():
            print(f"{row[0]:<6} | ₹{row[1]:<14} | {row[2]:<18} | {row[3]:<10}")
    except sqlite3.OperationalError:
        print("Table 'iccc_analytics' not ready yet.")

    # --- 2. TRAFFIC LOGS TABLE ---
    print("\n" + "=" * 95)
    print(" 🚗 TABLE: traffic_logs (LIVE AI HISTORY) ".center(95, " "))
    print("=" * 95)
    print(f"{'ID':<5} | {'Timestamp':<21} | {'Vehicle Classification':<38} | {'Plate':<15} | {'Status':<8}")
    print("-" * 95)
    try:
        cursor.execute(
            "SELECT id, timestamp, vehicle_type, license_plate, priority_status FROM traffic_logs ORDER BY id DESC")
        rows = cursor.fetchall()
        if not rows:
            print("No vehicles processed yet. Upload a frame from dashboard to generate table rows!".center(95))
        for row in rows:
            print(f"{row[0]:<5} | {row[1]:<21} | {row[2]:<38} | {row[3]:<15} | {row[4]:<8}")
    except sqlite3.OperationalError:
        print("Table 'traffic_logs' not ready yet.")

    print("=" * 95 + "\n")
    conn.close()


if __name__ == "__main__":
    display_table_format()