import streamlit as st
import pandas as pd
from supabase import create_client
import random, string, time
from datetime import datetime, timedelta, timezone

st.set_page_config(
    page_title="LYNXIS AI | URL Infrastructure",
    page_icon="🚀",
    layout="wide"
)

# Hidden SEO metadata for Google Bots
st.markdown("""
    <div style="display:none;">
        <h1>Lynxis AI</h1>
        <p>Professional URL shortening, Node management, and Infrastructure for Discord.</p>
        <p>Created by Dali Snouda. High-speed redirection and analytics.</p>
    </div>
""", unsafe_allow_html=True)

# --- 1. MAXIMUM NEBULA UI & ADVANCED ENTERPRISE CSS ---
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
                <br><br>
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
                <br><br><br>
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

# --- 8. ADMIN MASTER CONTROL (The God View) ---
elif menu == "Admin Master Control" and is_admin:
    st.markdown("<h1 class='hero-title'>GOD MODE</h1>", unsafe_allow_html=True)
    
    # --- USER ANALYTICS ---
    all_users_res = supabase.table("users").select("*").execute()
    users_list = all_users_res.data if all_users_res.data else []
    
    # Stats Row
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Registered Users", len(users_list))
    c2.metric("VIP Operators", len([u for u in users_list if u.get('is_premium')]))
    c3.metric("Standard Users", len([u for u in users_list if not u.get('is_premium')]))
    
    # --- MANUAL VIP ELEVATION ---
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Manual VIP Elevation")
    t_email = st.text_input("Target User Email", placeholder="user@example.com")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ ACTIVATE MONTHLY (30 Days)", use_container_width=True):
            expiry = datetime.now(timezone.utc) + timedelta(days=30)
            supabase.table("users").update({
                "is_premium": True, "credits": 9999, "subscription_end": expiry.isoformat()
            }).eq("email", t_email.lower().strip()).execute()
            st.success(f"Monthly VIP activated for {t_email}")
            time.sleep(1); st.rerun()

    with col2:
        if st.button("➕ ACTIVATE YEARLY (365 Days)", use_container_width=True):
            expiry = datetime.now(timezone.utc) + timedelta(days=365)
            supabase.table("users").update({
                "is_premium": True, "credits": 9999, "subscription_end": expiry.isoformat()
            }).eq("email", t_email.lower().strip()).execute()
            st.success(f"Yearly VIP activated for {t_email}")
            time.sleep(1); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # --- USER REGISTRY TABLE ---
    st.subheader("Full User Registry")
    if users_list:
        df_users = pd.DataFrame(users_list)
        # Cleaning up columns for display
        display_df = df_users[['email', 'name', 'is_premium', 'credits', 'subscription_end']]
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No users have registered with the infrastructure yet.")

    # --- SECURITY OVERLOOK (Node Monitor) ---
    st.divider()
    st.subheader("🛡️ GLOBAL NODE MONITOR")
    all_links = supabase.table("links").select("*").order("created_at", desc=True).execute()
    if all_links.data:
        for link in all_links.data:
            with st.expander(f"NODE: {link['short_code']} | Creator: {link['user_email']}"):
                st.write(f"**Target URL:** {link['original_url']}")
                st.write(f"**Clicks:** {link['clicks']}")
                if st.button(f"TERMINATE {link['short_code']}", key=f"kill_{link['short_code']}"):
                    supabase.table("links").delete().eq("short_code", link['short_code']).execute()
                    st.rerun()
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

# --- 7. PRO-LEGAL ENGINE (REAL POLICIES) ---

def show_legal(type):
    # CSS for the "Tall" look
    st.markdown("""
        <style>
            .legal-box {
                padding: 60px 40px; 
                min-height: 70vh; 
                line-height: 1.8;
                font-family: 'Inter', sans-serif;
            }
            .legal-title {
                font-size: 50px;
                letter-spacing: 5px;
                margin-bottom: 40px;
                color: #00f2fe;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<h1 class='legal-title'>{type.upper()}</h1>", unsafe_allow_html=True)
    st.markdown('<div class="glass-card legal-box">', unsafe_allow_html=True)
    
    if type == "Terms of Service":
        st.markdown(f"""
        ### 1. ACCEPTANCE OF PROTOCOL
        By accessing the LYNXIS Infrastructure, you agree to be bound by these Terms of Service and all applicable laws and regulations.
        
        ### 2. PROHIBITED USAGE
        You are strictly prohibited from using LYNXIS for:
        * Phishing or deceptive practices.
        * Distribution of malware or viruses.
        * Any activity that violates the laws of your jurisdiction.
        
        ### 3. INFRASTRUCTURE LIMITATIONS
        LYNXIS is a redirection service. We do not host, control, or verify the content of the destination URLs. Use at your own risk.
        
        ### 4. VIP MEMBERSHIP
        Subscriptions are billed via Buy Me a Coffee. We reserve the right to terminate access for any account found violating security protocols without refund.
        
        *Last Updated: February 2026*
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        ### 1. DATA COLLECTION
        We collect minimal data required for operation: Google Email, Name, and Profile Picture. 
        
        ### 2. ANALYTICS DATA
        We track click counts and timestamps for Nodes created on our platform to provide creator analytics.
        
        ### 3. THIRD-PARTY SERVICES
        Payment information is never stored on our servers. All transactions are handled securely by Stripe/Buy Me a Coffee.
        
        ### 4. YOUR RIGHTS
        You may request a complete data purge via the Settings panel or by contacting our infrastructure lead at **ai.websno@gmail.com**.
        
        *Privacy Shield: Active*
        """, unsafe_allow_html=True)

    if st.button("← RETURN TO INTERFACE", use_container_width=True):
        st.query_params.clear()
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop() 

# --- DETECTION LOGIC ---
params = st.query_params
if params.get("view") == "terms":
    show_legal("Terms of Service")
elif params.get("view") == "privacy":
    show_legal("Privacy Policy")

# --- THE TALL FOOTER ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align: center; padding: 40px; border-top: 1px solid rgba(255,255,255,0.1); margin-top: 50px;">
    <p style="color: #555; font-size: 14px; letter-spacing: 2px;">LYNXIS CORE INFRASTRUCTURE</p>
    <div style="margin: 20px 0;">
        <a href="?view=terms" target="_self" style="color:#4facfe; text-decoration:none; margin:0 15px;">Terms of Service</a>
        <a href="?view=privacy" target="_self" style="color:#4facfe; text-decoration:none; margin:0 15px;">Privacy Policy</a>
        <a href="mailto:ai.websno@gmail.com" style="color:#4facfe; text-decoration:none; margin:0 15px;">Contact Support</a>
    </div>
    <p style="color: #333; font-size: 10px;">© 2026 LYNXIS SYSTEMS. ALL RIGHTS RESERVED.</p>
</div>
""", unsafe_allow_html=True)
