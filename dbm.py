import sqlite3

DATABASE_NAME = "inventory.db"

def connect_db():
    """Connects to the SQLite database and returns the connection object."""
    return sqlite3.connect(DATABASE_NAME)

def create_table():
    """Creates the inventory table if it does not exist."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                item_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                image_path TEXT
            )
        """)
        conn.commit()

def insert_item(item_name, quantity, image_path):
    """Inserts a new item into the inventory table."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO inventory (item_name, quantity, image_path) VALUES (?, ?, ?)", 
                       (item_name, quantity, image_path))
        conn.commit()

def get_all_items():
    """Retrieves all items from the inventory."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT rowid, * FROM inventory")
        return cursor.fetchall()

def update_item_quantity(item_id, new_quantity):
    """Updates the quantity of an item by its rowid."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE inventory SET quantity = ? WHERE rowid = ?", 
                       (new_quantity, item_id))
        conn.commit()

def delete_item(item_id):
    """Deletes an item from the inventory by its rowid."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE rowid = ?", (item_id,))
        conn.commit()

# Call create_table() to ensure the database and table exist when the app starts
create_table()