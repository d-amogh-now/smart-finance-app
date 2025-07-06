import streamlit as st
import streamlit.components.v1 as components

# --- App Config
st.set_page_config(page_title="Smart Finance App", page_icon="💰")

st.title("💳 Smart Balance Viewer")
st.markdown("Please sign in with your Google account to continue")

# --- Firebase Config (from your Firebase setup)
firebase_config = {
  "apiKey": "AIzaSyAYFzJ404quHTLGfr1zNU-Xt5bH8sFspww",
  "authDomain": "smart-finance-app-b64dc.firebaseapp.com",
  "projectId": "smart-finance-app-b64dc",
  "storageBucket": "smart-finance-app-b64dc.firebasestorage.app",
  "messagingSenderId": "420160178429",
  "appId": "1:420160178429:web:5160818c5a33f9e05fd694"
}

# --- HTML + JS for Firebase Google Login
login_component = f"""
<script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-auth-compat.js"></script>

<div id="login-box">
  <button onclick="signInWithGoogle()">Sign in with Google</button>
</div>
<script>
  const firebaseConfig = {firebase_config};
  firebase.initializeApp(firebaseConfig);

  function signInWithGoogle() {{
    const provider = new firebase.auth.GoogleAuthProvider();
    firebase.auth().signInWithPopup(provider).then(result => {{
      const user = result.user;
      const loginData = {{
        email: user.email,
        name: user.displayName
      }};
      window.parent.postMessage({{ type: 'LOGIN_SUCCESS', loginData }}, '*');
    }}).catch(console.error);
  }}
</script>
"""

# --- Placeholder for user login status
user_email = st.session_state.get("user_email", None)

# --- Streamlit JS bridge to listen to login event
components.html(
    login_component,
    height=200
)

# --- Capture login from browser → Streamlit session state
st.markdown("""
<script>
window.addEventListener("message", (event) => {
  if (event.data.type === "LOGIN_SUCCESS") {
    const loginData = event.data.loginData;
    const streamlitEvent = new CustomEvent("streamlit:setComponentValue", {{
      detail: {{ key: "user_email", value: loginData.email }}
    }});
    window.dispatchEvent(streamlitEvent);
  }
});
</script>
""", unsafe_allow_html=True)

# --- If user is logged in, show the dashboard
if user_email:
    st.success(f"Welcome back, {user_email} 🎉")
    st.subheader("Your Mock Bank Balances:")

    mock_balances = {
        "SBI": 120000,
        "HDFC": 73500,
        "ICICI": 26400
    }

    for bank, balance in mock_balances.items():
        st.write(f"**{bank}**: ₹{balance:,.2f}")

    st.markdown(f"---\n### 🧾 Total Balance: ₹{sum(mock_balances.values()):,.2f}")
