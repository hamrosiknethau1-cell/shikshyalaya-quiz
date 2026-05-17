import streamlit as st

# १. पासवर्ड सुरक्षा (Password: nepal123)
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 शिक्षालय अनलाइन क्विज हब")
    password = st.text_input("कृपया वेबसाइटको पासवर्ड राख्नुहोस्:", type="password")
    
    if st.button("प्रवेश गर्नुहोस्"):
        if password == "nepal123":
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("गलत पासवर्ड! कृपया फेरि प्रयास गर्नुहोस्।")
    st.stop()

# २. मुख्य क्विज वेबसाइट
st.title("📚 शिक्षालय (Shikshyalaya) क्विज हब")
st.write("तपाईंको डिजिटल कानुनी र शैक्षिक सहयोगी")
st.markdown("---")

topic = st.sidebar.radio(
    "क्विजको विषय छान्नुहोस्:",
    ("गृहपृष्ठ (Home)", "नेपालको संविधान", "सैनिक ऐन, २०६३", "मुलुकी देवानी संहिता")
)

if topic == "गृहपृष्ठ (Home)":
    st.subheader("शिक्षालय क्विजमा स्वागत छ!")
    st.write("देब्रेपट्टिको मेनुबाट आफूले खेल्न चाहेको कानुन वा विषय छनोट गर्नुहोस्।")

elif topic == "नेपालको संविधान":
    st.subheader("📜 नेपालको संविधान सम्बन्धी क्विज")
    q1 = st.radio("१. नेपालको वर्तमान संविधान कहिले जारी भयो?", ["२०७२ असोज ३", "२०७२ भदौ ३", "२०७२ कार्तिक ३"])
    if st.button("उत्तर जाँच्नुहोस्", key="const_q1"):
        if q1 == "२०७२ असोज ३": st.success("सही उत्तर! 🎉")
        else: st.error("गलत उत्तर! सही उत्तर २०७२ असोज ३ हो।")

elif topic == "सैनिक ऐन, २०६३":
    st.subheader("🪖 सैनिक ऐन, २०६३ सम्बन्धी क्विज")
    q2 = st.radio("१. सैनिक ऐन, २०६३ प्रमाणीकरण कहिले भएको हो?", ["२०६३ मंसिर २३", "२०६३ कार्तिक २३", "२०६३ पुस २३"])
    if st.button("उत्तर जाँच्नुहोस्", key="army_q1"):
        if q2 == "२०६३ मंसिर २३": st.success("सही उत्तर! 🎉")
        else: st.error("गलत उत्तर!")