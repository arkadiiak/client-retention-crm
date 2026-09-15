"""
Client Retention CRM Analysis
-------------------------------
Loads the lapsed-client database and recovery action log into SQLite,
then uses pandas to segment clients, analyze contact outcomes, and
visualize recovery performance by outreach method.
"""

import re
import sqlite3
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
CLIENTS_CSV = BASE_DIR / "data" / "client_database.csv"
ACTIONS_CSV = BASE_DIR / "data" / "recovery_action_log.csv"
SCHEMA_PATH = BASE_DIR / "sql" / "schema_retention.sql"
DB_PATH = BASE_DIR / "python" / "client_retention.db"


def clean_currency(value):
    if pd.isna(value):
        return None
    return float(re.sub(r"[£,]", "", str(value)))


def build_database():
    clients_df = pd.read_csv(CLIENTS_CSV)
    clients_df["spend_gbp"] = clients_df["spend_gbp"].apply(clean_currency)

    actions_df = pd.read_csv(ACTIONS_CSV)
    actions_df["spend_gbp"] = actions_df["spend_gbp"].apply(clean_currency)

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_PATH.read_text())

    clients_df.to_sql("client_database", conn, if_exists="replace", index=False)
    actions_df.to_sql("recovery_action_log", conn, if_exists="append", index=False)

    conn.commit()
    return conn


def segment_summary(conn):
    query = """
        SELECT
            CASE
                WHEN visits >= 40 THEN 'High Value (40+)'
                WHEN visits >= 20 THEN 'Mid Value (20-39)'
                WHEN visits >= 10 THEN 'Regular (10-19)'
                ELSE 'New / Light (0-9)'
            END AS segment,
            COUNT(*) AS client_count,
            ROUND(AVG(spend_gbp), 2) AS avg_spend,
            ROUND(SUM(spend_gbp), 2) AS total_spend
        FROM client_database
        GROUP BY segment
        ORDER BY avg_spend DESC
    """
    return pd.read_sql(query, conn)


def contact_result_breakdown(conn):
    query = """
        SELECT contact_result, COUNT(*) AS client_count,
               ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM client_database), 1) AS pct_of_total
        FROM client_database
        GROUP BY contact_result
        ORDER BY client_count DESC
    """
    return pd.read_sql(query, conn)


def top_unresponsive_high_value(conn, limit=10):
    query = """
        SELECT client_id, spend_gbp, visits, last_visit
        FROM client_database
        WHERE contact_result = 'No Response'
        ORDER BY spend_gbp DESC
        LIMIT ?
    """
    return pd.read_sql(query, conn, params=(limit,))


def method_success_rate(conn):
    query = """
        SELECT method, COUNT(*) AS attempts,
               SUM(CASE WHEN result LIKE 'Booked%' THEN 1 ELSE 0 END) AS booked_outcomes,
               ROUND(100.0 * SUM(CASE WHEN result LIKE 'Booked%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS success_rate_pct
        FROM recovery_action_log
        GROUP BY method
        ORDER BY success_rate_pct DESC
    """
    return pd.read_sql(query, conn)


def plot_segment_summary(segment_df):
    import matplotlib.pyplot as plt

    ax = segment_df.plot(kind="bar", x="segment", y="client_count", legend=False, figsize=(8, 5))
    ax.set_title("Lapsed Clients by Value Segment")
    ax.set_ylabel("Number of clients")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(BASE_DIR / "python" / "clients_by_segment.png")
    print("Chart saved to python/clients_by_segment.png")


def main():
    conn = build_database()

    print("\n=== Client segments by visit frequency ===")
    print(segment_summary(conn).to_string(index=False))

    print("\n=== Contact result breakdown ===")
    print(contact_result_breakdown(conn).to_string(index=False))

    print("\n=== Top 10 high-value clients with no response ===")
    print(top_unresponsive_high_value(conn).to_string(index=False))

    print("\n=== Recovery success rate by outreach method ===")
    print(method_success_rate(conn).to_string(index=False))

    plot_segment_summary(segment_summary(conn))
    conn.close()


if __name__ == "__main__":
    main()
