import streamlit as st
import streamlit.components.v1 as components
import json

# --- App config
st.set_page_config(page_title="Smart Finance App", page_icon="💰")

st.title("💳 Smart Balance Viewer")
st.markdown("Please sign in with your Google account to continue")

# --- Firebase config (from your Firebase console)
firebase_config = {
  "apiKey": "AIzaSyAYFzJ404quHTLGfr1zNU-Xt5bH8sFspww",
  "authDomain": "smart-finance-app-b64dc.firebaseapp.com",
  "projectId": "smart-finance-app-b64dc",
  "storageBucket": "smart-finance-app-b64dc.firebasestorage.app",
  "messagingSenderId": "420160178429",
  "appId": "1:420160178429:web:5160818c5a33f9e05fd694"
}

# --- HTML + JS for Google login using redirect (outside iframe)
login_component = f"""
<script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-auth-compat.js"></script>

<div id="login-box">
  <button onclick="signInWithGoogle()">Sign in with Google</button>
</div>

<script>
  const firebaseConfig = {json.dumps(firebase_config)};
  firebase.initializeApp(firebaseConfig);

  function signInWithGoogle() {{
    const provider = new firebase.auth.GoogleAuthProvider();
    firebase.auth().signInWithRedirect(provider);
  }}

  firebase.auth().getRedirectResult().then((result) => {{
    if (result.user) {{
      const user = result.user;
      const loginData = {{
        email: user.email,
        name: user.displayName
      }};
      window.parent.postMessage({{ type: 'LOGIN_SUCCESS', loginData }}, '*');
    }}
  }}).catch(console.error);
</script>
"""

# --- Display login button
components.html(login_component, height=300)

# --- Session state logic (JS -> Streamlit)
user_data = st.session_state.get("user_data")

# Listen for user data sent from frontend
st.markdown("""
<script>
window.addEventListener("message", (event) => {
  if (event.data.type === "LOGIN_SUCCESS") {
    const user = event.data.loginData;
    const payload = JSON.stringify(user);
    const streamlitEvent = new CustomEvent("streamlit:store", {
      detail: { key: "user_data", value: payload }
    });
    window.dispatchEvent(streamlitEvent);
  }
});
</script>
""", unsafe_allow_html=True)

# --- Show dashboard if logged in
if user_data:
    user_info = json.loads(user_data)
    st.success(f"Welcome, {user_info['name']} ({user_info['email']}) 👋")

    st.subheader("Your Mock Bank Balances")
    mock_balances = {
        "SBI": 120000,
        "HDFC": 73500,
        "ICICI": 26400
    }

    for bank, balance in mock_balances.items():
        st.write(f"**{bank}**: ₹{balance:,.2f}")

    total = sum(mock_balances.values())
    st.markdown(f"---\n### 🧾 Total Balance: ₹{total:,.2f}")
