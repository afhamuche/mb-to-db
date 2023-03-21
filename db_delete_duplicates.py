import sqlite3
from concurrent.futures import ThreadPoolExecutor

def process_duplicate_tid(tid):
    # Connect to the database
    conn = sqlite3.connect('trades.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Select all the rows with the duplicate tid
    rows = cursor.execute("SELECT * FROM trades WHERE tid = ?", (tid,)).fetchall()
    # Delete all but the first row with the duplicate tid
    count = 0
    for row in rows[1:]:
        cursor.execute("DELETE FROM trades WHERE tid = ?", (tid,))
        # Insert the deleted row back into the table
        cursor.execute("INSERT INTO trades (amount, date, price, tid, type, satoshi, volume) VALUES (?, ?, ?, ?, ?, ?, ?)", row)
        count += 1
    print(f"Processed {tid}: deleted {count} duplicate rows")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Connect to the database
conn = sqlite3.connect('trades.db')

# Create a cursor object
cursor = conn.cursor()

# Find the duplicate tid values in the table
query = '''
    SELECT tid, COUNT(*) as count
    FROM trades
    GROUP BY tid
    HAVING count > 1;
'''

duplicate_tids = [tid for tid, _ in cursor.execute(query).fetchall()]

# Divide the list of duplicate tids into sublists
num_threads = 4
batch_size = len(duplicate_tids) // num_threads
batches = [duplicate_tids[i:i+batch_size] for i in range(0, len(duplicate_tids), batch_size)]

# Process each batch on a separate thread
with ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = [executor.submit(process_duplicate_tid, tid) for batch in batches for tid in batch]

# Close the connection
conn.close()
