# 🧾 Export 0DTE Options to TOS Watchlist

This script automates the creation of **ThinkorSwim (TOS) watchlist import files** for **0DTE (Zero Days to Expiration)** options.  
It uses data from **Yahoo Finance** to identify **At-The-Money (ATM)** options and exports both **calls** and **puts** around the current price.

---

## 🧠 Overview

After running the script, it creates two text files (calls and puts) that you can directly import into a TOS watchlist.  
Each file contains formatted option symbols in **TOS import format**.

**Example output:**
options-chains/
├── SPY_CALLS_watchlist_2025-10-06.txt
└── SPY_PUTS_watchlist_2025-10-06.txt

**TOS symbol format example:**
.SPY251006C664
.SPY251006P664

---

## ⚙️ Features

- Pulls latest market data using **Yahoo Finance**
- Determines the **At-The-Money (ATM)** strike automatically
- Selects a range of strikes (default ±5)
- Generates **separate watchlist files** for Calls and Puts
- Compatible with **ThinkorSwim watchlist import** feature

---

## 🧩 Parameters

| Parameter | Type | Default | Description |
|------------|------|----------|--------------|
| `symbol` | `str` | `"SPY"` | Underlying asset symbol |
| `n_strikes` | `int` | `5` | Number of strikes above and below ATM |
| `output_folder` | `str` | `"./options-chains"` | Folder for exported files |
| `date` | `str` | `None` | Expiration date (`YYYY-MM-DD`). Defaults to today. |

---

## 🚀 Example Usage

### Run from Python
from import_options_0dte import export_tos_0dte_watchlist

Use today’s expiration
export_tos_0dte_watchlist(symbol="SPY", n_strikes=5)

Or specify a future expiration date
export_tos_0dte_watchlist(symbol="SPY", n_strikes=5, date="2025-10-06")

### Run from PowerShell
& "C:\path\to\python.exe" "C:\path\to\import-options-0dte.py"

---

## 📦 Installation

Install required dependencies:
pip install yfinance pandas

---

## 📂 Output Files

| File | Description |
|------|--------------|
| `SYMBOL_CALLS_watchlist_YYYY-MM-DD.txt` | Call options in TOS format |
| `SYMBOL_PUTS_watchlist_YYYY-MM-DD.txt` | Put options in TOS format |

Each file contains one TOS-formatted option symbol per line — ready for import into ThinkorSwim.

---

## 🧭 Import into ThinkorSwim

1. In **TOS**, right-click any **Watchlist** panel.  
2. Choose **Import → From File...**  
3. Select one of the exported `.txt` files.  
4. The watchlist will populate with your chosen strikes.

---

## 🧱 Example Output (SPY 0DTE)

Example with `symbol="SPY"`, `date="2025-10-06"`, and `n_strikes=5`:
options-chains/
├── SPY_CALLS_watchlist_2025-10-06.txt
└── SPY_PUTS_watchlist_2025-10-06.txt

Each file contains:
.SPY251006C662
.SPY251006C663
.SPY251006C664
.SPY251006C665
.SPY251006C666

---

## 🧰 Notes

- The ATM strike is determined by comparing strikes to the **last closing price**.
- Expiration dates are pulled from Yahoo Finance’s listed options chain.
- The script validates that the provided expiration date exists for the chosen symbol.

---

## 🏁 Example Console Output
Exported 11 calls → ./options-chains/SPY_CALLS_watchlist_2025-10-06.txt
Exported 11 puts → ./options-chains/SPY_PUTS_watchlist_2025-10-06.txt

---

## 📜 License

This project is open-source and provided **as-is** without warranty.  
Use at your own discretion for educational or personal trading workflow automation.

---

**Author:** Damien Johnston  
**Last updated:** 2025-10-04