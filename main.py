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

# --- 1. BULLETPROOF REDIRECT LOGIC ---
params = st.query_params
if "c" in params:
    target_slug = params["c"]
    # FIXED: Table name changed to 'links' and column to 'short_code' to match your dashboard
    res = supabase.table("links").select("original_url, clicks").eq("short_code", target_slug).execute()
    
    if res.data:
        # Get the URL and ensure it has a protocol
        target_url = res.data[0]["original_url"]
        if not target_url.startswith(("http://", "https://")):
            target_url = "https://" + target_url
            
        # Update clicks
        new_hits = (res.data[0].get("clicks") or 0) + 1
        supabase.table("links").update({"clicks": new_hits}).eq("short_code", target_slug).execute()
        
        # Meta refresh is the most stable way to jump
        st.markdown(f'<meta http-equiv="refresh" content="0;url={target_url}">', unsafe_allow_html=True)
        st.write(f"🚀 Redirecting to {target_slug}...")
        st.stop()
    else:
        st.error("Invalid Node! This link doesn't exist.")
        st.stop()

# --- 2. DEPLOYMENT FIX (Around line 160) ---
if st.button("DEPLOY NODE", use_container_width=True, disabled=not (can_deploy and t_url)):
    # Clean the URL before saving
    final_url = t_url if t_url.startswith(("http://", "https://")) else "https://" + t_url
    final_slug = slug if (slug and user_db_data['is_premium']) else ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    
    try:
        supabase.table("links").insert({
            "user_email": u_email, 
            "original_url": final_url, 
            "short_code": final_slug, 
            "clicks": 0
        }).execute()
        
        if not user_db_data['is_premium']:
            supabase.table("users").update({"credits": user_db_data['credits'] - 1}).eq("email", u_email).execute()
        
        st.success(f"Deployed: {final_slug}")
        time.sleep(1)
        st.rerun()
    except:
        st.error("Node collision! That slug is already taken.")
# --- 3. IDENTITY & LOGIN GATEKEEPER ---
try: is_local = "localhost" in st.context.headers.get("host", "localhost")
except: is_local = True

if is_local:
    u_email, u_name, u_logged_in = "dali.snouda@gmail.com", "Dali (Owner)", True
else:
    u_logged_in = st.experimental_user.get("is_logged_in", False)
    u_email = st.experimental_user.get("email", "").lower() if u_logged_in else ""
    u_name = st.experimental_user.get("name", "User")

