import streamlit as st
import requests

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

    /* 3. העלמה של כפתורי הפלוס והמינוס (כדי שזה ייראה נקי) */
    [data-testid="stNumberInputStepDown"],
    [data-testid="stNumberInputStepUp"] {
        display: none !important;
    }
    
    /* 4. עיצוב כפתורים ירוקים */
    div.stButton > button {
        background-color: #28a745;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 10px 0px;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.3);
    }
    div.stButton > button:hover {
        background-color: #218838;
        color: white;
    }

    /* 5. ריווח */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- משתנים ---
URL = "https://script.google.com/macros/s/AKfycbxFNkmr5JbLmpikXCTpNnjS0XCQjcYI45dQhw4md11nqq48FlHmQBg2AcBidcSZ09LDdw/exec"

# --- כותרת ---
st.markdown("<h1 style='text-align: center; color: #28a745;'>מערכת ניהול תקלות 🍏</h1>", unsafe_allow_html=True)

# --- טאבים ---
tab1, tab2 = st.tabs(["📝 פתיחת תקלה", "✅ סגירה (טופל)"])

# === טאב 1: פתיחת תקלה ===
with tab1:
    st.markdown("##### 📌 דיווח חדש")
    with st.form("open_ticket_form", clear_on_submit=True):
        
        # השינוי הגדול: value=None משאיר את השדה ריק!
        # step=1 מבטיח מספרים שלמים ומקלדת מספרים
        room_number = st.number_input("מספר חדר", min_value=0, step=1, value=None, placeholder="הקלד מספר חדר...")
        
        issue_type = st.selectbox(
            "מה הבעיה?",
            ["אין אינטרנט", "רמקול תקול", "חסר כבל HDMI", "מקרן לא עובד", "בעיה במחשב", "מזגן לא עובד", "אחר"]
        )
        
        notes = st.text_area("הערות (לא חובה)")
        
        st.write("")
        submit_open = st.form_submit_button("שלח דיווח 🚀")
        
        if submit_open:
            # בדיקה אם השדה ריק (None)
            if room_number is None:
                st.error("⚠️ חובה להזין מספר חדר")
            else:
                data = {"פעולה": "פתח", "מספר חדר": room_number, "סוג תקלה": issue_type, "הערות": notes}
                try:
                    with st.spinner('שולח...'):
                        res = requests.post(URL, params=data)
                    if res.status_code == 200:
                        st.balloons()
                        st.success("נשלח בהצלחה! האדמין בדרך.")
                except:
                    st.error("שגיאת תקשורת")

# === טאב 2: סגירת תקלה ===
with tab2:
    st.markdown("##### ✅ סגירת קריאה")
    with st.form("close_ticket_form", clear_on_submit=True):
        
        # גם כאן: מתחיל ריק (None)
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
                        res = requests.post(URL, params=data)
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
st.markdown("<h4 style='text-align: center; margin-bottom: 10px;'>📞 יצירת קשר מהיר</h4>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.link_button("חייג 📞", "tel:+972546258744", use_container_width=True)
with col2:
    st.link_button("וואטסאפ 💬", "https://wa.me/972546258744", use_container_width=True)
