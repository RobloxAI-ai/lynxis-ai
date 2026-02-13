import streamlit as st
import pandas as pd
from supabase import create_client
import random, string, time
from datetime import datetime, timedelta, timezone

# --- 1. SETTINGS & SEO ---
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

# --- 2. MAXIMUM NEBULA UI & CSS ---
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

# --- 3. DATABASE ---
@st.cache_resource
def init_db():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
supabase = init_db()

# --- 4. REDIRECT PORTAL ---
query_params = st.query_params
if "c" in query_params:
    target_slug = query_params["c"]
    response = supabase.table("links").select("original_url, clicks").eq("short_code", target_slug).execute()
    if response.data:
        node = response.data[0]
        target_url = node["original_url"]
        if not target_url.startswith(("http://", "https://")): target_url = "https://" + target_url
        new_clicks = (node.get("clicks") or 0) + 1
        supabase.table("links").update({"clicks": new_clicks}).eq("short_code", target_slug).execute()
        st.markdown(f"""
            <div style="text-align:center; padding:50px; background:rgba(255,255,255,0.05); border-radius:20px; border:1px solid #4facfe;">
                <h1 style="color:#00f2fe; font-size:40px;">NODE READY</h1>
                <p style="color:#ffffff; font-size:18px;">Security protocols cleared. Open the gateway below:</p><br>
                <a href="{target_url}" target="_blank" style="background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 15px 40px; text-decoration: none; border-radius: 12px; font-weight: bold; font-size: 22px; box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4); display:inline-block;">🚀 ENTER PORTAL</a>
                <p style="color:gray; font-size:12px; margin-top:30px;">Link: {target_url}</p>
            </div>
        """, unsafe_allow_html=True)
        st.stop()

# --- 5. IDENTITY GATEKEEPER ---
u_logged_in = False
u_email = ""
u_name = "User"
try:
    if hasattr(st, "user") and st.user.get("is_logged_in"):
        u_logged_in = True
        u_email = st.user.get("email", "").lower()
        u_name = st.user.get("name", "User")
except: pass

# Local Testing Override
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

# --- 6. USER SYNC ---
u_query = supabase.table("users").select("*").eq("email", u_email).execute()
if not u_query.data:
    supabase.table("users").insert({"email": u_email, "name": u_name, "credits": 5, "is_premium": False}).execute()
    st.rerun()
user_db_data = u_query.data[0]
is_admin = (u_email == "ai.websno@gmail.com" or u_email == "dali.snouda@gmail.com")

# --- 7. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='color:#00f2fe;'>LYNXIS</h1>", unsafe_allow_html=True)
    st.divider()
    st.write(f"Identity: **{u_name}**")
    st.write(f"Credits: `{user_db_data['credits']}/5`" if not user_db_data['is_premium'] else "💎 VIP Access")
    nav = ["Dashboard", "Analytics", "Settings", "Upgrade ⚡"]
    if is_admin: nav.append("Admin Master Control")
    menu = st.radio("GATEWAY", nav)
    if st.button("Secure Logout"): st.logout()

