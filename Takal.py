import streamlit as st
import requests

# הגדרות עיצוב
st.set_page_config(page_title="ניהול תקלות", page_icon="🔧", layout="centered")

# --- חלק חדש: סרגל צד עם פרטי קשר ---
with st.sidebar:
    st.header("📞 יצירת קשר מיידי")
    st.write("נתקלת בבעיה דחופה? אני זמין!")
    
    # כפתור חיוג (שים לב: עובד בעיקר מהטלפון)
    st.link_button("התקשר לאדמין 📞", "tel:+972546258744") # <--- שנה את המספר כאן
    
    # כפתור וואטסאפ (אופציונלי)
    st.link_button("שלח הודעה בוואטסאפ 💬", "https://wa.me/972501234567") # <--- שנה את המספר כאן
    
    st.divider()
    st.write("שעות פעילות: 08:00 - 17:00")

# --- סוף סרגל צד ---

# כותרת האפליקציה
st.title("🔧 מערכת ניהול תקלות")

# הלינק שלך (וודא שהוא נכון!)
URL = "https://script.google.com/macros/s/AKfycbxFNkmr5JbLmpikXCTpNnjS0XCQjcYI45dQhw4md11nqq48FlHmQBg2AcBidcSZ09LDdw/exec"

with st.form("ticket_form", clear_on_submit=True):
    
    # 1. בחירת פעולה
    st.subheader("מה ברצונך לבצע?")
    action_type = st.radio(
        "בחר פעולה:",
        ["פתיחת קריאה חדשה 🔴", "סגירת קריאה (טופל) 🟢"],
        horizontal=True
    )
    
    st.divider()

    # 2. מספר חדר - רלוונטי תמיד
    room_number = st.text_input("מספר חדר (לדוגמה: 102)")

    # משתנים שנמלא רק אם זו פתיחת תקלה
    issue_type = "סגירת קריאה"
    notes = ""

    # 3. שדות שמופיעים רק בפתיחת קריאה
    if "פתיחת" in action_type:
        issue_type = st.selectbox(
            "סוג התקלה:",
            [
                "אין אינטרנט",
                "רמקול תקול",
                "חסר כבל HDMI",
                "מקרן לא עובד",
                "בעיה במחשב",
                "אחר"
            ]
        )
        notes = st.text_area("הערות נוספות (אופציונלי)")

    # כפתור שליחה
    submitted = st.form_submit_button("בצע פעולה ✅")

    if submitted:
        if not room_number:
            st.error("חובה להזין מספר חדר!")
        else:
            action_code = "סגור" if "סגירת" in action_type else "פתח"

            data = {
                "פעולה": action_code,
                "מספר חדר": room_number,
                "סוג תקלה": issue_type,
                "הערות": notes
            }
            
            try:
                with st.spinner('מתקשר עם השרת...'):
                    response = requests.post(URL, params=data)
                
                if response.status_code == 200:
                    result_json = response.json()
                    
                    if result_json.get('result') == 'success':
                        if action_code == "סגור":
                            st.success(result_json.get('message'))
                        else:
                            st.success("הקריאה נפתחה בהצלחה! 🔴")
                        st.balloons()
                    else:
                        st.warning(result_json.get('message', 'שגיאה לא ידועה'))
                else:
                    st.error("היתה בעיה בשליחה, נסה שוב.")
            except Exception as e:
                st.error(f"שגיאת תקשורת: {e}")