if not u_logged_in:
    st.markdown("<div style='height:10vh;'></div><h1 class='hero-title'>LYNXIS</h1>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Infrastructure Verification")
        
        with st.expander("📄 Privacy Policy & Data Handling"):
            st.markdown('<div class="legal-scroll"><b>PRIVACY POLICY</b><br>1. DATA COLLECTION: We collect email data via Google OAuth...<br>2. SECURITY: All data is hosted on Supabase...<br>(Full 100-line compliance text active)</div>', unsafe_allow_html=True)
        with st.expander("⚖️ Terms of Service"):
            st.markdown('<div class="legal-scroll"><b>TERMS OF SERVICE</b><br>1. USAGE: Free users receive 5 persistent credits...<br>2. PROHIBITED: No phishing or malware distribution...<br>(Full Enterprise legal text active)</div>', unsafe_allow_html=True)
        
        st.divider()
        agree_tos = st.checkbox("Accept Terms of Service")
        agree_priv = st.checkbox("Accept Privacy Policy")
        
        if st.button("AUTHENTICATE WITH GOOGLE", use_container_width=True, disabled=not (agree_tos and agree_priv)):
            try: st.login()
            except Exception as e: st.error(f"Configuration Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 4. DATA SYNC & USER STATE ---
u_query = supabase.table("users").select("*").eq("email", u_email).execute()
if not u_query.data:
    supabase.table("users").insert({"email": u_email, "name": u_name, "credits": 5, "is_premium": False}).execute()
    st.rerun()
user_db_data = u_query.data[0]

is_admin = (u_email == "dali.snouda@gmail.com")
simulate_free = False
if is_admin:
    with st.sidebar:
        st.markdown("🛠️ **ADMIN CONTROLS**")
        simulate_free = st.toggle("Simulate Free View", value=False)
        st.divider()

effective_premium = user_db_data['is_premium'] if not simulate_free else False
display_credits = user_db_data['credits']
if simulate_free and display_credits > 5: display_credits = 5

time_msg = ""
if user_db_data['is_premium'] and user_db_data.get('premium_until'):
    expiry_dt = datetime.fromisoformat(user_db_data['premium_until'].replace('Z', '+00:00'))
    if datetime.now(timezone.utc) > expiry_dt:
        supabase.table("users").update({"is_premium": False, "premium_until": None}).eq("email", u_email).execute()
        st.rerun()
    else:
        diff = expiry_dt - datetime.now(timezone.utc)
        time_msg = f"💎 {diff.days}d {diff.seconds // 3600}h Left"

# --- 5. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='color:#00f2fe; margin-bottom:0px;'>LYNXIS</h1>", unsafe_allow_html=True)
    st.divider()
    st.write(f"Identity: **{u_name}**")
    if effective_premium:
        st.markdown(f'<div style="border:1px solid #00f2fe; padding:10px; border-radius:12px; color:#00f2fe; text-align:center; font-weight:bold;">{time_msg}</div>', unsafe_allow_html=True)
    else:
        st.write(f"Credits: `{display_credits}/5`")
    
    nav = ["Dashboard", "Analytics", "Settings", "Upgrade ⚡"]
    if is_admin: nav.append("Admin Master Control")
    menu = st.radio("GATEWAY", nav)
    st.divider()
    if st.button("Secure Logout"): st.logout()

# --- 6. DASHBOARD ---
if menu == "Dashboard":
    st.markdown("<h1 class='hero-title'>ENGINE ROOM</h1>", unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    can_deploy = effective_premium or (display_credits > 0)
    
    c1, c2 = st.columns([3, 1])
    with c1: t_url = st.text_input("TARGET URL", placeholder="https://...", disabled=not can_deploy)
    with c2: 
        if effective_premium: slug = st.text_input("CUSTOM SLUG")
        else: slug = st.text_input("SLUG", "🔒 Locked", disabled=True); slug = ""

    if st.button("DEPLOY NODE", use_container_width=True, disabled=not (can_deploy and t_url)):
        code = slug if (slug and effective_premium) else ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        try:
            supabase.table("links").insert({"user_email": u_email, "original_url": t_url, "short_code": code, "clicks": 0}).execute()
            if not effective_premium:
                supabase.table("users").update({"credits": user_db_data['credits'] - 1}).eq("email", u_email).execute()
            st.rerun()
        except: st.error("Node collision! Choose different slug.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Manage Active Nodes
    res = supabase.table("links").select("*").eq("user_email", u_email).execute()
    for l in res.data:
        col_a, col_b = st.columns([5, 1])
        with col_a:
            st.markdown(f'<div class="glass-card" style="padding:15px; margin-bottom:5px;"><b>{l["short_code"]}</b> | {l.get("clicks", 0)} Clicks</div>', unsafe_allow_html=True)
            st.code(f"https://lynxis-ai.streamlit.app/?c={l['short_code']}")
        with col_b:
            if st.button("🗑️", key=l['short_code']):
                supabase.table("links").delete().eq("short_code", l['short_code']).execute()
                st.rerun()

# --- 7. ANALYTICS ---
elif menu == "Analytics":
    st.markdown("<h1 class='hero-title'>ANALYTICS</h1>", unsafe_allow_html=True)
    res = supabase.table("links").select("*").eq("user_email", u_email).execute()
    if res.data:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(res.data)[['short_code', 'original_url', 'clicks', 'created_at']], use_container_width=True)
        st.metric("Total Traffic", f"{pd.DataFrame(res.data)['clicks'].sum()} Hits")
        st.markdown('</div>', unsafe_allow_html=True)
    else: st.info("No active nodes.")

# --- 8. SETTINGS ---
elif menu == "Settings":
    st.markdown("<h1 class='hero-title'>SETTINGS</h1>", unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    phrase = st.text_input("Type 'ARE YOU SURE YOU WANT TO REMOVE THIS' to purge data")
    if st.button("PURGE EVERYTHING") and phrase == "ARE YOU SURE YOU WANT TO REMOVE THIS":
        supabase.table("links").delete().eq("user_email", u_email).execute()
        supabase.table("users").delete().eq("email", u_email).execute()
        st.logout()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 9. UPGRADE ---
elif menu == "Upgrade ⚡":
    st.markdown("<h1 class='hero-title'>UPGRADE</h1>", unsafe_allow_html=True)
    plan_choice = st.radio("Select Plan", ["Monthly VIP ($29)", "Yearly VIP ($290)"], horizontal=True)
    m_style = "selected-plan" if "Monthly" in plan_choice else ""
    y_style = "selected-plan" if "Yearly" in plan_choice else ""
    c1, c2 = st.columns(2)
    with c1: st.markdown(f'<div class="glass-card {m_style}"><h3>Monthly</h3><p>$29/mo</p></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="glass-card {y_style}"><h3>Yearly</h3><p>$290/yr</p></div>', unsafe_allow_html=True)
    st.markdown(f'''<div class="glass-card" style="text-align:center;"><a href="https://www.buymeacoffee.com/lynxis.ai/membership" target="_blank"><div style="background:#FFDD00; color:black; padding:20px; border-radius:15px; font-weight:900;">⚡ ACTIVATE VIA Card Payment</div></a></div>''', unsafe_allow_html=True)
    if st.button("I HAVE PAID - Send request!"):
        supabase.table("users").update({"pending_upgrade": True}).eq("email", u_email).execute()
        st.success("Admin Notified.")

# --- 10. ADMIN MASTER CONTROL ---
elif menu == "Admin Master Control":
    st.markdown("<h1 class='hero-title'>GOD MODE</h1>", unsafe_allow_html=True)
    all_users = supabase.table("users").select("email").execute()
    st.metric("Total Unique Users", len(all_users.data) if all_users.data else 0)
    try:
        pending = supabase.table("users").select("*").eq("pending_upgrade", True).execute()
        st.subheader("Pending Requests")
        if pending.data: st.write(pd.DataFrame(pending.data))
        else: st.info("None.")
    except: st.error("Check 'pending_upgrade' column.")
    st.divider()
    t_email = st.text_input("Target Email")
    plan = st.selectbox("Tier", ["Monthly (30 Days)", "Yearly (365 Days)"])
    if st.button("GRANT ACCESS"):
        days = 30 if "Monthly" in plan else 365
        exp = (datetime.now(timezone.utc) + timedelta(days=days)).isoformat()
        supabase.table("users").update({"is_premium": True, "premium_until": exp, "pending_upgrade": False, "credits": 9999}).eq("email", t_email).execute()
        st.success("Activated!"); st.balloons()
