# HP Inc — Inventory & Billing Automation

> ETL pipeline for automatic WMS↔ERP inventory reconciliation and monthly LSP billing automation. Built and deployed in production for HP Inc Chile's logistics operation.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=white)
![SAP](https://img.shields.io/badge/SAP_S%2F4HANA-0FAAFF?style=flat&logo=sap&logoColor=white)

---

## Impact

| Project | Before | After |
|---|---|---|
| Monthly LSP billing | 3 days of manual work | **4 hours · 100% accuracy** |
| WMS↔SAP reconciliation | Daily manual process | **Fully automated** · freed inventory control operator |
| Rework extraction | Manual Word review | **Automated** · structured database output |

---

## Context

HP Inc outsources its logistics operation to a 3PL provider (DHL). Every month, the LSP invoices for services rendered: warehousing, reworks (product conditioning for MTO/BTO orders), and special operations. In parallel, the LSP's inventory system (WMS) and HP's ERP (SAP S/4) must stay permanently reconciled.

Before these automations, the process required manually downloading reports from three different systems, cross-referencing them in Excel, and generating invoices — a 3-day process that also produced frequent billing errors requiring corrections.

---

## Scripts

### `revision_stock.py` — Delivery generation prediction
Crosses available stock in SAP S/4 against the open order backlog, applies delivery block criteria from the regional User Status Playbook, and predicts which orders can generate a delivery immediately. Allows the warehouse team to plan operations ahead of time.

**Core logic:**
1. Available stock in S/4 (excluding location 1005)
2. Minus: stock already consumed by existing deliveries
3. Minus: stock reserved by blocked purchase orders
4. Result: `AvailableStock` → `Generates?` column (True/False)

**Stack:** Python · pandas · SAP S/4

---

### `extraccion_retrabajos.py` — Word table extractor for rework orders
Processes folders of Word (.docx) documents containing MTO/BTO rework orders, extracts all tables from each document, and structures the data into a CSV file for analysis and billing purposes.

**Stack:** Python · python-docx · openpyxl

---

### `conversor_html.py` — HTML to Excel report converter
Converts `.html` files (reports exported from legacy WMS systems) to clean `.xlsx` format. Used frequently by the team when working with WMS reports that only export as HTML.

**Stack:** Python · pandas · lxml · openpyxl  
**Usage:** Interactive — prompts for the file path via console

---

## Setup

```bash
git clone https://github.com/your-username/hp-inventory-billing
cd hp-inventory-billing
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your values:

```env
# revision_stock.py
PATH_STOCK=path/to/stock_s4.xlsx
PATH_BACKLOG=path/to/backlog.xlsx
PATH_WORKBOOK=path/to/playbook.xlsx
PATH_CHARLIELIST=path/to/charlie_list.xlsx
PATH_OUTPUT=path/to/output_stock.xlsx

# extraccion_retrabajos.py
PATH_OUTPUT=path/to/retrabajos_output.csv

# conversor_html.py
OUTPUT_PATH=path/to/output.xlsx
```

---

## Dependencies

```
pandas>=1.3
openpyxl
python-dotenv
python-docx
lxml
```

---

## Author

**Vicente Arasaya**  
Supply Chain & Operations Automation · HP Inc Chile  
[linkedin.com/in/your-profile](https://linkedin.com/in/your-profile) · [github.com/your-username](https://github.com/your-username)
