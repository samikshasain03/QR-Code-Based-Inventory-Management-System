# dashboard.py
import sqlite3
import matplotlib.pyplot as plt
from datetime import date

def dashboard():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    # ✅ 1. Stock levels
    cursor.execute("""
        SELECT pm.prod_name, b.batch_id, b.stock, b.exp_date
        FROM Batches b
        JOIN Products_Master pm ON b.product_id = pm.product_id
    """)
    batches = cursor.fetchall()
    product_labels = [f"{prod_name}\n({batch_id[:6]})" for prod_name, batch_id, stock, exp in batches]
    stocks = [stock for _, _, stock, _ in batches]

    # ✅ 2. Expired products
    today = date.today().isoformat()
    expired = [(prod_name, batch_id, exp) for prod_name, batch_id, stock, exp in batches if exp <= today]

    # ✅ 3. Recent transactions
    cursor.execute("""
        SELECT t.id, pm.prod_name, t.batch_id, t.scan_time, t.status
        FROM Transactions t
        JOIN Batches b ON t.batch_id = b.batch_id
        JOIN Products_Master pm ON b.product_id = pm.product_id
        ORDER BY t.scan_time DESC
        LIMIT 10
    """)
    Transactions = cursor.fetchall()

    # ✅ 4. Sales per product (transaction count)
    cursor.execute("""
        SELECT pm.prod_name, COUNT(*) as sales_count
        FROM Transactions t
        JOIN Batches b ON t.batch_id = b.batch_id
        JOIN Products_Master pm ON b.product_id = pm.product_id
        WHERE t.status = 'OK'
        GROUP BY pm.prod_name
        ORDER BY sales_count DESC
    """)
    sales = cursor.fetchall()
    conn.close()

    # 📊 Stock levels
    plt.figure(figsize=(10, 6))
    plt.bar(product_labels, stocks, color="skyblue")
    plt.title("Stock Levels per Batch")
    plt.ylabel("Quantity")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()

    if sales:
        plt.figure(figsize=(10, 6))  # make the chart bigger
        names = [row[0] for row in sales]
        counts = [row[1] for row in sales]
        # Bar chart with border for clarity
        plt.bar(names, counts, color="lightgreen", edgecolor="black")
        # Titles and labels with better font sizes
        plt.title("Sales Count per Product", fontsize=16, fontweight="bold")
        plt.ylabel("Transactions (Sales)", fontsize=14)
        plt.xlabel("Products", fontsize=14)
        # Make axis labels more readable
        plt.xticks(rotation=25, ha="right", fontsize=11)
        plt.yticks(fontsize=12)
        
        for i, count in enumerate(counts):
            plt.text(i, count + 0.1, str(count), ha="center", fontsize=12, fontweight="bold")
        
         # Optional: grid for y-axis
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.show()
    else:
        print("\nℹ️ No sales data available yet.")

    # ⏰ Expired products
    if expired:
        print("\n⚠️ Expired Products:")
        for prod_name, batch_id, exp in expired:
            print(f" - {prod_name} (Batch {batch_id[:6]}) expired on {exp}")
    else:
        print("\n✅ No expired products.")

    # 📝 Recent transactions
    print("\n📜 Recent Transactions:")
    for id, prod_name, batch_id, scan_time, status in Transactions:
        print(f"[{scan_time}] {prod_name} (Batch {batch_id[:6]}) → {status}")

if __name__ == "__main__":
    dashboard()
