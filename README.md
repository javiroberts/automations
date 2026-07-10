# Automations

A collection of personal automation scripts and LLM system prompt agents to manage invoicing, monthly expenses classification, and study coaching.

## Project Structure

```
automations/
├── README.md               # Project overview and documentation
├── expenses/               # Monthly expenses classification system
│   ├── system_prompt.md    # Instructions for the Expense Classifier LLM Agent
│   └── input/              # Monthly folders containing source statements and ledgers
│       ├── 202605/         # May 2026 statements & ledger
│       └── 202606/         # June 2026 statements & ledger
├── invoicing/              # Python invoicing automation project
│   ├── pyproject.toml      # Poetry configuration & dependencies
│   ├── poetry.lock         # Lockfile for reproducible builds
│   ├── src/                # Invoicing source code
│   │   └── invoicing/
│   │       ├── __init__.py
│   │       └── main.py     # Main invoicing automation script
│   └── environment/        # Credentials & configuration (ignored by Git)
│       └── invoicing/
│           ├── .env
│           └── credentials.json
└── study/                  # LLM study assistant configurations
    └── system_prompt.md    # System prompt for LLM Study Coach
```

---

## 1. Invoicing Automation

The `invoicing` module is a Python script that automates the generation and archiving of monthly client invoices.

### How It Works
1. **Google Sheets Template Update**: Connects to a template invoice on Google Sheets using Service Account credentials. Updates the client name, submission date, payment due date, and invoice amount, then increments the invoice number.
2. **Export to PDF**: Exports the Google Sheet template as a high-quality PDF.
3. **Upload to Google Drive**: Uploads the generated PDF invoice to a designated archive folder in Google Drive.
4. **Cleanup**: Automatically deletes the local temporary PDF.

### Prerequisites & Setup
Make sure you have [Poetry](https://python-poetry.org/) and Python >= 3.13 installed.

1. Navigate to the `invoicing/` directory:
   ```bash
   cd invoicing
   ```
2. Install the dependencies:
   ```bash
   poetry install
   ```
3. Set up Google credentials:
   - Create a Google Cloud Project and enable the Google Sheets and Google Drive APIs.
   - Generate a Service Account key and save the JSON file as `environment/invoicing/credentials.json`.
4. Configure the environment variables in `environment/invoicing/.env`:
   ```env
   CUSTOMER_SHORTCODE=CLIENT_CODE
   CUSTOMER_NAME="Client Name Ltd."
   INVOICE_AMOUNT=1500.00
   FILE_ID="your_google_sheet_file_id"
   FOLDER_ID="your_google_drive_folder_id"
   ```

### Execution
Run the script using Poetry:
```bash
poetry run invoicing
```

---

## 2. Monthly Expense Classifier

The `expenses` module provides the system instructions and workspace conventions to run an **LLM-based Expense Classifier Agent** that processes monthly bank statements and produces a consolidated accounting ledger.

### How It Works
1. **Input Stage**: Source statements (PDFs, XLS, or CSV files) are placed under `expenses/input/<YYYYMM>/`.
2. **Strict Month Filtering**: The agent scans the folder and extracts transactions, filtering them strictly by the target month. Transactions from other months are discarded.
3. **Currency Conversion & Normalization**: Galicia credit card dollar amounts are converted to EUR (using a reference exchange rate). Santander, Galicia, and N26 files are parsed, deduplicated, and unified.
4. **Classification Engine**: Transactions are classified into categories (`School fees`, `Travel`, `Restaurants`, `Small expenses`, `Home/Groceries`, `Shopping`, `Subscriptions/Recurring`, `Rent`, `Third-party transfers`) based on a hard-mapped keyword list and a prioritized fallback rule set.
5. **Output Ledger**: Saves the results directly to `expenses/input/<YYYYMM>/ledger.csv` in a clean, sorted CSV format.

### Supported Sources
* **Santander España (`Santander_ES`)**: Formatted as CSV, XLS, or PDF.
* **Galicia Credit Cards (`Galicia_TC_Master` / `Galicia_TC_Visa`)**: PDF statements (Argentina). Converts foreign currencies (USD) to EUR. Skips ARS transactions.
* **N26 Bank (`N26`)**: CSV statements (Europe). Standardizes dates, concatenates payees/references, and normalizes amounts.
* **Personal Logs (`Personal_Log`)**: Manual CSV/TXT transaction sheets.

### Ledger Output Conventions
The resulting `ledger.csv` uses the following formats:
- **Columns**: `Date,Source,Category,Description,Amount EUR`
- **Date format**: `M/D/YY` (e.g. `5/1/26` or `6/30/26`).
- **Amount EUR format**: Accounting-style currency notation:
  - **Negative (Outflows)**: ` $(X.XX)` (e.g. ` $(9.76)`). Wrap in quotes if over €1,000 to handle commas: `" $(1,492.29)"`.
  - **Positive (Inflows)**: ` $X.XX ` with a trailing space (e.g. ` $41.15 `).

### Running the Classifier Agent
Feed the instructions in [expenses/system_prompt.md](file:///Users/javiroberts/workspace/automations/expenses/system_prompt.md) to your LLM agent context, specifying the month you want to run (e.g., `/month 202605` or "generate the ledger for June 2026").

---

## 3. LLM Study Coach

The `study` module contains the system instructions for configuring a personal exam preparation coach agent. 

* The instructions are located in [study/system_prompt.md](file:///Users/javiroberts/workspace/automations/study/system_prompt.md).
* The coach helps guide the user through exam problems by offering hints, identifying errors, and asking leading questions rather than giving direct answers, building problem-solving intuition.
