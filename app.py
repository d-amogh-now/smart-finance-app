import streamlit as st
import streamlit_authenticator as stauth

# --- User credentials (dummy login)
credentials = {
    "usernames": {
        "amogh@email.com": {
            "name": "Amogh",
            "password": stauth.Hasher(["123456"]).generate()[0]
        }
    }
}

# --- Authenticator config
authenticator = stauth.Authenticate(
    credentials,
    "smart_balance_app", "abcdef", cookie_expiry_days=1
)

# --- Login UI
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Logged in as {name}")

    st.title("💳 Smart Balance Viewer")
    st.markdown("Check balances across your PAN-linked bank accounts")

    pan = st.text_input("Enter your PAN number")
    phone = st.text_input("Enter your Phone number")

    if st.button("Fetch Balances"):
        if not pan.strip() or not phone.strip():
            st.error("❌ Please enter both PAN and phone number.")
        else:
            st.success("✅ Mock bank accounts found for this PAN!")

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

elif authentication_status is False:
    st.error("Incorrect email or password ❌")
elif authentication_status is None:
    st.warning("Please enter your credentials to log in.")
