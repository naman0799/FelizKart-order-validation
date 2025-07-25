# FelizKart Order Validation Pipeline #

A real-world inspired data validation project simulating a retail order processing system. Built with **pure Python**, this project performs file-based ETL-style validations on daily order files from an imaginary online marketplace: **FelizKart**.

> Ideal for showcasing real-time file ingestion, data quality validation, rejection handling, and simulated business notification via email.

---

## Project Overview

**FelizKart** operates in 3 cities: **Delhi, Bengaluru, and Mumbai**.
Every day, it generates transaction files containing orders which are sent to a centralized processing team. Your job is to:

1. **Ingest** daily transaction files
2. **Validate** each order record
3. **Separate valid and invalid files**
4. **Log errors with reasons for rejection**
5. **Send a summary email to business**

---

## Core Functionalities

### ✅ Validation Rules

Each order must:

* Have a **valid product ID** (checked against `product_master.csv`)
* Have **non-empty fields** (no missing values)
* Come from **allowed cities** only (Delhi, Bengaluru, Mumbai)
* Have a **valid date** (no future dates)
* Have a **correct sales value** = price × quantity

### Folder Architecture

```
FelizKart/
├── code/
│   ├── main_kart.py             ← Main driver program
│   ├── validator.py             ← All business rule validations
│   ├── emailer.py               ← Sends summary email (or simulates)
│   ├── file_reader.py           ← Reads files and handles file errors
│   └── test_validator.py        ← Unit tests using pytest
├── product_master/
│   └── product_master.csv       ← Product ID and price master data
├── incoming_files/
│   └──20240725/                 ← Files from current date
├── success_files/
│   └──20240725/                 ← All clean, validated files
├── rejected_files/
│   └──20240725/
│       ├─ error_orders1.csv     ← Only rejected orders with reasons
│       └─ orders1.csv           ← Original rejected file
└── README.md
```

---

## How It Works

1. **Run `main_kart.py`** from the `code/` folder
2. It checks today's date folder in `incoming_files/YYYYMMDD/`
3. For each file:

   * Applies validations from `validator.py`
   * Moves to `success_files/` if all records are clean
   * Moves to `rejected_files/` if any record fails validation
   * Creates `error_*.csv` with rejection reasons
4. Finally, it **sends an email** (or simulates one) summarizing the number of successful and failed files

---

## 📆 Example Email Output (Simulated)

```
To: abc123@gmail.com
Subject: Validation email for 2025-07-25

Body:
Total Files: 10
Successful Files: 8
Rejected Files: 2
```

---

## Skills Demonstrated

* Python scripting & file handling
* Custom validation rules
* Error logging & rejection tracing
* Email automation (via `smtplib` or simulated)
* Directory-based batch processing
* Modular programming (clean code separation)
* Unit testing with `pytest`

---

## 🔧 How to Run Locally

### Prerequisites

* Python 3.7+
* `product_master.csv` file in `/product_master/`
* Create input files in `/incoming_files/YYYYMMDD/` format
* (Optional) Set up `.env` or environment variable for `EMAIL_APP_PASSWORD`

### Run:

```bash
cd code
python main_kart.py
```

---

## Future Enhancements

* ♻️ Add Pandas to simplify row operations
* 🚀 Extend with database ingestion (load into SQL Server)
* 🛌 Connect with real SMTP to enable actual email delivery
* 📈 Visualize reports in a dashboard (e.g., Streamlit or Power BI)

---

## Author

**Naman Sharma**
[LinkedIn](https://www.linkedin.com/in/naman-sharma-ds/)
