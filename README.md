# Automations

A collection of personal automation scripts and LLM system prompt agents to manage invoicing, monthly expenses classification, and study coaching.

## Project Structure

```
automations/
├── README.md               # Project overview and directory documentation
├── expenses/               # Monthly expenses classification system
│   ├── system_prompt.md    # Self-contained instructions for the LLM Agent
│   └── input/              # Monthly folders containing source statements and ledgers
├── invoicing/              # Python invoicing automation project
│   ├── pyproject.toml      # Poetry configuration & dependencies
│   ├── src/                # Invoicing source code
│   └── environment/        # Credentials & configuration (ignored by Git)
└── study/                  # LLM study assistant configurations
    └── system_prompt.md    # Self-contained instructions for LLM Study Coach
```

---

## 1. Invoicing Automation

A Python script located in the `invoicing/` folder that automates the generation and archiving of monthly client invoices.

### Setup & Execution
1. Navigate to `invoicing/` and install dependencies:
   ```bash
   cd invoicing
   poetry install
   ```
2. Configure credentials in `invoicing/environment/invoicing/credentials.json` and settings in `invoicing/environment/invoicing/.env`.
3. Run the automation:
   ```bash
   poetry run invoicing
   ```

---

## 2. Monthly Expense Classifier

An LLM-based agent configured via the self-contained instructions in [expenses/system_prompt.md](file:///Users/javiroberts/workspace/automations/expenses/system_prompt.md). It processes monthly bank/credit card statements placed under `expenses/input/<YYYYMM>/` and produces a consolidated `ledger.csv` file.

Please refer directly to [expenses/system_prompt.md](file:///Users/javiroberts/workspace/automations/expenses/system_prompt.md) for details on supported file formats, parsing rules, strict month filtering, classification rules, and ledger output conventions.

---

## 3. LLM Study Coach

An LLM-based study assistant configured via the self-contained instructions in [study/system_prompt.md](file:///Users/javiroberts/workspace/automations/study/system_prompt.md) to guide you through exam practice.
