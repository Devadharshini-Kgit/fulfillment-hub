import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="Fulfillment Hub", page_icon="📦", layout="wide")

# -----------------------------
# Sample data
# -----------------------------
NOW = datetime(2026, 10, 5, 10, 0)

orders = pd.DataFrame([
    ["ORD-1001", "Priya S", "Wireless Earbuds", "Black", "Priority", "Processing", NOW + timedelta(hours=1), "ShipRocket"],
    ["ORD-1002", "Arun K", "Running Shoes", "Blue-9", "Regular", "Picking", NOW + timedelta(hours=6), "Delhivery"],
    ["ORD-1003", "Meena R", "Cotton Kurti", "Maroon-M", "Priority", "Awaiting Stock", NOW + timedelta(minutes=45), "BlueDart"],
    ["ORD-1004", "Rahul P", "Laptop Stand", "Silver", "Regular", "Packed", NOW + timedelta(hours=8), "Delhivery"],
    ["ORD-1005", "Divya N", "Water Bottle", "1L-Black", "Regular", "Staging", NOW + timedelta(hours=2), "ShipRocket"],
    ["ORD-1006", "Karthik V", "Wireless Mouse", "White", "Priority", "Picking", NOW - timedelta(minutes=20), "BlueDart"],
    ["ORD-1007", "Sneha M", "Yoga Mat", "Purple", "Regular", "Processing", NOW + timedelta(hours=5), "Delhivery"],
    ["ORD-1008", "Vijay S", "T-Shirt", "Black-L", "Priority", "Packed", NOW + timedelta(hours=1, minutes=30), "ShipRocket"],
    ["ORD-1009", "Nisha P", "Phone Case", "iPhone 15-Clear", "Regular", "Picking", NOW + timedelta(hours=7), "Delhivery"],
    ["ORD-1010", "Suresh G", "Cotton Kurti", "Maroon-L", "Regular", "Awaiting Stock", NOW + timedelta(hours=4), "BlueDart"],
    ["ORD-1011", "Anitha R", "Bluetooth Speaker", "Black", "Priority", "Staging", NOW - timedelta(minutes=10), "ShipRocket"],
    ["ORD-1012", "Manoj T", "Running Shoes", "Black-10", "Regular", "Shipped", NOW + timedelta(days=1), "Delhivery"],
], columns=["Order ID", "Customer", "Product", "Variant", "Priority", "Status", "Ship By", "Courier"])

inventory = pd.DataFrame([
    ["P001", "Wireless Earbuds", "Black", 12, 3, 8, 5, "OK"],
    ["P002", "Running Shoes", "Blue-9", 4, 0, 6, 4, "OK"],
    ["P002", "Running Shoes", "Black-10", 1, 5, 4, 3, "OK"],
    ["P003", "Cotton Kurti", "Maroon-M", 0, 7, 5, 2, "Transfer needed"],
    ["P003", "Cotton Kurti", "Maroon-L", 1, 0, 4, 2, "Low stock"],
    ["P004", "Laptop Stand", "Silver", 7, 0, 5, 2, "OK"],
    ["P005", "Water Bottle", "1L-Black", 10, 2, 6, 4, "OK"],
    ["P006", "Wireless Mouse", "White", 2, 0, 5, 3, "Low stock"],
    ["P007", "Yoga Mat", "Purple", 8, 0, 5, 3, "OK"],
    ["P008", "T-Shirt", "Black-L", 6, 0, 5, 2, "OK"],
    ["P009", "Phone Case", "iPhone 15-Clear", 0, 8, 4, 3, "Transfer needed"],
    ["P010", "Bluetooth Speaker", "Black", 3, 0, 5, 2, "Low stock"],
], columns=["SKU", "Product", "Variant", "Main WH", "Second WH", "Today Demand", "Reorder Point", "Inventory Flag"])

# -----------------------------
# Helpers
# -----------------------------
def urgency(row):
    minutes = (row["Ship By"] - NOW).total_seconds() / 60
    if row["Status"] in ["Shipped"]:
        return "Complete"
    if minutes < 0:
        return "OVERDUE"
    if minutes <= 60:
        return "Due < 1h"
    if minutes <= 180:
        return "Due < 3h"
    return "On track"

