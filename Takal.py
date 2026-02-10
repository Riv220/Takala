import streamlit as st
import requests
import base64

# --- הגדרת עמוד ---
st.set_page_config(page_title="מוקד טכני", page_icon="💻", layout="centered", initial_sidebar_state="collapsed")

# --- עיצוב מותאם (CSS) ---
st.markdown("""
    <style>
    /* 1. הסתרת תפריטים */
    [data-testid="stSidebar"] { display: none; }
    #MainMenu { visibility: hidden; }
    
    /* 2. כיוון ימין-שמאל */
    .stApp {
        direction: rtl;
        text-align: right;
    }

    /* 3. העלמה של כפתורי הפלוס והמינוס */
    [data-testid="stNumberInputStepDown"],
    [data-testid="stNumberInputStepUp"] {
        display: none !important;
    }
    
    /* 4. עיצוב כפתור שליחה - ענק וברור */
    [data-testid="stFormSubmitButton"] > button {
        background-color: #007bff; /* כחול טכני */
        color: white;
        border-radius: 12px;
        border: none;
        padding: 20px 0px;
        font-size: 26px !important;
        font-weight: bold;
        width: 100%;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
        margin-top: 15px;
    }
    
    /* אפקט לחיצה */
    [data-testid="stFormSubmitButton"] > button:active {
        background-color: #0056b3;
        transform: scale(0.98);
    }
    
    /* 5. עיצוב האקורדיון של המצלמה */
    .streamlit-expanderHeader {
        font-weight: bold;
        color: #333;
        background-color: #e9ecef;
        border-radius: 8px;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- כתובת הסקריפט שלך (V6) ---
URL = "https://script.google.com/macros/s/AKfycbxFNkmr5JbLmpikXCTpNnjS0XCQjcYI45dQhw4md11nqq48FlHmQBg2AcBidcSZ09LDdw/exec"

# --- כותרת ---
st.markdown("<h1 style='text-align: center; color: #007bff;'>💻 דיווח תקלה טכנית</h1>", unsafe_allow_html=True)

# --- טאבים ---
tab1, tab2 = st.tabs(["🔧 פתיחת קריאה", "✅ סגירה"])

# === טאב 1: פתיחת תקלה ===
with tab1:
    with st.form("open_ticket_form", clear_on_submit=True):
        
        col1, col2 = st.columns([1, 2])
        with col1:
             room_number = st.number_input("חדר", min_value=0, step=1, value=None, placeholder="מספר...")
        with col2:
             # רשימה טכנית בלבד
             issue_type = st.selectbox(
                "מהות התקלה",
                [
                    "מחשב לא עולה / תקוע",
                    "מקרן / מסך",
                    "בעיית רשת / אינטרנט",
                    "מדפסת / סורק",
                    "ציוד היקפי (מקלדת/עכבר)",
                    "כבלים וחיבורים",
                    "תוכנה / סיסמאות",
                    "אחר"
                ]
            )
        
        # שורה קצרה במקום בלוק גדול
        notes = st.text_input("הערה קצרה (אופציונלי)", placeholder="לדוגמה: המחשב של המרצה")
        
        st.write("") 
        
        # --- מצלמה בתוך אקורדיון ---
        with st.expander("📷  צרף תמונה (לחץ כאן)"):
            photo = st.camera_input("צלם")
        
        st.write("")
        
        # --- כפתור שליחה ---
        submit_open = st.form_submit_button("פתח קריאה טכנית 🚀")
        
        if submit_open:
            if room_number is None:
                st.error("⚠️ חובה להזין מספר חדר")
            else:
                image_base64 = ""
                if photo:
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
                    with st.spinner('שולח...'):
                        res = requests.post(URL, data=data)
                    
                    if res.status_code == 200:
                        st.balloons()
                        st.success("✅ הקריאה נפתחה!")
                    else:
                        st.error(f"שגיאה: {res.status_code}")
                except Exception as e:
                    st.error(f"שגיאת תקשורת: {e}")

# === טאב 2: סגירת תקלה ===
with tab2:
    st.markdown("### סגירת טיפול")
    with st.form("close_ticket_form", clear_on_submit=True):
        
        close_room = st.number_input("מספר חדר", min_value=0, step=1, value=None, placeholder="הקלד מספר חדר...", key="close_room")
        
        st.write("")
        submit_close = st.form_submit_button("סגור קריאה 👍")
        
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

col1, col2 = st.columns(2)
with col1:
    st.link_button("📞 חייג", "tel:+972546258744", use_container_width=True)
with col2:
    st.link_button("💬 וואטסאפ", "https://wa.me/972546258744", use_container_width=True)
