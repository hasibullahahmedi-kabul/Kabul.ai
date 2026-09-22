import streamlit as st
import subprocess
from data_spy import fetch_global_intel
from brother_brain import analyze_with_brother_eye

# تنظیمات ظاهری داشبورد برادر چشمی
st.set_page_config(page_title="Brother Eye OS", page_icon="👁️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #00ff66; }
    h1 { color: #ff0055; font-family: 'Courier New', Courier, monospace; }
    </style>
    """, unsafe_allow_index=True)

st.title("👁️ BROTHER EYE - TACTICAL MONITORING SYSTEM")
st.write("سیستم پایش و تحلیل استراتژیک برادر چشمی فعال است.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📡 کنترل سخت‌افزار و چشمی")
    if st.button("فعال‌سازی اسکنر تصویری (دوربین)"):
        st.info("در حال باز کردن دوربین... برای خروج در پنجره باز شده کلید Q را بزنید.")
        # اجرای اسکریپت دوربین به صورت جداگانه
        subprocess.Popen(["python", "eye_scanner.py"])

with col2:
    st.subheader("🌐 اطلاعات شبکه و جاسوسی")
    if st.button("دریافت آخرین داده‌های اینتل"):
        intel = fetch_global_intel()
        st.session_state['intel'] = intel
        for item in intel:
            st.write(item)

st.write("---")
st.subheader("🧠 مرکز فرماندهی و چت با برادر چشمی")

user_input = st.text_input("دستور خود را وارد کنید، اپراتور:")
if st.button("ارسال دستور"):
    current_intel = st.session_state.get('intel', ["داده جدیدی از شبکه دریافت نشده است."])
    with st.spinner("در حال تحلیل منطقی..."):
        answer = analyze_with_brother_eye(user_input, current_intel)
        st.text_area("پاسخ برادر چشمی:", value=answer, height=200)
