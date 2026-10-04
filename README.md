# Fulfillment Hub — XYZ Operations Analyst Take-Home

A lightweight Streamlit prototype designed to improve visibility and exception handling in XYZ's e-commerce fulfillment workflow.

## Problem Focus

The prototype focuses on four operational problems from the assignment:

1. Lack of order status visibility
2. Priority orders and shipment deadlines being missed
3. Inventory mismatch and stock needing transfer from the secondary warehouse
4. Operational exceptions being handled informally and forgotten

The goal is not to build a full ERP system. The goal is to give the office and warehouse teams one simple place to see what needs attention first.

## Features

- Dashboard showing order, priority, overdue, stock-blocked, and staging metrics
- Order queue with search and filters
- Priority and shipment-deadline visibility
- Inventory view showing Main WH and Secondary WH stock
- Transfer-needed and low-stock flags
- Exception queue with recommended actions
- Fictional sample data for demonstration

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py