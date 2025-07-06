# app.py

import streamlit as st

# --- Page setup
st.set_page_config(page_title="Smart Balance Viewer", page_icon="💰")

# --- Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Function to display login screen
def show_login():
    st.title("🔐 Login to Smart Balance App")
    st.markdown("Please enter your credentials to continue")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email == "amogh@email.com" and password == "123456":
            st.session_state.logged_in = True
            st.success("Login successful ✅")
        else:
            st.error("Incorrect email or password ❌")

# --- Function to show balance page
def show_balance_page():
    st.title("💳 Smart Balance Viewer")
    st.markdown("Check balances across your PAN-linked bank accounts")

    pan = st.text_input("Enter your PAN number")
    phone = st.text_input("Enter your Phone number")

    if st.button("Fetch Balances"):
        if not pan.strip() or not phone.strip():
            st.error("❌ Please enter both PAN and phone number.")
        else:
            st.success("✅ Mock bank accounts found for this PAN!")

            # --- Simulated balances
            mock_balances = {
                "SBI": 120000,
                "HDFC": 73500,
                "ICICI": 26400
            }

            st.markdown("### 🏦 Account Balances")
            for bank, balance in mock_balances.items():
                st.write(f"**{bank}**: ₹{balance:,.2f}")

            total = sum(mock_balances.values())
            st.markdown(f"---\n### 🧾 **Total Balance: ₹{total:,.2f}**")

# --- App logic
if st.session_state.logged_in:
    show_balance_page()
else:
    show_login()
