import sqlite3
import pandas as pd
from pathlib import Path

def export_imessage_to_csv():
    # Use the copied database on the Desktop
    db_copy_path = Path.home() / "Desktop/chat_copy.db"
    if not db_copy_path.exists():
        print("Copied chat.db not found. Ensure you created a copy of chat.db on your Desktop.")
        return

    # Connect to the SQLite database
    conn = sqlite3.connect(db_copy_path)

    # Query to extract messages
    query = """
    SELECT 
        datetime(message.date / 1000000000 + 978307200, 'unixepoch') AS timestamp,
        CASE WHEN is_from_me = 1 THEN 'Me' ELSE handle.id END AS sender,
        message.text AS message
    FROM 
        message
    LEFT JOIN 
        handle ON message.handle_id = handle.ROWID
    WHERE 
        message.text IS NOT NULL
    ORDER BY 
        message.date ASC;
    """

    try:
        # Execute query and load data into a DataFrame
        messages = pd.read_sql_query(query, conn)

        # Save to CSV
        output_path = Path.home() / "Desktop/imessage_export.csv"
        messages.to_csv(output_path, index=False)
        print(f"Messages exported successfully to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the database connection
        conn.close()

# Run the export function
if __name__ == "__main__":
    export_imessage_to_csv()
