import streamlit as st
import requests
import base64

# --- הגדרת עמוד ---
st.set_page_config(page_title="מוקד טכני", page_icon="💻", layout="centered", initial_sidebar_state="collapsed")

# --- עיצוב מותאם (CSS) ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    #MainMenu { visibility: hidden; }
    
    .stApp {
        direction: rtl;
        text-align: right;
    }

    [data-testid="stNumberInputStepDown"],
    [data-testid="stNumberInputStepUp"] {
        display: none !important;
    }
    
    /* התיקון לכפתור - מכריח אותו ואת העטיפה שלו להיות 100% */
    div[data-testid="stFormSubmitButton"], 
    div[data-testid="stFormSubmitButton"] > button {
        width: 100% !important;
        display: block !important;
    }
    
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #007bff !important; 
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 15px 0px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2) !important;
    }
    
    div[data-testid="stFormSubmitButton"] > button:active {
        background-color: #0056b3 !important;
        transform: scale(0.98) !important;
    }
    
    div.stButton > button {
        width: 100% !important;
        border-radius: 12px !important;
        padding: 15px 0 !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }

    [data-testid="stFileUploader"] section {
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 12px;
        text-align: center;
        border: 2px dashed #ced4da;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- פונקציה לשליחה לטלגרם ---
def send_telegram_alert(room, issue, notes):
    bot_token = "8658832858:AAHfW3hMpNF1VA-anxTUGpbPNod5funoCG4" # הטוקן שהרגע הבאת לי
    chat_id = "6432576359" # ה-ID שלך
    
    message = f"🚨 קריאה טכנית חדשה!\n\n🚪 חדר: {room}\n🔧 תקלה: {issue}\n📝 הערות: {notes}"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    
    try:
        requests.post(url, json=payload)
    except Exception as e:
        st.error(f"שגיאה בטלגרם: {e}")

# --- כתובת הסקריפט (גוגל שיטס) ---
URL = "https://script.google.com/macros/s/AKfycbxFNkmr5JbLmpikXCTpNnjS0XCQjcYI45dQhw4md11nqq48FlHmQBg2AcBidcSZ09LDdw/exec"

# --- כותרת ---
st.markdown("<h1 style='text-align: center; color: #28a745; margin-bottom: 20px;'>💻 דיווח תקלה טכנית</h1>", unsafe_allow_html=True)

# --- טאבים ---
tab1, tab2 = st.tabs(["🔧 פתיחת קריאה", "✅ סגירה"])

# === טאב 1: פתיחת תקלה ===
with tab1:
    with st.form("open_ticket_form", clear_on_submit=True):
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            room_number = st.number_input("חדר", min_value=0, step=1, value=None, placeholder="מספר")
        
        with col2:
            issue_type = st.selectbox(
            "מהות התקלה",
            [
                "מקרן (תקלה / שלט)",
                "מסך (גלילה / טלוויזיה)",
                "כבל HDMI (חסר / תקול)",
                "רמקולים / סאונד",
                "מחשב תקוע / לא עולה",
                "אינטרנט / רשת",
                "מדפסת / סורק",
                "אחר"
            ]
        )
    
        notes = st.text_area("הערות נוספות", height=100)
        
        st.write("") 
        
        photo = st.file_uploader("📷 צרף תמונה (אופציונלי)", type=['png', 'jpg', 'jpeg'])
        
        st.write("")
        
        submit_open = st.form_submit_button("פתח קריאה טכנית 🚀", use_container_width=True)
        
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
                    with st.spinner('שולח דיווח...'):
                        res = requests.post(URL, data=data)
                    
                    if res.status_code == 200:
                        # שולח התראה לטלגרם!
                        send_telegram_alert(room_number, issue_type, notes)
                        
                        st.balloons()
                        st.success("✅ הקריאה נפתחה בהצלחה!")
                    else:
                        st.error(f"שגיאה: {res.status_code}")
                except Exception as e:
                    st.error(f"שגיאת תקשורת: {e}")

# === טאב 2: סגירת תקלה ===
with tab2:
    st.markdown("### 🏁 סגירת טיפול")
    
    close_room = st.number_input("מספר חדר", min_value=0, step=1, value=None, placeholder="הקלד מספר חדר...", key="close_room")
    
    st.write("")
    
    if st.button("סגור קריאה 👍", use_container_width=True):
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

# --- כפתורי קשר תחתונים ---
st.markdown("""
<div style="display: flex; gap: 10px;">
    <a href="tel:+972546258744" style="text-decoration: none; width: 100%;">
        <div style="
            background-color: #0d6efd; 
            color: white; 
            padding: 15px; 
            border-radius: 12px; 
            text-align: center; 
            font-weight: bold; 
            font-size: 18px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            📞 חייג
        </div>
    </a>
    <a href="https://wa.me/972546258744" style="text-decoration: none; width: 100%;">
        <div style="
            background-color: #25D366; 
            color: white; 
            padding: 15px; 
            border-radius: 12px; 
            text-align: center; 
            font-weight: bold; 
            font-size: 18px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            💬 וואטסאפ
        </div>
    </a>
</div>
""", unsafe_allow_html=True)
