import sqlite3
import uuid
import qrcode
import os 
from datetime import datetime, date
import re


#function to products in the inventory 
def add_products():
    
    #connect to the Database 
    
    conn= sqlite3.connect("inventory.db")
    cursor= conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    
    #make the directory for the Qr codes 
    
    if not os.path.exists("Qr_codes"):
        os.makedirs("Qr_codes")
        
    #lets iterate now 
    while True:
        
        #product name entry 
        name = input ("Enter the Product Name: ").strip()
        if not name:
            print("Product name cannot be empty.")
            continue
        
        category= input("Enter the Product Category:").strip()
        
        cursor.execute("SELECT product_id FROM Products_master WHERE prod_name= ?",(name,))
        row= cursor.fetchone()
        
        if row:
            product_id=row[0]
            print(f"Product already exists iN the database (Product_id={product_id}.")
        else:
            cursor.execute("INSERT INTO Products_master(prod_name,category) VALUES (?,?)", (name, category) )
            conn.commit()
            product_id = cursor.lastrowid
            print(f"✅ Added new product to Products_Master with Product_id={product_id}.")
        
        
        
        # Batch Details Entry
        
        #manufacturing date entry 
        mfg_input = input("Enter the Manufacturing Date (YYYY-MM-DD): ").strip()
        if mfg_input:
            try:
                mfd_date = datetime.strptime(mfg_input, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
        else:
            mfd_date =date.today()
            
            
        #expriry date formatting 
        exp_input = input("Enter the Expiry Date (YYYY-MM-DD):").strip()
        try:
            exp_date = datetime.strptime(exp_input, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid. Enter Valid expiry date.")
            
        if exp_date <=mfd_date:
            print("Expiry date must be after manufacture date.")
            continue
        
        #stock entry 
        try:
            stock_input = input("Enter Stock Quantity: ").strip()
            stock = int(stock_input)
            if stock < 0:
                raise ValueError
        except ValueError:
            print("Stock must be a non-negative integer.")
            continue
        
        # 5️⃣ Generate batch_id and QR code
        batch_id = str(uuid.uuid4())
        # Create safe product name for filename (replace spaces with underscores)
        safe_name = re.sub(r'[^A-Za-z0-9]+', '_', name).strip("_")
        # Shorten batch_id for filename readability
        short_id = batch_id[:6]
        # Save QR with product name + short batch id
        filename = f"{safe_name}_batch_{short_id}.png"
        qr_path = os.path.join("Qr_codes", filename)
        qr = qrcode.make(batch_id)
        qr.save(qr_path)
        
        #insert the data into the database 
        cursor.execute(""" 
                       INSERT INTO Batches(batch_id,product_id,mfd_date,exp_date,stock) VALUES (?,?,?,?,?)""",
                       (batch_id,product_id,mfd_date.isoformat(),exp_date.isoformat(),stock))
        conn.commit()
        
         # ---- Feedback ----
        print("\n✅ Batch created successfully!")
        print(f"   Product       : {name}")
        print(f"   Category      : {category or '(none)'}")
        print(f"   Batch ID      : {batch_id}")
        print(f"   MFD Date      : {mfd_date.isoformat()}")
        print(f"   EXP Date      : {exp_date.isoformat()}")
        print(f"   Stock         : {stock}")
        print(f"   QR Code Path  : {qr_path}\n")
        
        
        again= input ("Do you want to add more products ? (y/n): ").strip().lower()
        if again != "y":
            break
        
    conn.close()
    print("\n🎉 Finished adding products!")
        
if __name__ == "__main__":
    add_products()
    