# --- 8. DASHBOARD ---
if menu == "Dashboard":
    st.markdown("<h1 class='hero-title'>ENGINE ROOM</h1>", unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Banned Keywords (The Guard)
    banned_words = ["robux", "free-money", "giftcard", "discord-nitro", "steam-promo", "login-verify", "free-nitro"]
    can_deploy = user_db_data['is_premium'] or (user_db_data['credits'] > 0)
    
    c1, c2 = st.columns([3, 1])
    with c1: t_url = st.text_input("TARGET URL", placeholder="https://...")
    with c2: 
        if user_db_data['is_premium']: slug = st.text_input("CUSTOM SLUG")
        else: st.text_input("SLUG", "🔒 VIP ONLY", disabled=True); slug = ""

    if st.button("🚀 DEPLOY NODE", use_container_width=True, disabled=not (can_deploy and t_url)):
        if any(word in t_url.lower() for word in banned_words):
            st.error("🚩 SECURITY ALERT: This URL violates LYNXIS safety protocols.")
        else:
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
                time.sleep(1); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Manage Active Nodes
    res = supabase.table("links").select("*").eq("user_email", u_email).execute()
    for l in res.data:
        ca, cb = st.columns([5, 1])
        with ca: st.code(f"https://lynxisai.com/?c={l['short_code']}") # Updated for your new domain
        with cb: 
            if st.button("🗑️", key=l['short_code']):
                supabase.table("links").delete().eq("short_code", l['short_code']).execute()
                st.rerun()

# --- 9. ANALYTICS ---
elif menu == "Analytics":
    st.markdown("<h1 class='hero-title'>ANALYTICS</h1>", unsafe_allow_html=True)
    res = supabase.table("links").select("*").eq("user_email", u_email).execute()
    if res.data:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        df = pd.DataFrame(res.data)
        st.metric("Total Hits", df['clicks'].sum())
        st.dataframe(df[['short_code', 'original_url', 'clicks']], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 10. ADMIN MASTER CONTROL ---
elif menu == "Admin Master Control" and is_admin:
    st.markdown("<h1 class='hero-title'>GOD MODE</h1>", unsafe_allow_html=True)
    pending = supabase.table("users").select("*").eq("pending_upgrade", True).execute()
    st.subheader("Pending VIP Requests")
    if pending.data: st.write(pd.DataFrame(pending.data))
    t_email = st.text_input("User Email to Elevate")
    if st.button("ACTIVATE VIP"):
        supabase.table("users").update({"is_premium": True, "credits": 9999, "pending_upgrade": False}).eq("email", t_email).execute()
        st.success("User Elevated.")

# --- 11. SETTINGS & UPGRADE ---
elif menu == "Settings":
    st.markdown("<h1 class='hero-title'>SETTINGS</h1>", unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write(f"**Email:** {u_email}")
    st.write(f"**Status:** {'💎 VIP' if user_db_data['is_premium'] else 'Standard'}")
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "Upgrade ⚡":
    st.markdown("<h1 class='hero-title'>EVOLVE</h1>", unsafe_allow_html=True)
    plan_type = st.radio("SELECT BILLING CYCLE", ["Monthly", "Yearly (Save 20%)"], horizontal=True)
    price = "29" if "Monthly" in plan_type else "279"
    period = "mo" if "Monthly" in plan_type else "yr"
    
    c1, c2 = st.columns(2)
    with c1: st.markdown('<div class="glass-card"><h3>STD</h3><h1>$0</h1></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="glass-card" style="border-color:#00f2fe;"><h3>PREM</h3><h1>${price}/{period}</h1></div>', unsafe_allow_html=True)
    
    st.link_button("💳 PAY VIA CARD PAYMENT", "https://www.buymeacoffee.com/lynxis.ai/membership", use_container_width=True)

# --- 12. LEGAL (TALL) ---
def show_legal(type):
    st.markdown(f"<h1 class='hero-title'>{type.upper()}</h1>", unsafe_allow_html=True)
    st.markdown('<div class="glass-card" style="min-height:70vh; padding:60px;">', unsafe_allow_html=True)
    if type == "Terms of Service":
        st.write("### 1. ACCEPTANCE... \n LYNXIS Infrastructure is for lawful use only.")
    else:
        st.write("### 1. PRIVACY... \n We only store Google Identity data.")
    if st.button("← RETURN TO INTERFACE"):
        st.query_params.clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

params = st.query_params
if params.get("view") == "terms": show_legal("Terms of Service")
elif params.get("view") == "privacy": show_legal("Privacy Policy")

# --- 13. FOOTER & SECURITY OVERWATCH ---
st.markdown(f"""
<div style="text-align: center; padding: 40px; border-top: 1px solid rgba(255,255,255,0.1); margin-top: 50px;">
    <a href="?view=terms" target="_self" style="color:#4facfe; text-decoration:none; margin:0 15px;">Terms</a> | 
    <a href="?view=privacy" target="_self" style="color:#4facfe; text-decoration:none; margin:0 15px;">Privacy</a> | 
    <a href="mailto:ai.websno@gmail.com" style="color:#4facfe; text-decoration:none; margin:0 15px;">Support</a>
    <p style="color: #333; font-size: 10px; margin-top:10px;">© 2026 LYNXIS SYSTEMS.</p>
</div>
""", unsafe_allow_html=True)

if is_admin:
    st.markdown("---")
    st.markdown("### 🛡️ INFRASTRUCTURE SECURITY OVERWATCH (Admin Only)")
    all_links = supabase.table("links").select("*").order("created_at", desc=True).execute()
    if all_links.data:
        for link in all_links.data:
            with st.expander(f"NODE: {link['short_code']} | Target: {link['original_url'][:40]}..."):
                st.write(f"Creator: {link.get('user_email', 'Unknown')}")
                if st.button(f"🚩 TERMINATE {link['short_code']}", key=f"overwatch_{link['short_code']}"):
                    supabase.table("links").delete().eq("short_code", link['short_code']).execute()
                    st.success("Purged."); time.sleep(0.5); st.rerun()
