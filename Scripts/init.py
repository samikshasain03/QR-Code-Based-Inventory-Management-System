import sqlite3

def init_db():
    
    #connect to the SQLITE DATABASE 
    
    conn= sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    
    #enable the foreign key 
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    #product table 
    cursor.execute("""
                   
                   CREATE TABLE IF NOT EXISTS Products_master(
                       
                       product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       prod_name TEXT UNIQUE NOT NULL,
                       category TEXT
                   )
                   
                   """)
    #Batches table - stores each batch of a product
    cursor.execute(""" 
                   
                   CREATE TABLE IF NOT EXISTS Batches(
                       batch_id TEXT PRIMARY KEY,
                       product_id INTEGER NOT NULL,
                       mfd_date DATE NOT NULL,
                       exp_date DATE NOT NULL,
                       stock INTEGER NOT NULL CHECK (stock >= 0),
                       FOREIGN KEY (product_id) REFERENCES Products_master(product_id)
                       )""")
    
    #transaction table 
    cursor.execute(""" 
                   
                   CREATE TABLE IF NOT EXISTS Transactions(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       batch_id TEXT NOT NULL,
                       scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       status TEXT CHECK (status IN ('OK','EXPIRED','OUT_OF_STOCK')),
                       FOREIGN KEY (batch_id) REFERENCES Batches(batch_id)
                       
                   )
                   """)
    conn.commit()
    conn.close()
    print("Database schema created succcesfully")
    
if __name__ == "__main__":
    init_db()