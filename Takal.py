import streamlit as st
import requests

# הגדרות עיצוב
st.set_page_config(page_title="ניהול תקלות", page_icon="🔧", layout="centered")
st.title("🔧 מערכת ניהול תקלות")

# הלינק שלך (וודא שהוא נכון!)
URL = "https://script.google.com/macros/s/AKfycbxFNkmr5JbLmpikXCTpNnjS0XCQjcYI45dQhw4md11nqq48FlHmQBg2AcBidcSZ09LDdw/exec"

with st.form("ticket_form", clear_on_submit=True):
    
    # 1. קודם כל בוחרים פעולה
    st.subheader("מה ברצונך לבצע?")
    action_type = st.radio(
        "בחר פעולה:",
        ["פתיחת קריאה חדשה 🔴", "סגירת קריאה (טופל) 🟢"],
        horizontal=True
    )
    
    st.divider()

    # 2. מספר חדר - רלוונטי תמיד (גם בפתיחה וגם בסגירה)
    room_number = st.text_input("מספר חדר (לדוגמה: 102)")

    # משתנים שנמלא רק אם זו פתיחת תקלה
    issue_type = "סגירת קריאה" # ברירת מחדל לסגירה
    notes = ""

    # 3. שדות שמופיעים *רק* אם בחרנו "פתיחת קריאה"
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
            # קביעת סוג הפעולה לשליחה
            action_code = "סגור" if "סגירת" in action_type else "פתח"

            # הכנת הנתונים
            data = {
                "פעולה": action_code,
                "מספר חדר": room_number,
                "סוג תקלה": issue_type, # בסגירה זה ישלח סתם טקסט, הסקריפט יתעלם מזה
                "הערות": notes
            }
            
            try:
                # שליחה לשרת
                with st.spinner('מתקשר עם השרת...'):
                    response = requests.post(URL, params=data)
                
                if response.status_code == 200:
                    result_json = response.json()
                    
                    if result_json.get('result') == 'success':
                        if action_code == "סגור":
                            st.success(result_json.get('message')) # הודעה מהשרת
                            st.balloons()
                        else:
                            st.success("הקריאה נפתחה בהצלחה! 🔴")
                    else:
                        st.warning(result_json.get('message', 'שגיאה לא ידועה'))
                else:
                    st.error("היתה בעיה בשליחה, נסה שוב.")
            except Exception as e:
                st.error(f"שגיאת תקשורת: {e}")
