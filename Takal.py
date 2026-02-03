import streamlit as st
import requests

# הגדרות עיצוב בסיסיות (כותרת, אייקון)
st.set_page_config(page_title="דיווח תקלות", page_icon="🔧", layout="centered")

# כותרת האפליקציה
st.title("🔧 דיווח תקלה טכנית")
st.write("אנא מלא את פרטי התקלה כדי שהאדמין יקבל התראה מיידית.")

# כתובת הסקריפט של גוגל (הדבק כאן את הלינק שיצרנו בשלב ה-Google Sheets)
URL = "https://script.google.com/macros/s/AKfycbxFNkmr5JbLmpikXCTpNnjS0XCQjcYI45dQhw4md11nqq48FlHmQBg2AcBidcSZ09LDdw/exec"
# טופס הדיווח
with st.form("ticket_form", clear_on_submit=True):
    # בחירת סוג התקלה
    issue_type = st.selectbox(
        "מה סוג התקלה?",
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
    
    # הערות נוספות (אופציונלי)
    notes = st.text_area("הערות נוספות (אופציונלי)")

    # כפתור שליחה
    submitted = st.form_submit_button("שלח קריאה ✅")

    if submitted:
        if not room_number:
            st.error("חובה להזין מספר חדר!")
        else:
            # הכנת הנתונים לשליחה
            data = {
                "סוג תקלה": issue_type,
                "מספר חדר": room_number,
                "הערות": notes
            }
            
            # שליחת הנתונים לגוגל שיטס
            try:
                response = requests.post(URL, params=data)
                if response.status_code == 200:
                    st.success("הקריאה נשלחה בהצלחה! האדמין קיבל התראה.")
                    st.balloons() # אפקט נחמד של בלונים
                else:
                    st.error("היתה בעיה בשליחה, נסה שוב.")
            except Exception as e:
                st.error(f"שגיאת תקשורת: {e}")