orders["Urgency"] = orders.apply(urgency, axis=1)
orders["Ship By Display"] = orders["Ship By"].dt.strftime("%d %b, %I:%M %p")

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
.main-title {font-size: 2rem; font-weight: 750; margin-bottom: 0.1rem;}
.subtitle {color: #6b7280; margin-bottom: 1rem;}
.card {padding: 14px 16px; border: 1px solid #e5e7eb; border-radius: 12px; background: white;}
.alert {padding: 10px 14px; border-radius: 9px; margin-bottom: 8px; border: 1px solid #e5e7eb;}
.small {font-size: 0.82rem; color: #6b7280;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar navigation
# -----------------------------
st.sidebar.title("📦 Fulfillment Hub")
st.sidebar.caption("XYZ Operations")
page = st.sidebar.radio("Navigate", ["Dashboard", "Orders", "Inventory", "Exceptions"])
st.sidebar.divider()
st.sidebar.caption("Demo data • 05 Oct 2026 • 10:00 AM")

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="main-title">Fulfillment Hub</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">One clear view of orders, inventory and operational exceptions.</div>', unsafe_allow_html=True)

if page == "Dashboard":
    total = len(orders)
    priority = int((orders["Priority"] == "Priority").sum())
    overdue = int((orders["Urgency"] == "OVERDUE").sum())
    blocked = int((orders["Status"] == "Awaiting Stock").sum())
    ready = int(orders["Status"].isin(["Packed", "Staging"]).sum())

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Orders today", total)
    c2.metric("Priority", priority)
    c3.metric("Overdue", overdue, delta=None)
    c4.metric("Blocked by stock", blocked)
    c5.metric("Ready / staged", ready)

    st.subheader("Needs attention now")
    attention = orders[(orders["Urgency"].isin(["OVERDUE", "Due < 1h"])) | (orders["Status"] == "Awaiting Stock")].copy()
    attention = attention.sort_values(["Urgency", "Priority"], ascending=[True, True])
    if attention.empty:
        st.success("No urgent exceptions.")
    else:
        display = attention[["Order ID", "Product", "Variant", "Priority", "Status", "Urgency", "Ship By Display"]]
        st.dataframe(display, use_container_width=True, hide_index=True)

    left, right = st.columns([1.2, 1])
    with left:
        st.subheader("Order flow")
        flow = orders["Status"].value_counts().reindex(["Processing", "Picking", "Awaiting Stock", "Packed", "Staging", "Shipped"], fill_value=0)
        st.bar_chart(flow)
    with right:
        st.subheader("Priority order view")
        p = orders[orders["Priority"] == "Priority"][["Order ID", "Status", "Urgency", "Ship By Display"]]
        st.dataframe(p, use_container_width=True, hide_index=True)

    st.info("Design principle: the dashboard surfaces exceptions first so the small office team can act before a shipment is missed.")

elif page == "Orders":
    st.subheader("Order queue")
    f1, f2, f3 = st.columns(3)
    with f1:
        status_filter = st.multiselect("Status", sorted(orders["Status"].unique()), default=[])
    with f2:
        priority_filter = st.multiselect("Priority", ["Priority", "Regular"], default=[])
    with f3:
        search = st.text_input("Search order / product", placeholder="ORD-1001 or earbuds")

    filtered = orders.copy()
    if status_filter:
        filtered = filtered[filtered["Status"].isin(status_filter)]
    if priority_filter:
        filtered = filtered[filtered["Priority"].isin(priority_filter)]
    if search:
        mask = filtered.astype(str).apply(lambda col: col.str.contains(search, case=False, na=False)).any(axis=1)
        filtered = filtered[mask]

    filtered = filtered.sort_values(by=["Priority", "Ship By"], key=lambda s: s.map({"Priority": 0, "Regular": 1}) if s.name == "Priority" else s)
    st.dataframe(filtered[["Order ID", "Customer", "Product", "Variant", "Priority", "Status", "Urgency", "Ship By Display", "Courier"]], use_container_width=True, hide_index=True)

    st.subheader("How an order moves")
    st.caption("Received → Processing → Picking → Packing → Staging → Shipping")

elif page == "Inventory":
    st.subheader("Inventory control")
    st.caption("Main warehouse is the shipping location. Secondary stock must be transferred before it can be picked.")

    a, b, c = st.columns(3)
    a.metric("SKUs tracked", len(inventory))
    b.metric("Transfer needed", int((inventory["Inventory Flag"] == "Transfer needed").sum()))
    c.metric("Low stock", int((inventory["Inventory Flag"] == "Low stock").sum()))

    st.dataframe(inventory, use_container_width=True, hide_index=True)

    st.subheader("Suggested stock actions")
    actions = inventory[inventory["Inventory Flag"] != "OK"].copy()
    if not actions.empty:
        for _, r in actions.iterrows():
            if r["Inventory Flag"] == "Transfer needed":
                st.warning(f"**{r['Product']} — {r['Variant']}**: move {min(r['Second WH'], max(1, r['Today Demand'] - r['Main WH']))} unit(s) from Secondary WH to Main WH before picking.")
            else:
                st.info(f"**{r['Product']} — {r['Variant']}**: main stock is {r['Main WH']} vs reorder point {r['Reorder Point']}. Monitor/replenish.")

elif page == "Exceptions":
    st.subheader("Exception queue")
    st.caption("A visible exception queue replaces informal reminders and makes ownership easier.")

    exceptions = []
    for _, r in orders.iterrows():
        if r["Urgency"] == "OVERDUE":
            exceptions.append([r["Order ID"], "Shipment deadline missed", "High", "Move to top of queue", r["Status"]])
        elif r["Urgency"] == "Due < 1h":
            exceptions.append([r["Order ID"], "Priority/deadline risk", "High", "Process immediately", r["Status"]])
        if r["Status"] == "Awaiting Stock":
            exceptions.append([r["Order ID"], "Stock unavailable in Main WH", "High", "Check secondary stock / transfer", r["Status"]])
        if r["Status"] == "Staging" and r["Urgency"] in ["OVERDUE", "Due < 1h"]:
            exceptions.append([r["Order ID"], "Courier pickup risk", "High", "Confirm pickup", r["Status"]])

    ex = pd.DataFrame(exceptions, columns=["Order ID", "Issue", "Severity", "Recommended Action", "Current Status"])
    if ex.empty:
        st.success("No active exceptions.")
    else:
        st.dataframe(ex, use_container_width=True, hide_index=True)

    st.subheader("Operational rulebook")
    st.markdown("""
    - **Priority + due within 1 hour:** process before regular orders.
    - **Main WH stock = 0 + Secondary WH stock > 0:** create a transfer action.
    - **Awaiting Stock:** do not allow the order to proceed to packing until stock is confirmed.
    - **Packed/Staging + pickup risk:** confirm courier pickup before the deadline.
    - **Every exception is visible in one queue:** reduces reliance on memory or informal messages.
    """)

st.divider()
st.caption("Fulfillment Hub — prototype built for the XYZ take-home project. Sample data is fictional.")
