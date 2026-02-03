import streamlit as st
import requests

# --- הגדרת עמוד בסיסית ---
st.set_page_config(page_title="ניהול תקלות", page_icon="🍏", layout="centered")

# --- עיצוב מותאם אישית (CSS) לירוק ולבן + עברית ---
st.markdown("""
    <style>
    /* כיוון טקסט מימין לשמאל */
    .stApp {
        direction: rtl;
        text-align: right;
    }
    
    /* צביעת כפתורים בירוק */
    div.stButton > button {
        background-color: #28a745;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #218838;
        color: white;
    }

    /* עיצוב כותרות הטאבים */
    button[data-baseweb="tab"] {
        font-size: 18px;
        font-weight: bold;
    }
    
    /* הסתרת התפריט של סטרימליט בצד למראה נקי */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- משתנים גלובליים ---
URL = "https://script.google.com/macros/s/AKfycbxFNkmr5JbLmpikXCTpNnjS0XCQjcYI45dQhw4md11nqq48FlHmQBg2AcBidcSZ09LDdw/exec"

# --- סרגל צד (תפריט המבורגר בטלפון) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2921/2921226.png", width=100) # אייקון נחמד
    st.title("מרכז תמיכה")
    st.info("אני זמין לכל בעיה דחופה!")
    
    # כפתורים ליצירת קשר
    st.link_button("📞 חייג לאדמין", "tel:+972546258744") 
    st.link_button("💬 שלח וואטסאפ", "https://wa.me/972546258744")

# --- כותרת ראשית ---
st.markdown("<h1 style='text-align: center; color: #28a745;'>מערכת ניהול תקלות 🍏</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>דיווח וטיפול מהיר בתקלות כיתה</p>", unsafe_allow_html=True)

# --- יצירת טאבים לניווט קל בטלפון ---
tab1, tab2 = st.tabs(["📝 פתיחת תקלה חדשה", "✅ סגירת תקלה (טופל)"])

# === טאב 1: פתיחת תקלה ===
with tab1:
    st.success("דיווח תקלה חדשה")
    with st.form("open_ticket_form", clear_on_submit=True):
        room_number = st.number_input("מספר חדר", min_value=1, step=1, placeholder="הקלד מספר חדר...")
        
        issue_type = st.selectbox(
            "מה הבעיה?",
            ["אין אינטרנט", "רמקול תקול", "חסר כבל HDMI", "מקרן לא עובד", "בעיה במחשב", "מזגן לא עובד", "אחר"]
        )
        
        notes = st.text_area("הערות נוספות (לא חובה)")
        
        # כפתור שליחה ירוק וגדול
        submit_open = st.form_submit_button("שלח דיווח 🚀")
        
        if submit_open:
            if not room_number:
                st.error("⚠️ חובה להזין מספר חדר")
            else:
                data = {
                    "פעולה": "פתח",
                    "מספר חדר": room_number,
                    "סוג תקלה": issue_type,
                    "הערות": notes
                }
                try:
                    with st.spinner('שולח דיווח...'):
                        res = requests.post(URL, params=data)
                    if res.status_code == 200:
                        st.balloons()
                        st.success("הדיווח נשלח בהצלחה! האדמין בדרך.")
                except:
                    st.error("שגיאת תקשורת")

# === טאב 2: סגירת תקלה ===
with tab2:
    st.info("סגירת קריאה קיימת")
    with st.form("close_ticket_form", clear_on_submit=True):
        st.write("סיימת לטפל בחדר? הזן את המספר וסגור את הקריאה.")
        
        close_room = st.number_input("מספר חדר לסגירה", min_value=1, step=1, key="close_room")
        
        submit_close = st.form_submit_button("סמן כ-טופל ✅")
        
        if submit_close:
            if not close_room:
                st.error("⚠️ איזה חדר לסגור?")
            else:
                data = {
                    "פעולה": "סגור",
                    "מספר חדר": close_room,
                    "סוג תקלה": "סגירה",
                    "הערות": ""
                }
                try:
                    with st.spinner('מעדכן סטטוס...'):
                        res = requests.post(URL, params=data)
                        response_data = res.json()
                    
                    if response_data.get('result') == 'success':
                        st.success(f"חדר {close_room}: {response_data.get('message')}")
                        st.balloons()
                    else:
                        st.warning("לא נמצאה קריאה פתוחה בחדר הזה.")
                except:
                    st.error("שגיאת תקשורת")
