import sqlite3
from pyzbar.pyzbar import decode 
import cv2 as cv
from datetime import datetime

#scanning procedure code 

#cv code 

def scan_qr(image_path):
    img = cv.imread(image_path)
    codes = decode(img)

    if not codes:
        raise ValueError("QR code not found in the image.")

    # If multiple QR codes are found, just take the first one
    batch_id = codes[0].data.decode("utf-8")
    return batch_id

#processing 

def process_scan(batch_id):
    
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    
    cursor.execute(""" 
                   SELECT product_id, mfd_date, exp_date, stock
                   FROM Batches
                   WHERE batch_id= ?
                   """,(batch_id,))
    row= cursor.fetchone()
    
    if not row:
        print("Invalid Batch ID ! NOT found in Database.")
        conn.close()
        return 
    
    product_id, mfd_date, exp_date, stock = row
    #get the names of the products 
    
    cursor.execute("""
                   SELECT prod_name
                   FROM Products_master 
                   WHERE product_id=?
                   """, (product_id,))
    product_name= cursor.fetchone()[0]
    
    today= datetime.today().date()
    exp_date= datetime.strptime(exp_date, "%Y-%m-%d").date()
    
    if today>=exp_date:
        status= "EXPIRED"
        print(f"⚠️ {product_name} (Batch {batch_id}) is expired!")
    elif stock > 0:
        status = "OK"
        cursor.execute("UPDATE Batches SET stock = stock - 1 WHERE batch_id = ?", (batch_id,))
        print(f"✅ Scanned {product_name} (Batch {batch_id}). Stock reduced to {stock - 1}.")
    else:
        status = "OUT_OF_STOCK"
        print(f"❌ {product_name} (Batch {batch_id}) is out of stock!")
    
    
    cursor.execute(""" 
                   INSERT INTO Transactions (batch_id, status)
                   VALUES(?,?)""",(batch_id, status))
    conn.commit()
    conn.close()
    
    
    
if __name__ == "__main__":
    image_path= input("Enter the path to the image: ").strip()
    
    try:
        batch_id= scan_qr(image_path)
        process_scan(batch_id)
    except ValueError as e:
        print(e)
    