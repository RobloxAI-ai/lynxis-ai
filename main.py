import streamlit as st
import pandas as pd
from supabase import create_client
import random, string, time
from datetime import datetime, timedelta, timezone

# --- 1. MAXIMUM NEBULA UI & ADVANCED ENTERPRISE CSS ---
st.set_page_config(page_title="LYNXIS AI | Global Infrastructure", page_icon="🔗", layout="wide")

st.markdown("""
<style>
    [data-testid="stAppViewContainer"], .stApp {
        background: radial-gradient(circle at center, #0d0221 0%, #000000 100%) !important;
        color: #ffffff !important;
    }
    @keyframes nebulaRotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    .stApp::before {
        content: ""; position: absolute; width: 200%; height: 200%; top: -50%; left: -50%;
        background: radial-gradient(circle at 50% 50%, rgba(79, 172, 254, 0.05) 0%, transparent 50%);
        animation: nebulaRotate 35s linear infinite; z-index: -1;
    }
    .hero-title {
        font-size: 85px; font-weight: 900; letter-spacing: -4px; text-align: center;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px; margin-top: -20px;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 40px; border-radius: 30px; margin-bottom: 30px;
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.5);
    }
    .selected-plan {
        border: 2px solid #00f2fe !important;
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.3) !important;
        background: rgba(0, 242, 254, 0.05) !important;
    }
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid rgba(255,255,255,0.1); }
    .stButton>button {
        background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%) !important;
        color: white !important; border: none !important; border-radius: 14px !important;
        padding: 12px 24px !important; font-weight: 800 !important;
    }
    .legal-scroll {
        height: 180px; overflow-y: scroll; font-size: 13px; padding: 15px; 
        background: rgba(0,0,0,0.3); border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- 2. CORE DATABASE ENGINE ---
@st.cache_resource
def init_db():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
supabase = init_db()

# --- 3. REDIRECT LOGIC (PORTAL VERSION) ---
query_params = st.query_params
if "c" in query_params:
    target_slug = query_params["c"]
    response = supabase.table("links").select("original_url, clicks").eq("short_code", target_slug).execute()
    
    if response.data:
        node = response.data[0]
        target_url = node["original_url"]
        if not target_url.startswith(("http://", "https://")):
            target_url = "https://" + target_url
            
        # Update Click Counter
        new_clicks = (node.get("clicks") or 0) + 1
        supabase.table("links").update({"clicks": new_clicks}).eq("short_code", target_slug).execute()
        
        # --- THE PORTAL UI (Bypasses "Refused to Connect") ---
        st.markdown(f"""
            <div style="text-align:center; padding:50px; background:rgba(255,255,255,0.05); border-radius:20px; border:1px solid #4facfe;">
                <h1 style="color:#00f2fe; font-size:40px;">NODE READY</h1>
                <p style="color:#ffffff; font-size:18px;">Security protocols cleared. Open the gateway below:</p>
                <br>
                <a href="{target_url}" target="_blank" style="
                    background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
                    color: white;
                    padding: 15px 40px;
                    text-decoration: none;
                    border-radius: 12px;
                    font-weight: bold;
                    font-size: 22px;
                    box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4);
                ">🚀 ENTER PORTAL</a>
                <br><br>
                <p style="color:gray; font-size:12px;">Link: {target_url}</p>
            </div>
        """, unsafe_allow_html=True)
        st.stop()
        
# --- 4. UNIVERSAL IDENTITY GATEKEEPER ---
u_logged_in = False
u_email = ""
u_name = "User"

# Try every possible version of the Streamlit User command
try:
    if hasattr(st, "user") and st.user.get("is_logged_in"):
        u_logged_in = True
        u_email = st.user.get("email", "").lower()
        u_name = st.user.get("name", "User")
    elif hasattr(st, "experimental_user") and st.experimental_user.get("is_logged_in"):
        u_logged_in = True
        u_email = st.experimental_user.get("email", "").lower()
        u_name = st.experimental_user.get("name", "User")
except:
    pass

# Force login for the owner (You) if testing locally
if "localhost" in str(st.context.headers.get("host", "")):
    u_email, u_name, u_logged_in = "dali.snouda@gmail.com", "Dali (Owner)", True

if not u_logged_in:
    st.markdown("<div style='height:10vh;'></div><h1 class='hero-title'>LYNXIS</h1>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Infrastructure Verification")
        agree = st.checkbox("I accept the LYNXIS Protocols")
        if st.button("AUTHENTICATE WITH GOOGLE", use_container_width=True, disabled=not agree):
            st.login()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 5. DATA SYNC & USER STATE ---
u_query = supabase.table("users").select("*").eq("email", u_email).execute()
if not u_query.data:
    supabase.table("users").insert({"email": u_email, "name": u_name, "credits": 5, "is_premium": False}).execute()
    st.rerun()
user_db_data = u_query.data[0]
is_admin = (u_email == "dali.snouda@gmail.com")

# --- 6. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='color:#00f2fe; margin-bottom:0px;'>LYNXIS</h1>", unsafe_allow_html=True)
    st.divider()
    st.write(f"Identity: **{u_name}**")
    st.write(f"Credits: `{user_db_data['credits']}/5`" if not user_db_data['is_premium'] else "💎 VIP Access")
    nav = ["Dashboard", "Analytics", "Settings", "Upgrade ⚡"]
    if is_admin: nav.append("Admin Master Control")
    menu = st.radio("GATEWAY", nav)
    if st.button("Secure Logout"): st.logout()

# --- 7. DASHBOARD ---
if menu == "Dashboard":
    st.markdown("<h1 class='hero-title'>ENGINE ROOM</h1>", unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    can_deploy = user_db_data['is_premium'] or (user_db_data['credits'] > 0)
    c1, c2 = st.columns([3, 1])
    with c1: t_url = st.text_input("TARGET URL", placeholder="https://...")
    with c2: 
        if user_db_data['is_premium']: slug = st.text_input("CUSTOM SLUG")
        else: st.text_input("SLUG", "🔒 VIP ONLY", disabled=True); slug = ""

    if st.button("DEPLOY NODE", use_container_width=True, disabled=not (can_deploy and t_url)):
        final_slug = slug if (slug and user_db_data['is_premium']) else ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        # Collision Check
        check = supabase.table("links").select("short_code").eq("short_code", final_slug).execute()
        if check.data:
            st.error("Node collision! Slug taken.")
        else:
            supabase.table("links").insert({"user_email": u_email, "original_url": t_url, "short_code": final_slug, "clicks": 0}).execute()
            if not user_db_data['is_premium']:
                supabase.table("users").update({"credits": user_db_data['credits'] - 1}).eq("email", u_email).execute()
            st.success(f"Node Live: {final_slug}")
            time.sleep(1)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Manage Active Nodes
    res = supabase.table("links").select("*").eq("user_email", u_email).execute()
    for l in res.data:
        col_a, col_b = st.columns([5, 1])
        with col_a:
            st.code(f"https://lynxis-ai.streamlit.app/?c={l['short_code']}")
        with col_b:
            if st.button("🗑️", key=l['short_code']):
                supabase.table("links").delete().eq("short_code", l['short_code']).execute()
                st.rerun()

# --- 8. ANALYTICS ---
elif menu == "Analytics":
    st.markdown("<h1 class='hero-title'>ANALYTICS</h1>", unsafe_allow_html=True)
    res = supabase.table("links").select("*").eq("user_email", u_email).execute()
    if res.data:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        df = pd.DataFrame(res.data)
        st.dataframe(df[['short_code', 'original_url', 'clicks']], use_container_width=True)
        st.metric("Total Hits", df['clicks'].sum())
        st.markdown('</div>', unsafe_allow_html=True)

# --- 9. ADMIN MASTER CONTROL ---
elif menu == "Admin Master Control" and is_admin:
    st.markdown("<h1 class='hero-title'>GOD MODE</h1>", unsafe_allow_html=True)
    pending = supabase.table("users").select("*").eq("pending_upgrade", True).execute()
    st.subheader("Pending VIP Requests")
    if pending.data: st.write(pd.DataFrame(pending.data))
    t_email = st.text_input("User Email")
    if st.button("ACTIVATE VIP"):
        supabase.table("users").update({"is_premium": True, "credits": 9999, "pending_upgrade": False}).eq("email", t_email).execute()
        st.success("User Elevated to VIP.")
# --- RESTORE: SETTINGS & UPGRADE ---
elif menu == "Settings":
    st.markdown("<h1 class='hero-title'>SETTINGS</h1>", unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write(f"**Connected Email:** {u_email}")
    st.write(f"**Account Status:** {'💎 VIP' if user_db_data['is_premium'] else 'Standard'}")
    if st.button("Request Data Wipe"):
        st.warning("Contact Dali to delete infrastructure nodes.")
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "Upgrade ⚡":
    st.markdown("<h1 class='hero-title'>EVOLVE</h1>", unsafe_allow_html=True)
    
    # --- DUAL TOGGLE ---
    plan_type = st.radio("SELECT BILLING CYCLE", ["Monthly", "Yearly (Save 20%)"], horizontal=True)
    price = "29" if "Monthly" in plan_type else "279"
    period = "mo" if "Monthly" in plan_type else "yr"

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'''<div class="glass-card">
            <h3 style="color:gray;">STANDARD</h3>
            <h1 style="margin:0;">$0</h1>
            <ul style="font-size:14px; margin-top:10px;"><li>5 Active Nodes</li><li>Standard Slugs</li></ul>
        </div>''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''<div class="glass-card" style="border-color:#00f2fe;">
            <h3 style="color:#00f2fe;">PREMIUM</h3>
            <h1 style="margin:0;">${price}<small style="font-size:15px;">/{period}</small></h1>
            <ul style="font-size:14px; margin-top:10px;"><li>Unlimited Nodes</li><li>Custom Slugs</li></ul>
        </div>''', unsafe_allow_html=True)
    
    st.write("---")

    # --- THE FORCE-VISIBLE BUTTON ---
    # We are putting this OUTSIDE of any 'if' statements so it has to show up.
    st.markdown("""
        <style>
            .stLinkButton > a {
                background: linear-gradient(45deg, #FFDD00, #FBB03B) !important;
                color: black !important;
                font-weight: 900 !important;
                font-size: 20px !important;
                border: none !important;
                padding: 20px !important;
                box-shadow: 0 0 20px rgba(255, 221, 0, 0.4) !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.link_button(
        "💳 PAY VIA CARD PAYMENT", 
        "https://www.buymeacoffee.com/lynxis.ai/membership", 
        use_container_width=True
    )
    
    st.caption("Secure payment processed via Buy Me a Coffee Gateway")
# --- 7. LEGAL ENGINE (REAL POLICIES) ---
# Create a simple "Page" detector for the legal documents
if "page" not in st.session_state:
    st.session_state.page = "main"

# Function to show the policies
def show_legal(type):
    st.markdown(f"<h1 class='hero-title'>{type.upper()}</h1>", unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if type == "Terms of Service":
        st.write("""
        **1. Acceptance of Terms:** By using LYNXIS, you agree to these protocols.
        **2. Prohibited Use:** You may not use LYNXIS for phishing, malware, or illegal content. We reserve the right to terminate any Node that violates security.
        **3. Liability:** LYNXIS is a redirection tool. We are not responsible for the destination content of any user-generated link.
        **4. Termination:** VIP status is a service agreement and can be revoked for TOS violations.
        """)
    else:
        st.write("""
        **1. Data Collection:** We collect your Google Email and Name for authentication only.
        **2. Link Tracking:** We log click counts to provide analytics to the Node creator.
        **3. Payments:** All financial data is handled by Buy Me a Coffee/Stripe. LYNXIS never sees your card details.
        **4. Data Deletion:** You can request a full data wipe via the Settings panel at any time.
        """)
    if st.button("RETURN TO INTERFACE"):
        st.session_state.page = "main"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop() # Stops the rest of the app from showing behind the legal text

# Logic to trigger the legal pages
query_params = st.query_params
if query_params.get("view") == "terms":
    show_legal("Terms of Service")
if query_params.get("view") == "privacy":
    show_legal("Privacy Policy")

# --- THE FOOTER ---
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 20px; color: gray; font-size: 12px; opacity: 0.7;">
    © 2026 LYNXIS INFRASTRUCTURE | 
    <a href="?view=terms" target="_self" style="color:#4facfe;">Terms of Service</a> | 
    <a href="?view=privacy" target="_self" style="color:#4facfe;">Privacy Policy</a> | 
    <a href="mailto:dali.snouda@gmail.com" style="color:#4facfe;">Contact Support</a>
</div>
""", unsafe_allow_html=True)
