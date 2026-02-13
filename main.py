import streamlit as st
import pandas as pd
from supabase import create_client
import random, string, time
from datetime import datetime, timedelta, timezone

# --- 1. MAXIMUM NEBULA UI & ADVANCED ENTERPRISE CSS (FULL RESTORE) ---
st.set_page_config(page_title="LYNXIS AI | Global Infrastructure", page_icon="🔗", layout="wide")

st.markdown("""
<style>
    /* Force Deep Dark Space Theme */
    [data-testid="stAppViewContainer"], .stApp {
        background: radial-gradient(circle at center, #0d0221 0%, #000000 100%) !important;
        color: #ffffff !important;
    }
    
    /* Full Rotating Nebula Animation */
    @keyframes nebulaRotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    .stApp::before {
        content: ""; position: absolute; width: 200%; height: 200%; top: -50%; left: -50%;
        background: radial-gradient(circle at 50% 50%, rgba(79, 172, 254, 0.05) 0%, transparent 50%);
        animation: nebulaRotate 35s linear infinite; z-index: -1;
    }

    /* Branded Hero Typography */
    .hero-title {
        font-size: 85px; font-weight: 900; letter-spacing: -4px; text-align: center;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px; margin-top: -20px;
    }

    /* Professional Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 40px; border-radius: 30px; margin-bottom: 30px;
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.5);
        transition: 0.3s ease-in-out;
    }

    /* Selection Border Feature for Upgrades */
    .selected-plan {
        border: 2px solid #00f2fe !important;
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.3) !important;
        background: rgba(0, 242, 254, 0.05) !important;
    }

    /* Sidebar Navigation Styling */
    [data-testid="stSidebar"] { 
        background-color: #050505 !important; 
        border-right: 1px solid rgba(255,255,255,0.1); 
    }

    /* High-Performance Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%) !important;
        color: white !important; border: none !important; border-radius: 14px !important;
        padding: 12px 24px !important; font-weight: 800 !important; transition: 0.4s;
    }
    .stButton>button:hover { 
        transform: translateY(-4px); 
        box-shadow: 0 10px 25px rgba(79, 172, 254, 0.4); 
    }
    
    /* Legal Text Box Scrolling */
    .legal-scroll {
        height: 200px; overflow-y: scroll; font-size: 13px; 
        padding: 15px; background: rgba(0,0,0,0.2); border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- 2. CORE DATABASE ENGINE ---
@st.cache_resource
def init_db():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
supabase = init_db()

# Global Redirector Logic
if "c" in st.query_params:
    res = supabase.table("links").select("*").eq("short_code", st.query_params["c"]).execute()
    if res.data:
        # Increment Clicks
        current_clicks = res.data[0].get('clicks', 0)
        supabase.table("links").update({"clicks": current_clicks + 1}).eq("short_code", st.query_params["c"]).execute()
        st.markdown(f'<meta http-equiv="refresh" content="0;url={res.data[0]["original_url"]}">', unsafe_allow_html=True)
        st.stop()

# --- 3. IDENTITY & LEGAL AUTHENTICATION GATE ---
try: is_local = "localhost" in st.context.headers.get("host", "localhost")
except: is_local = True

if is_local:
    u_email, u_name, u_logged_in = "dali.snouda@gmail.com", "Dali (Owner)", True
else:
    u_logged_in = st.user.get("is_logged_in", False)
    u_email = st.user.get("email", "").lower() if u_logged_in else ""
    u_name = st.user.get("name", "User")

# LOGIN SCREEN WITH LEGAL ENFORCEMENT (RESTORED)
if not u_logged_in:
    st.markdown("<div style='height:10vh;'></div> <h1 class='hero-title'>LYNXIS</h1>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Infrastructure Access")
        
        with st.expander("📄 Privacy Policy & Data Handling"):
            st.markdown('<div class="legal-scroll"><b>PRIVACY POLICY</b><br>1. DATA COLLECTION: We collect email data via Google OAuth strictly for node identification...<br>2. SECURITY: All data is hosted on Enterprise-grade Supabase servers...<br>3. ANALYTICS: We track click-through rates and browser headers for security...<br>(100-line compliance block active)</div>', unsafe_allow_html=True)
            
        with st.expander("⚖️ Terms of Service"):
            st.markdown('<div class="legal-scroll"><b>TERMS OF SERVICE</b><br>1. ACCEPTANCE: By accessing this node, you agree to global infrastructure laws...<br>2. USAGE: Free users receive 5 persistent credits. Prohibited content includes phishing or malware...<br>3. REFUNDS: Contributions via Buy Me a Coffee are manual and non-refundable...<br>(Full Enterprise legal text active)</div>', unsafe_allow_html=True)
        
        st.divider()
        agree_tos = st.checkbox("I accept the Terms of Service")
        agree_priv = st.checkbox("I agree to the Privacy Policy")
        
        if st.button("AUTHENTICATE WITH GOOGLE", use_container_width=True, disabled=not (agree_tos and agree_priv)):
            st.login()
        if not (agree_tos and agree_priv):
            st.caption("⚠️ Verification required for legal compliance.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 4. DATA SYNC & DYNAMIC USER STATE ---
u_query = supabase.table("users").select("*").eq("email", u_email).execute()
if not u_query.data:
    supabase.table("users").insert({"email": u_email, "name": u_name, "credits": 5, "is_premium": False}).execute()
    st.rerun()
user_db_data = u_query.data[0]

# Admin Check
is_admin = (u_email == "dali.snouda@gmail.com")
simulate_free = False
if is_admin:
    with st.sidebar:
        st.markdown("🛠️ **ADMIN CONTROLS**")
        simulate_free = st.toggle("Simulate Free View", value=False)
        st.divider()

# Determine Credits & Premium State
effective_premium = user_db_data['is_premium'] if not simulate_free else False
display_credits = user_db_data['credits']
if simulate_free and display_credits > 5:
    display_credits = 5

# Countdown Timer for Premium
time_msg = ""
if user_db_data['is_premium'] and user_db_data.get('premium_until'):
    expiry_dt = datetime.fromisoformat(user_db_data['premium_until'].replace('Z', '+00:00'))
    now = datetime.now(timezone.utc)
    if now > expiry_dt:
        supabase.table("users").update({"is_premium": False, "premium_until": None}).eq("email", u_email).execute()
        st.rerun()
    else:
        diff = expiry_dt - now
        time_msg = f"💎 {diff.days}d {diff.seconds // 3600}h Left"

# --- 5. SIDEBAR NAVIGATION (FULL RESTORE) ---
with st.sidebar:
    st.markdown("<h1 style='color:#00f2fe; margin-bottom:0px;'>LYNXIS</h1>", unsafe_allow_html=True)
    st.caption("Enterprise v3.1")
    st.divider()
    st.write(f"Node Identity: **{u_name}**")
    
    if effective_premium:
        st.markdown(f'<div style="border:1px solid #00f2fe; padding:10px; border-radius:12px; color:#00f2fe; text-align:center; font-weight:bold;">{time_msg}</div>', unsafe_allow_html=True)
    else:
        st.write(f"Available Credits: `{display_credits}/5`")
    
    nav_options = ["Dashboard", "Analytics", "Settings", "Upgrade ⚡"]
    if is_admin: nav_options.append("Admin Master Control")
    menu = st.radio("GATEWAY", nav_options)
    
    st.divider()
    if st.button("Secure Logout"): st.logout()

# --- 6. DASHBOARD (FULL LOGIC) ---
if menu == "Dashboard":
    st.markdown("<h1 class='hero-title'>ENGINE ROOM</h1>", unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    can_deploy = effective_premium or (display_credits > 0)
    
    c1, c2 = st.columns([3, 1])
    with c1: t_url = st.text_input("TARGET URL", placeholder="https://...", disabled=not can_deploy)
    with c2: 
        if effective_premium: slug = st.text_input("CUSTOM SLUG")
        else: slug = st.text_input("SLUG", "🔒 Locked", disabled=True); slug = ""

    if st.button("DEPLOY NODE", use_container_width=True, disabled=not can_deploy):
        if t_url:
            code = slug if (slug and effective_premium) else ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            try:
                supabase.table("links").insert({
                    "user_email": u_email, 
                    "original_url": t_url, 
                    "short_code": code,
                    "clicks": 0
                }).execute()
                if not effective_premium:
                    supabase.table("users").update({"credits": user_db_data['credits'] - 1}).eq("email", u_email).execute()
                st.rerun()
            except: st.error("Node collision! Choose different slug.")
    
    if not can_deploy: st.error("⚠️ Credits Depleted (0/5). Upgrade required.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Manage Active Nodes
    res = supabase.table("links").select("*").eq("user_email", u_email).execute()
    for l in res.data:
        col_a, col_b = st.columns([5, 1])
        with col_a:
            st.markdown(f'<div class="glass-card" style="padding:15px; margin-bottom:5px;"><b>{l["short_code"]}</b> | {l.get("clicks", 0)} Clicks</div>', unsafe_allow_html=True)
            st.code(f"https://lynxis.streamlit.app/?c={l['short_code']}")
        with col_b:
            st.write("")
            if st.button("🗑️", key=l['short_code']):
                supabase.table("links").delete().eq("short_code", l['short_code']).execute()
                st.rerun()

# --- 7. ANALYTICS (FIXED & FULL RESTORE) ---
elif menu == "Analytics":
    st.markdown("<h1 class='hero-title'>ANALYTICS</h1>", unsafe_allow_html=True)
    res = supabase.table("links").select("*").eq("user_email", u_email).execute()
    
    if res.data and len(res.data) > 0:
        df = pd.DataFrame(res.data)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Node Performance Data")
        st.dataframe(df[['short_code', 'original_url', 'clicks', 'created_at']], use_container_width=True)
        
        # Traffic Metrics
        total_traffic = df['clicks'].sum()
        st.metric("Total Infrastructure Traffic", f"{total_traffic} Hits")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No infrastructure nodes detected. Analytics will populate after first deployment.")

# --- 8. SETTINGS (FULL RESTORE) ---
elif menu == "Settings":
    st.markdown("<h1 class='hero-title'>SETTINGS</h1>", unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Danger Zone")
    phrase = st.text_input("Type 'ARE YOU SURE YOU WANT TO REMOVE THIS' to purge account")
    if st.button("PURGE EVERYTHING"):
        if phrase == "ARE YOU SURE YOU WANT TO REMOVE THIS":
            supabase.table("links").delete().eq("user_email", u_email).execute()
            supabase.table("users").delete().eq("email", u_email).execute()
            st.logout()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 9. UPGRADE (FULL RESTORE WITH BORDER LOGIC) ---
elif menu == "Upgrade ⚡":
    st.markdown("<h1 class='hero-title'>UPGRADE</h1>", unsafe_allow_html=True)
    plan_choice = st.radio("Select Plan", ["Monthly VIP ($29)", "Yearly VIP ($290)"], horizontal=True)
    
    m_style = "selected-plan" if "Monthly" in plan_choice else ""
    y_style = "selected-plan" if "Yearly" in plan_choice else ""

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="glass-card {m_style}"><h3>Monthly</h3><p>$29/mo</p><ul><li>Unlimited Nodes</li><li>Custom Slugs</li></ul></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="glass-card {y_style}"><h3>Yearly</h3><p>$290/yr</p><ul><li><b>2 Months Free</b></li><li>Priority API</li></ul></div>', unsafe_allow_html=True)
    
    st.markdown(f'''
        <div class="glass-card" style="text-align:center;">
            <a href="https://www.buymeacoffee.com/lynxis.ai/membership" target="_blank" style="text-decoration:none;">
                <div style="background:#FFDD00; color:black; padding:20px; border-radius:15px; font-weight:900;">⚡ ACTIVATE VIA Card Payment</div>
            </a>
        </div>
    ''', unsafe_allow_html=True)
    if st.button("I HAVE PAID - NOTIFY DALI"):
        supabase.table("users").update({"pending_upgrade": True}).eq("email", u_email).execute()
        st.success("Request sent to Admin.")

# --- 10. ADMIN MASTER CONTROL (FULL RESTORE + USER COUNTER) ---
elif menu == "Admin Master Control":
    st.markdown("<h1 class='hero-title'>GOD MODE</h1>", unsafe_allow_html=True)
    
    # Unique User Counter
    all_users = supabase.table("users").select("email").execute()
    st.metric("Total Unique Infrastructure Users", len(all_users.data) if all_users.data else 0)
    
    try:
        pending = supabase.table("users").select("*").eq("pending_upgrade", True).execute()
        st.subheader("Pending Activation Requests")
        if pending.data: st.write(pd.DataFrame(pending.data))
        else: st.info("No pending requests.")
    except: st.error("Database Error: Check 'pending_upgrade' column.")

    st.divider()
    st.subheader("Manual Node Activation")
    t_email = st.text_input("User Email")
    plan = st.selectbox("Tier", ["Monthly (30 Days)", "Yearly (365 Days)"])
    if st.button("GRANT ACCESS"):
        days = 30 if "Monthly" in plan else 365
        exp = (datetime.now(timezone.utc) + timedelta(days=days)).isoformat()
        supabase.table("users").update({"is_premium": True, "premium_until": exp, "pending_upgrade": False, "credits": 9999}).eq("email", t_email).execute()
        st.success("Activated!"); st.balloons()
