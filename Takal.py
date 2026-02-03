import streamlit as st
import requests

# הגדרות עיצוב בסיסיות
st.set_page_config(page_title="ניהול תקלות", page_icon="🔧", layout="centered")

# כותרת האפליקציה
st.title("🔧 מערכת ניהול תקלות")

# כתובת הסקריפט - וודא שזה הלינק שלך!
URL = "https://script.google.com/macros/s/AKfycbxFNkmr5JbLmpikXCTpNnjS0XCQjcYI45dQhw4md11nqq48FlHmQBg2AcBidcSZ09LDdw/exec"

# יצירת טופס
with st.form("ticket_form", clear_on_submit=True):
    
    # === החלק החדש: בחירה מה רוצים לעשות ===
    st.subheader("מה ברצונך לבצע?")
    action_type = st.radio(
        "בחר פעולה:",
        ["פתיחת קריאה חדשה 🔴", "סגירת קריאה (טופל) 🟢"],
        horizontal=True
    )
    
    st.divider() # קו מפריד

    # בחירת סוג התקלה
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
    
    # הזנת מספר חדר
    room_number = st.text_input("מספר חדר (לדוגמה: 102)")
    
    # הערות נוספות
    notes = st.text_area("הערות נוספות (אופציונלי)")

    # כפתור שליחה יחיד
    submitted = st.form_submit_button("בצע פעולה ✅")

    if submitted:
        if not room_number:
            st.error("חובה להזין מספר חדר!")
        else:
            # המרת הבחירה למשהו שהסקריפט מבין
            action_code = "סגור" if "סגירת" in action_type else "פתח"

            # הכנת הנתונים לשליחה
            data = {
                "פעולה": action_code,  # זה הפרמטר החדש
                "סוג תקלה": issue_type,
                "מספר חדר": room_number,
                "הערות": notes
            }
            
            # שליחה לשרת
            try:
                with st.spinner('מתקשר עם השרת...'):
                    response = requests.post(URL, params=data)
                
                if response.status_code == 200:
                    result_json = response.json()
                    
                    if result_json.get('result') == 'success':
                        if action_code == "סגור":
                            st.success(f"התקלה בחדר {room_number} סומנה כטופלה! 🟢")
                        else:
                            st.success("הקריאה נפתחה בהצלחה! 🔴")
                        st.balloons()
                    else:
                        # הודעה אם לא נמצאה תקלה לסגירה
                        st.warning(result_json.get('message', 'שגיאה לא ידועה'))
                else:
                    st.error("היתה בעיה בשליחה, נסה שוב.")
            except Exception as e:
                st.error(f"שגיאת תקשורת: {e}")
