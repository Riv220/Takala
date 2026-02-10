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

    /* 3. העלמה של כפתורי הפלוס והמינוס במספרים */
    [data-testid="stNumberInputStepDown"],
    [data-testid="stNumberInputStepUp"] {
        display: none !important;
    }
    
    /* 4. עיצוב כפתורי הפעולה (פתח/סגור קריאה) */
    div.stButton > button {
        background-color: #007bff; /* כחול ראשי */
        color: white;
        border-radius: 15px;
        border: none;
        padding: 20px 0px; /* גובה הכפתור */
        font-size: 24px !important; /* גודל טקסט */
        font-weight: bold;
        width: 100%; /* רוחב מלא */
        box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
        margin-top: 20px;
        transition: 0.3s;
    }
    
    /* אפקט לחיצה */
    div.stButton > button:active {
        transform: scale(0.98);
        background-color: #0056b3;
    }

    /* 5. עיצוב אזור העלאת קובץ */
    [data-testid="stFileUploader"] section {
        padding: 15px;
        background-color: #f1f3f5;
        border-radius: 12px;
        text-align: center;
        border: 2px dashed #ced4da;
    }

    /* ריווח כללי */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- כתובת הסקריפט (V6) ---
URL = "https://script.google.com/macros/s/AKfycbxFNkmr5JbLmpikXCTpNnjS0XCQjcYI45dQhw4md11nqq48FlHmQBg2AcBidcSZ09LDdw/exec"

# --- כותרת ---
st.markdown("<h1 style='text-align: center; color: #333; margin-bottom: 20px;'>💻 דיווח תקלה טכנית</h1>", unsafe_allow_html=True)

# --- טאבים ---
tab1, tab2 = st.tabs(["🔧 פתיחת קריאה", "✅ סגירה"])

# === טאב 1: פתיחת תקלה ===
with tab1:
    
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
    
    # --- העלאת קובץ (הפתרון הנקי) ---
    photo = st.file_uploader("📷 צרף תמונה (אופציונלי)", type=['png', 'jpg', 'jpeg'])
    
    st.write("")
    
    # --- כפתור שליחה ענק ---
    if st.button("פתח קריאה טכנית 🚀"):
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
    
    if st.button("סגור קריאה 👍"):
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

# --- כפתורי קשר מעוצבים (HTML) ---
# זה נותן לנו שליטה מלאה על הצבעים (ירוק לוואטסאפ, כחול לטלפון)

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
