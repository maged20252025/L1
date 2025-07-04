import streamlit as st
import streamlit.components.v1 as components
from docx import Document
from docx.shared import Inches
import re
import uuid
import os
import time
import html
import csv
from io import BytesIO

# ----------------------------------------------------
# إعدادات الصفحة الأساسية
# ----------------------------------------------------
st.set_page_config(
    page_title="القوانين اليمنية بآخر تعديلاتها حتى عام 2025م",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ... باقي الكود كما هو بدون تغيير ...

def main():
    # ---------- هيدر مع التصميم الجديد وصورة المستخدم ----------
    st.markdown(
        """
        <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 18px; margin-top: 12px;">
            <div style="background: linear-gradient(135deg, #388E3C 80%, #81C784 100%);
                        border-radius: 36px;
                        width: 170px;
                        height: 170px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        box-shadow: 0 8px 32px rgba(56,142,60,0.18);
                        margin-bottom: 10px;
                        border: 3px solid #2e7d32;">
                <img src="data:image/jpeg;base64,{img_base64}" style="width:146px; height:146px; border-radius: 30px; object-fit:cover;" alt="Yemeni Laws Logo"/>
            </div>
            <div style="color: #2e7d32; font-size: 2.05rem; font-family: 'Cairo', 'Tajawal', sans-serif; font-weight: 700; text-align: center; margin-bottom: 0; margin-top: 0; letter-spacing: 1px;">
                القوانين اليمنية بآخر تعديلاتها
            </div>
            <div style="color: #388E3C; font-size: 1.17rem; font-family: 'Cairo', 'Tajawal', sans-serif; text-align: center; margin-bottom: 0; margin-top: 6px;">
                أحدث التعديلات حتى 2025
            </div>
        </div>
        """.format(
            img_base64=st.get_image("image1")  # استخدام الصورة رقم 1 من الصور المرفوعة
        ),
        unsafe_allow_html=True
    )
    st.divider()
    # ------------------------------------------------

    if is_activated():
        run_main_app()
        return

    st.info("👋 مرحباً بك! يرجى تفعيل التطبيق أو بدء التجربة المجانية للاستفادة من جميع الميزات.")

    with st.container(border=True):
        st.subheader("🔐 تفعيل التطبيق")
        code = st.text_input("أدخل كود التفعيل هنا:", key="activation_code_input", help="أدخل الكود الذي حصلت عليه لتفعيل النسخة الكاملة.")
        if st.button("✅ تفعيل الآن", key="activate_button", use_container_width=True):
            if code and activate_app(code.strip()):
                st.success("✅ تم التفعيل بنجاح! يرجى إعادة تشغيل التطبيق لتطبيق التغييرات.")
                st.stop()
            else:
                st.error("❌ كود التفعيل غير صحيح أو انتهت صلاحيته.")

    st.markdown("---")

    with st.container(border=True):
        st.subheader("⏱️ النسخة التجريبية المجانية")
        device_id = get_device_id()
        trial_start = get_trial_start(device_id)

        if trial_start is None:
            if st.button("🚀 بدء التجربة المجانية (3 دقائق)", key="start_trial_button", use_container_width=True):
                register_trial(device_id)
                st.success("✅ بدأت النسخة التجريبية الآن. لديك 3 دقائق لاستخدام التطبيق.")
                st.warning("يرجى التفاعل مع الصفحة (مثلاً، النقر بالماوس أو التمرير) لتحديث الواجهة وبدء استخدام التطبيق.")

        if trial_start is not None:
            elapsed_time = time.time() - trial_start
            remaining_time = TRIAL_DURATION - elapsed_time

            if remaining_time > 0:
                minutes = int(remaining_time // 60)
                seconds = int(remaining_time % 60)
                st.info(f"⏳ النسخة التجريبية لا تزال نشطة. الوقت المتبقي: {minutes:02d}:{seconds:02d}")
                run_main_app()
            else:
                st.error("❌ انتهت مدة التجربة المجانية لهذا الجهاز. يرجى تفعيل التطبيق للاستمرار في الاستخدام.")

if __name__ == "__main__":
    main()
    
