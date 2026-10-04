# AI Usage Note — Fulfillment Hub

I used AI tools as a brainstorming and development assistant while building this prototype. I remained responsible for deciding which problems to solve, how the workflow should work, and which suggestions were practical for the XYZ scenario.

## How I Used AI

- Used AI to brainstorm ways to translate the fulfillment workflow into a simple operations application.
- Used AI to suggest sample order and inventory data that could demonstrate common fulfillment exceptions.
- Used AI assistance for the initial Streamlit/Python implementation, UI structure, and code organization.
- Reviewed and tested the suggested logic against the assignment workflow before including it in the prototype.

## Where I Applied My Own Judgment

### 1. Kept the application intentionally simple

A more complex system could include authentication, barcode scanning, courier API integrations, automated label generation, and a database. I did not make these core features because the assignment describes a small team currently using spreadsheets and notes that the warehouse team is not very comfortable with technology.

I therefore focused on a small number of clear screens and visible actions instead of building a complex enterprise system.

### 2. Prioritized exceptions instead of adding more dashboards

AI-generated ideas can easily lead to adding many charts and metrics. I chose to make the main dashboard answer a practical question first:

**What needs attention right now?**

Priority orders, overdue orders, stock-blocked orders, and staging/pickup risks are surfaced because they can directly affect fulfillment.

## My Judgment

The prototype is intentionally a proof of workflow rather than a production ERP system. The sample data is fictional. The application could later be connected to real order, inventory, and courier systems if XYZ requires those capabilities.

The final scope and prioritization were based on my understanding of the assignment and the operational problems described in it.
