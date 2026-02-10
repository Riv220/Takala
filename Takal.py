import streamlit as st
import requests
import base64

# --- הגדרת עמוד ---
st.set_page_config(page_title="ניהול תקלות", page_icon="🍏", layout="centered", initial_sidebar_state="collapsed")

# --- עיצוב מותאם (CSS) ---
st.markdown("""
    <style>
    /* 1. הסתרת התפריטים */
    [data-testid="stSidebar"] { display: none; }
    #MainMenu { visibility: hidden; }
    
    /* 2. כיוון טקסט מימין לשמאל */
    .stApp {
        direction: rtl;
        text-align: right;
    }

    /* 3. העלמה של כפתורי הפלוס והמינוס */
    [data-testid="stNumberInputStepDown"],
    [data-testid="stNumberInputStepUp"] {
        display: none !important;
    }
    
    /* 4. עיצוב כפתור שליחה - גדול ובולט! */
    [data-testid="stFormSubmitButton"] > button {
        background-color: #28a745;
        color: white;
        border-radius: 15px;
        border: none;
        padding: 15px 0px; /* גובה הכפתור */
        font-size: 24px !important; /* גודל טקסט ענק */
        font-weight: bold;
        width: 100%;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
        margin-top: 10px;
    }
    
    /* אפקט לחיצה */
    [data-testid="stFormSubmitButton"] > button:active {
        background-color: #1e7e34;
        transform: scale(0.98);
    }
    
    /* 5. עיצוב האקספנדר (איפה שהמצלמה) */
    .streamlit-expanderHeader {
        font-weight: bold;
        color: #555;
        background-color: #f0f2f6;
        border-radius: 10px;
    }

    /* 6. ריווח כללי */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- משתנים ---
# וודא שזו הכתובת של הסקריפט המעודכן (V6)
URL = "https://script.google.com/macros/s/AKfycbxFNkmr5JbLmpikXCTpNnjS0XCQjcYI45dQhw4md11nqq48FlHmQBg2AcBidcSZ09LDdw/exec"

# --- כותרת ---
st.markdown("<h1 style='text-align: center; color: #28a745;'>🍏 מערכת תקלות</h1>", unsafe_allow_html=True)

# --- טאבים ---
tab1, tab2 = st.tabs(["📝 פתיחת תקלה", "✅ סגירה"])

# === טאב 1: פתיחת תקלה ===
with tab1:
    with st.form("open_ticket_form", clear_on_submit=True):
        
        st.markdown("### פרטי הדיווח")
        room_number = st.number_input("מספר חדר", min_value=0, step=1, value=None, placeholder="הקלד מספר חדר...")
        
        issue_type = st.selectbox(
            "מה הבעיה?",
            ["אין אינטרנט", "רמקול תקול", "חסר כבל HDMI", "מקרן לא עובד", "בעיה במחשב", "מזגן לא עובד", "אחר"]
        )
        
        notes = st.text_area("הערות (לא חובה)")
        
        st.write("") # רווח קטן
        
        # --- השינוי הגדול: מצלמה בתוך "מגירה" ---
        with st.expander("📸 הוסף תמונה (לחץ לפתיחה)"):
            st.info("אם המצלמה הפוכה, לחץ על האייקון הקטן בפינה להחלפה")
            photo = st.camera_input("צלם עכשיו")
        
        st.write("")
        submit_open = st.form_submit_button("שלח דיווח 🚀")
        
        if submit_open:
            if room_number is None:
                st.error("⚠️ חובה להזין מספר חדר")
            else:
                image_base64 = ""
                if photo:
                    # המרה מהירה של התמונה לטקסט
                    bytes_data = photo.getvalue()
                    image_base64 = base64.b64encode(bytes_data).decode('utf-8')

                data = {
                    "פעולה": "פתח",
                    "מספר חדר": room_number,
                    "סוג תקלה": issue_type,
                    "הערות": notes,
                    "image_base64": image_base64
                }
                
                try:
                    with st.spinner('שולח דיווח...'):
                        res = requests.post(URL, data=data) # שימוש ב-data לתמיכה בתמונות
                    
                    if res.status_code == 200:
                        st.balloons()
                        st.success("✅ הדיווח נשלח בהצלחה!")
                    else:
                        st.error(f"שגיאה: {res.status_code}")
                except Exception as e:
                    st.error(f"שגיאת תקשורת: {e}")

# === טאב 2: סגירת תקלה ===
with tab2:
    st.markdown("### סגירת קריאה")
    with st.form("close_ticket_form", clear_on_submit=True):
        
        close_room = st.number_input("איזה חדר טופל?", min_value=0, step=1, value=None, placeholder="הקלד מספר חדר...", key="close_room")
        
        st.write("")
        submit_close = st.form_submit_button("עדכן שטופל 👍")
        
        if submit_close:
            if close_room is None:
                st.error("⚠️ איזה חדר?")
            else:
                data = {"פעולה": "סגור", "מספר חדר": close_room, "סוג תקלה": "סגירה", "הערות": ""}
                try:
                    with st.spinner('מעדכן...'):
                        res = requests.post(URL, data=data)
                        response_data = res.json()
                    
                    if response_data.get('result') == 'success':
                        st.success(f"חדר {close_room}: {response_data.get('message')}")
                        st.balloons()
                    else:
                        st.warning("לא נמצאה קריאה פתוחה בחדר הזה.")
                except:
                    st.error("שגיאת תקשורת")

st.divider()

# --- כפתורי קשר ---
col1, col2 = st.columns(2)
with col1:
    st.link_button("📞 חייג", "tel:+972546258744", use_container_width=True)
with col2:
    st.link_button("💬 וואטסאפ", "https://wa.me/972546258744", use_container_width=True)
