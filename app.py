# app.py

import streamlit as st

# --- Page Configuration
st.set_page_config(page_title="Smart Balance Viewer", page_icon="💰")

# --- Title and Description
st.title("💳 Smart Balance Viewer")
st.markdown("Check balances across your PAN-linked bank accounts (demo version)")

# --- User Inputs
pan = st.text_input("Enter your PAN number")
phone = st.text_input("Enter your Phone number")

# --- Button
if st.button("Fetch Balances"):
    if not pan.strip() or not phone.strip():
        st.error("❌ Please enter both PAN and phone number.")
    else:
        st.success("✅ Mock bank accounts found for this PAN!")

        # --- Simulated Mock Data (Replace with real API later)
        mock_balances = {
            "SBI": 120000,
            "HDFC": 73500,
            "ICICI": 26400
        }

        # --- Display Balances
        st.markdown("### 🏦 Account Balances")
        for bank, balance in mock_balances.items():
            st.write(f"**{bank}**: ₹{balance:,.2f}")

        total = sum(mock_balances.values())
        st.markdown(f"---\n### 🧾 **Total Balance: ₹{total:,.2f}**")


