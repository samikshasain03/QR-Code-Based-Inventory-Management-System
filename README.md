# 📦 QR Code-Based Inventory Management System

A simple yet powerful **Inventory Management System** built with **Python + SQLite**, featuring **QR Code integration** for product tracking.

This project demonstrates:

* 🐍 **Programming skills** → custom Python scripts for DB management, scanning & processing
* 📊 **Data Analytics skills** → stock/sales visualizations using `matplotlib`
* 🔍 **Real-world problem-solving** → track products by batch, check expiry, handle out-of-stock, and log transactions

---

## 🚀 Features

✅ **Add Products & Batches**

* Store product details (name, category)
* Add multiple batches per product (with unique `batch_id`)
* Automatically generates a **QR code** for each batch

✅ **Scan Products via QR**

* Decode QR codes (from image path for now; later can be upgraded to webcam/app)
* On scan:

  * Reduce stock count
  * Detect expired products
  * Mark as out of stock if inventory = 0

✅ **Transaction Logging**

* Every scan is recorded in a **Transactions** table with status:

  * `OK` → valid sale
  * `EXPIRED` → expired batch
  * `OUT_OF_STOCK` → no stock left

✅ **Dashboard & Data Analytics**

* 📊 Stock levels visualization (per batch)
* 📊 Sales per product (count of successful scans)
* ⚠️ Expired products list
* 📝 Recent transactions log

---

## 📂 Project Structure

```
QR-Code-Based-Inventory-Management-System/
│
├── Scripts/               # All Python scripts
│   ├── init_db.py         # Initialize database schema
│   ├── add_products.py    # Add new products + batches + generate QR
│   ├── scan.py            # Scan QR codes & process transactions
│   ├── dashboard.py       # Visualize stock, sales, expired, transactions
│
├── Qr_codes/              # Folder where generated sample QR codes are saved
│   └── *.png
```

## ⚙️ How to Run

### 1️⃣ Setup

* Clone this repo
* Make sure you have **Python 3.10+** installed
* Install dependencies:

```bash
pip install qrcode[pil] opencv-python pyzbar matplotlib
```

### 2️⃣ Initialize Database

Run once to create `inventory.db`:

```bash
python Scripts/init_db.py
```

### 3️⃣ Add Products & Batches

```bash
python Scripts/add_products.py
```

👉 This will:

* Ask for product details
* Create entries in DB
* Generate a QR code in `/Qr_codes/`

### 4️⃣ Scan Products

```bash
python Scripts/scan.py
```

👉 Enter the path of the QR code image (e.g., `Qr_codes/product_batch_xxxx.png`)

System will:

* Check expiry
* Update stock
* Insert transaction record

### 5️⃣ View Dashboard

```bash
python Scripts/dashboard.py
```

👉 Displays:

* Stock per batch (bar chart)
* Sales per product (bar chart)
* Expired product warnings
* Recent transactions

---

## 🔮 Future Improvements

🚧 Planned features:

* Live QR scanning via **webcam**
* Web or Mobile App for user-friendly interface
* Export reports (PDF/Excel)
* Role-based access (Admin, Staff)
* Power BI integration for advanced analytics
* Notifications & alerts for expiry dates and stock

---

## 🎥 Demo

I’ve made a **demo video** showing:

* Adding products
* Scanning them
* Checking dashboard updates

🔗 [LinkedIn](https://www.linkedin.com/in/samiksha-sain/)
---

## 🧑‍💻 Author

👋 Hi, I’m **Samiksha Sain**

* Aspiring **Data Analyst / Python Developer**
* Building real-world projects to combine **programming + analytics**
* [Connect on LinkedIn](https://www.linkedin.com/in/samiksha-sain/)

---

⚡ If you like this project, consider giving it a ⭐ on GitHub!

---

👉 That’s the **README.md** template. Once you paste it locally, GitHub will render it beautifully (with headings, emojis, code blocks, etc.).

---

Do you also want me to create a **short `requirements.txt` file** so people can install dependencies in one go?

