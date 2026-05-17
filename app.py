import streamlit as st
import time

# १. सेसन स्टेटहरू (Session States) व्यवस्थापन
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user_role" not in st.session_state:
    st.session_state["user_role"] = None
if "current_question" not in st.session_state:
    st.session_state["current_question"] = 0
if "score" not in st.session_state:
    st.session_state["score"] = 0
if "answered" not in st.session_state:
    st.session_state["answered"] = False
if "start_time" not in st.session_state:
    st.session_state["start_time"] = None
if "total_time_taken" not in st.session_state:
    st.session_state["total_time_taken"] = 0
if "num_questions_selected" not in st.session_state:
    st.session_state["num_questions_selected"] = 10
if "quiz_finished" not in st.session_state:
    st.session_state["quiz_finished"] = False

# क्विज रिसेट गर्ने फङ्सन
def reset_quiz():
    st.session_state["current_question"] = 0
    st.session_state["score"] = 0
    st.session_state["answered"] = False
    st.session_state["start_time"] = time.time()
    st.session_state["total_time_taken"] = 0
    st.session_state["quiz_finished"] = False

def logout():
    st.session_state["authenticated"] = False
    st.session_state["user_role"] = None
    reset_quiz()

# २. लगइन विन्डो
if not st.session_state["authenticated"]:
    st.title("🔒 शिक्षालय अनलाइन क्विज हब")
    st.subheader("कृपया अगाडि बढ्न आफ्नो पासवर्ड राख्नुहोस्")
    st.write("---")
    
    password = st.text_input("पासवर्ड (Password):", type="password")
    
    if st.button("प्रवेश गर्नुहोस् 🔓"):
        if password == "nepal123":
            st.session_state["authenticated"] = True
            st.session_state["user_role"] = "admin"
            reset_quiz()
            st.rerun()
        elif password == "user123":
            st.session_state["authenticated"] = True
            st.session_state["user_role"] = "user"
            reset_quiz()
            st.rerun()
        else:
            st.error("गलत पासवर्ड! (Admin: nepal123 / User: user123)")
    st.stop()


# --- ३. सुरक्षित वाटरमार्क र आकर्षक CSS स्टाइल ---
st.markdown(
    """
    <style>
    .stApp { background-color: #f4f7f6 !important; }
    .stApp::before {
        content: "SHIKSHYALAYA QUIZ HUB";
        position: fixed; top: 50%; left: 50%;
        transform: translate(-50%, -50%) rotate(-30deg);
        font-size: 5.5rem; font-weight: bold;
        color: rgba(0, 51, 102, 0.03); z-index: -1;  
        pointer-events: none; white-space: nowrap;
    }
    h1 { color: #1e3c72 !important; font-weight: 800 !important; }
    h2, h3 { color: #2a5298 !important; font-weight: bold !important; }
    
    div[data-testid="stRadio"] label p {
        font-size: 1.15rem !important; color: #111111 !important; font-weight: 600 !important;
    }
    div.stButton > button {
        background: linear-gradient(to right, #1e3c72, #2a5298) !important;
        color: white !important; border-radius: 8px !important; font-weight: bold !important;
    }
    .marksheet-table {
        width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 1.1rem;
        background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .marksheet-table th { background-color: #1e3c72; color: white; text-align: left; padding: 12px; }
    .marksheet-table td { padding: 12px; border-bottom: 1px solid #dddddd; }
    </style>
    """,
    unsafe_allow_html=True
)

# ४. मुख्य शीर्षक
st.title("📚 शिक्षालय (Shikshyalaya) क्विज हब")
st.markdown("---")


# ५. देब्रेपट्टीको मेनु बार (Sidebar)
st.sidebar.title("🎛️ मेनु बार")
topic = st.sidebar.radio(
    "क्विजको विषय छान्नुहोस्:",
    ("गृहपृष्ठ (Home)", "नेपालको संविधान", "सैनिक ऐन, २०६३", "मुलुकी देवानी संहिता"),
    on_change=reset_quiz
)

st.sidebar.write("---")

# प्रश्न संख्या रोज्ने Option (ड्रपडाउन मेनु)
if topic != "गृहपृष्ठ (Home)":
    st.session_state["num_questions_selected"] = st.sidebar.selectbox(
        "❓ प्रश्न संख्या छान्नुहोस्:",
        (5, 10, 15, 20),
        index=1,
        disabled=st.session_state["current_question"] > 0 or st.session_state["quiz_finished"]
    )
    st.sidebar.caption("नोट: परीक्षा सुरु भएपछि प्रश्न संख्या परिवर्तन गर्न मिल्दैन।")

st.sidebar.write("---")
if st.sidebar.button("🔒 लगआउट (Logout)"):
    logout()
    st.rerun()


# ६. प्रश्नहरूको वृहत डाटाबेस (१० भन्दा बढी थपिएको ताकी युजरले चाहेमा धेरै रोज्न सकोस्)
raw_quiz_data = {
    "नेपालको संविधान": [
        {"q": "१. नेपालको वर्तमान संविधान कहिले जारी भयो?", "options": ["२०७२ भदौ ३", "२०७२ असोज ३", "२०७२ कार्तिक ३"], "ans": "२०७२ असोज ३", "hint": "यो संबिधान २०७२ सालको वडादसैँको आसपास जारी भएको हो।"},
        {"q": "२. नेपालको संविधानमा कतिवटा मौलिक हकहरू व्यवस्था गरिएको छ?", "options": ["३० वटा", "२५ वटा", "३१ वटा"], "ans": "३१ वटा", "hint": "भाग ३ मा सम्मानपूर्वक बाँच्न पाउने हकदेखि उपभोक्ताको हकसम्म समेटिएका छन्।"},
        {"q": "३. नेपालको संविधानमा कति भाग, धारा र अनुसूचीहरू छन्?", "options": ["३५ भाग, ३०८ धारा, ९ अनुसूची", "३५ भाग, धारा ३१५, धारा ८ अनुसूची", "३0 भाग, ३०० धारा, ७ अनुसूची"], "ans": "३५ भाग, ३०८ धारा, ९ अनुसूची", "hint": "पहिलो जारी हुँदा र हालसम्म यो संरचना परिवर्तन भएको छैन।"},
        {"q": "४. नेपालको संविधानको कुन धारामा 'समानताको हक' व्यवस्था गरिएको छ?", "options": ["धारा १६", "धारा १८", "धारा १७"], "ans": "धारा १८", "hint": "यो हक मौलिक हक अन्तर्गत पर्दछ।"},
        {"q": "५. संविधान अनुसार नेपालको सार्वभौमसत्ता र राजकीयसत्ता कसमा निहित रहेको छ?", "options": ["राष्ट्रपतिमा", "संसदमा", "नेपाली जनतामा"], "ans": "नेपाली जनतामा", "hint": "धारा २ मा यसको स्पष्ट व्याख्या गरिएको छ।"},
        {"q": "६. नेपालको संविधान संसोधन सम्बन्धी व्यवस्था कुन भागमा गरिएको छ?", "options": ["भाग २७", "भाग २८", "भाग २९"], "ans": "भाग २७", "hint": "यो भागमा संविधान संसोधनको प्रक्रिया र सीमाहरू तोकिएका छन्।"},
        {"q": "७. नेपालको संविधानमा नागरिकका कतिवटा कर्तव्यहरू तोकिएका छन्?", "options": ["५ वटा", "४ वटा", "६ वटा"], "ans": "४ वटा", "hint": "धारा ४८ मा राष्ट्रप्रति वफादार हुनेसहितका कर्तव्य छन्।"},
        {"q": "८. संबैधानिक निकाय 'अख्तियार दुरुपयोग अनुसन्धान आयोग' सम्बन्धी व्यवस्था कुन भागमा छ?", "options": ["भाग २२", "भाग २३", "भाग २१"], "ans": "भाग २१", "hint": "यो भ्रष्टाचार नियन्त्रण गर्ने नेपालको प्रमुख संवैधानिक निकाय हो।"},
        {"q": "९. नेपालको राष्ट्रिय झण्डा सम्बन्धी व्यवस्था संविधानको कुन अनुसूचीमा छ?", "options": ["अनुसूची १", "अनुसूची २", "अनुसूची ३"], "ans": "अनुसूची १", "hint": "यसमा झण्डा बनाउने तरिका र रङहरूको ठ्याक्कै नाप दिइएको छ।"},
        {"q": "१०. स्थानीय तहको व्यवस्थापकीय अधिकार कुन धारामा उल्लेख छ?", "options": ["धारा २२६", "धारा २३०", "धारा २२१"], "ans": "धारा २२१", "hint": "यसले गाउँ सभा र नगर सभाको व्यवस्थापकीय अधिकारलाई सुनिश्चित गर्छ।"},
        {"q": "११. नेपालको वर्तमान संविधान घोषणा कसले गरेका थिए?", "options": ["रामवरण यादव", "सुशील कोइराला", "केपी शर्मा ओली"], "ans": "रामवरण यादव", "hint": "नेपालका प्रथम राष्ट्रपतिको हैसियतमा उनले यो संविधान जारी गरेका हुन्।"},
        {"q": "१२. नेपालको संविधानको कुन भागमा नागरिकता सम्बन्धी व्यवस्था छ?", "options": ["भाग २", "भाग ३", "भाग ४"], "ans": "भाग २", "hint": "यस भागमा प्रादेशिक पहिचानसहितको सङ्घीय नागरिकताको व्यवस्था छ।"}
    ],
    "सैनिक ऐन, २०६३": [
        {"q": "१. सैनिक ऐन, २०६३ प्रमाणीकरण कहिले भएको हो?", "options": ["२०६३ कार्तिक २३", "२०६३ मंसिर २३", "२०६३ पुस २३"], "ans": "२०६३ मंसिर २३", "hint": "यो ऐन तत्कालीन व्यवस्थापिका-संसदले पारित गरेपछि लालमोहर लागेको हो।"},
        {"q": "२. सैनिक ऐन, २०६३ बमोजिम नेपाली सेनाको नियन्त्रण, प्रयोग र व्यवस्थापन कसले गर्छ?", "options": ["नेपाल सरकार", "प्रधानसेनापति", "रक्षामन्त्री"], "ans": "नेपाल सरकार", "hint": "ऐनको धारा ४ बमोजिम यो अधिकार मन्त्रिपरिषद्मा निहित हुन्छ।"},
        {"q": "३. सैनिक ऐन, २०६३ मा कति परिच्छेदहरू रहेका छन्?", "options": ["१५ वटा", "१३ वटा", "१० वटा"], "ans": "१३ वटा", "hint": "यस ऐनमा सैनिक अदालत, अनुशासन र सेवा सर्त सम्बन्धी व्यवस्थाहरू समेटिएका छन्।"},
        {"q": "४. राष्ट्रिय सुरक्षा परिषद्को अध्यक्ष को हुने संवैधानिक / कानुनी व्यवस्था छ?", "options": ["रक्षामन्त्री", "प्रधानसेनापति", "प्रधानमन्त्री"], "ans": "प्रधानमन्त्री", "hint": "सेना परिचालनको सिफारिस गर्ने यो उच्च निकायको नेतृत्व देशको कार्यकारी प्रमुखले गर्छन्।"},
        {"q": "५. सैनिक ऐन अनुसार प्रधानसेनापतिको पदावधि कति वर्षको हुनेछ?", "options": ["३ वर्ष", "४ वर्ष", "५ वर्ष"], "ans": "३ वर्ष", "hint": "धारा १४ अनुसार प्रधानसेनापति आफ्नो पदमा निश्चित अवधिसम्म मात्र रहन पाउँछन्।"},
        {"q": "६. सैनिक ऐन अनुसार कसको सिफारिसमा नेपाल सरकारले प्रधानसेनापतिको नियुक्ति गर्दछ?", "options": ["सुरक्षा परिषद्", "मन्त्रिपरिषद्", "रक्षामन्त्रालय"], "ans": "मन्त्रिपरिषद्", "hint": "धारा ८ अनुसार मन्त्रिपरिषद्को सिफारिसमा राष्ट्रपतिबाट औपचारिक नियुक्ति हुन्छ।"},
        {"q": "७. सैनिक अदालतको गठन सम्बन्धी व्यवस्था सैनिक ऐनको कुन परिच्छेदमा छ?", "options": ["परिच्छेद ११", "परिच्छेद १०", "परिच्छेद १२"], "ans": "परिच्छेद ११", "hint": "सैनिक कसुरहरूको सुनुवाइ गर्न विशेष अदालतहरूको व्यवस्था यही परिच्छेदमा छ।"},
        {"q": "८. सैनिक विशेष अदालतको अध्यक्ष को हुने व्यवस्था छ?", "options": ["सैनिक रक्षा सचिव", "उच्च अदालतको न्यायाधीश", "प्रधानसेनापति"], "ans": "उच्च अदालतको न्यायाधीश", "hint": "धारा ११९ अनुसार कानुनी निष्पक्षताका लागि अदालतको बहालवाला न्यायाधीश तोकिन्छ।"},
        {"q": "९. सैनिक ऐन बमोजिम भगौडा सैनिकलाई पक्रने अधिकार कसलाई हुन्छ?", "options": ["सैनिक प्रहरीलाई मात्र", "नेपाल प्रहरीलाई मात्र", "नेपाली सेना र नेपाल प्रहरी दुवैलाई"], "ans": "नेपाली सेना र नेपाल प्रहरी दुवैलाई", "hint": "गैरकानुनी रूपमा सेवा छाडेका व्यक्तिलाई नियन्त्रणमा लिन दुवै सुरक्षा निकाय समन्वय गर्छन्।"},
        {"q": "१०. सैनिक सेवाबाट अवकाश दिने उमेर हद सम्बन्धी व्यवस्था कहाँ तोकिएको छ?", "options": ["सैनिक नियमावलीमा", "सैनिक ऐनमा", "नेपालको संविधानमा"], "ans": "सैनिक नियमावलीमा", "hint": "पद अनुसारको उमेरको हद र विस्तृत नियмаवली सरकारले स्वीकृत गर्छ।"}
    ],
    "मुलुकी देवानी संहिता": [
        {"q": "१. मुलुकी देवानी संहिता, २०७४ कहिलेदेखि लागू भयो?", "options": ["२०७४ भदौ १ गते", "२०७५ असोज १ गते", "२०७५ भदौ १ गते"], "ans": "२०७५ भभदौ १ गते", "hint": "यो कानुन पुरानो मुलुकी ऐन, २०२० लाई प्रतिस्थापन गर्दै लागू भएको हो।"},
        {"q": "२. देवानी संहिता अनुसार कति वर्ष उमेर पूरा भएपछि विवाह गर्न योग्य मानिन्छ?", "options": ["२० वर्ष", "१८ वर्ष", "२१ वर्ष"], "ans": "२० वर्ष", "hint": "नयाँ कानुनी प्रावधानले केटा र केटी दुवैका लागि एउटै उमेर हद तोकेको छ।"},
        {"q": "३. देवानी कानूनको सामान्य सिद्धान्त अन्तर्गत कानूनको अज्ञानता के मानिन्छ?", "options": ["क्षम्य हुन्छ", "क्षम्य हुँदैन", "अदालतको इच्छामा भर पर्छ"], "ans": "क्षम्य हुँदैन", "hint": "'मलाई यो कानुन थाहा थिएन' भनेर कसुर वा दायित्वबाट उम्किन पाइँदैन।"},
        {"q": "४. देवानी संहिता अनुसार कति वर्षसम्म कतै जानकारी नभएमा व्यक्तिको प्राकृतिक मृत्यु भएको मानिन्छ (हराएको हकमा)?", "options": ["१० वर्ष", "१२ वर्ष", "७ वर्ष"], "ans": "१२ वर्ष", "hint": "लामो समयसम्म फेला नपरेका व्यक्तिको सम्पत्ति र हक हस्तान्तरणका लागि यो कानुनी अवधि तोकिएको हो।"},
        {"q": "५. मुलुकी देवानी संहितामा 'सम्पत्ति सम्बन्धी व्यवस्था' कुन भागमा गरिएको छ?", "options": ["भाग ३", "भाग ५", "भाग ४"], "ans": "भाग ४", "hint": "यस भागमा भोगचलन, स्वामित्व र हक हस्तान्तरणका नियमहरू छन्।"},
        {"q": "६. देवानी संहिता अनुसार कस्तो सम्पत्तिलाई 'अचल सम्पत्ति' मानिन्छ?", "options": ["जग्गा र जग्गामा बनेको घर", "सुनचाँदी र नगद", "शेयर र बैंक ब्यालेन्स"], "ans": "जग्गा र जग्गामा बनेको घर", "hint": "सहजै एक ठाउँबाट अर्को ठाउँमा सार्न नसकिने वस्तुहरू पर्छन्।"},
        {"q": "७. देवानी संहिता अनुसार 'करार' (Contract) हुनका लागि कम्तीमा कति पक्ष आवश्यक पर्छन्?", "options": ["एक मात्र पक्ष", "दुई वा दुई भन्दा बढी पक्ष", "तीन पक्ष अनिवार्य"], "ans": "दुई वा दुई भन्दा बढी पक्ष", "hint": "सहमति र सम्झौता हुन सधैँ प्रस्ताव राख्ने र स्वीकार गर्ने भिन्दाभिन्दै व्यक्ति चाहिन्छ।"},
        {"q": "८. अंशियारहरूका बीच सम्पत्ति अंशबण्डा गर्दा कुन आधारमा गरिन्छ?", "options": ["समान आधारमा", "जेठो छोराको इच्छामा", "कमाउने व्यक्तिको हकमा"], "ans": "समान आधारमा", "hint": "देवानी संहिताले बराबरी हक दिन्छ।"},
        {"q": "९. हकसाफी (Pre-emption) सम्बन्धी दाबी गर्ने हदम्याद कति तोकिएको छ?", "options": ["३ महिना", "३५ दिन", "६ महिना"], "ans": "६ महिना", "hint": "सम्पत्ति बिक्री भएको थाहा पाएको मितिबाट निश्चित महिनाभित्र अदालत जानुपर्छ।"},
        {"q": "१०. देवानी संहिता अनुसार कति वर्षभन्दा कम उमेरका बालबालिकाले गरेको मञ्जुरीलाई कानुनतः मञ्जुरी मानिँदैन?", "options": ["१६ वर्ष", "१४ वर्ष", "१८ वर्ष"], "ans": "१८ वर्ष", "hint": "साबालक नभएसम्म कानुनी रूपमा आफैँ पूर्ण मञ्जुरी दिने अधिकार हुँदैन।"}
    ]
}

# ७. मुख्य सञ्चालन भाग
if topic == "गृहपृष्ठ (Home)":
    st.subheader("🏠 शिक्षालय क्विजमा स्वागत छ!")
    st.write("देब्रेपट्टिको मेनु बारबाट आफू अनुकूलको विषय रोज्नुहोस् र कतिवटा प्रश्नको परीक्षा दिने हो सो पनि चयन गर्नुहोस्।")
    st.info("📊 **नयाँ सुविधाहरू:** अब आफूले चाहेको प्रश्न संख्या रोज्न र परीक्षाको बिचमै **Finish Quiz** गरी मार्कसिट निकाल्न सकिन्छ।")

elif topic in raw_quiz_data:
    # छानिएको संख्या अनुसार प्रश्नहरू फिल्टर गर्ने (यदि डेटाबेसमा प्रश्न संख्या कम भए उपलब्ध भएसम्म मिलाउने)
    limit = st.session_state["num_questions_selected"]
    questions = raw_quiz_data[topic][:limit]
    total_qs = len(questions)
    
    if st.session_state["start_time"] is None:
        st.session_state["start_time"] = time.time()
        
    current_idx = st.session_state["current_question"]
    
    # --- क) मार्कसिट डिस्प्ले खण्ड (यदि सबै प्रश्न सकिए वा बीचमै सिध्याएमा) ---
    if current_idx >= total_qs or st.session_state["quiz_finished"]:
        st.balloons()
        st.success("🎉 परीक्षा समाप्त भयो। तल तपाईंको डिजिटल शैक्षिक प्रतिवेदन तयार छ।")
        
        if st.session_state["total_time_taken"] == 0:
            st.session_state["total_time_taken"] = round(time.time() - st.session_state["start_time"])
            
        elapsed_time = st.session_state["total_time_taken"]
        mins = elapsed_time // 60
        secs = elapsed_time % 60
        
        # हालसम्म हल गरेका मध्येको स्कोर प्रतिशत गणना
        correct_ans = st.session_state["score"]
        # बीचमै सिध्याउँदा जतिवटा प्रश्न पुगेको थियो, त्यतिलाई वा कुललाई कुल मान्ने
        attempted_qs = current_idx if current_idx <= total_qs else total_qs
        if attempted_qs == 0: attempted_qs = 1 # Division by zero रोक्न
        
        wrong_ans = attempted_qs - correct_ans
        unanswered = total_qs - attempted_qs
        
        percentage = round((correct_ans / total_qs) * 100, 2)
        result_status = " उत्तीर्ण (PASSED) ✅" if percentage >= 40 else "अनुत्तीर्ण (FAILED) ❌"
        status_color = "#2ecc71" if percentage >= 40 else "#e74c3c"

        st.markdown(f"""
        <div style="background-color: white; padding: 25px; border-radius: 12px; border-top: 8px solid #1e3c72; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h2 style="text-align: center; color: #1e3c72; margin-bottom: 5px;">📜 शिक्षालय परीक्षा मार्कसिट</h2>
            <p style="text-align: center; color: #555; font-size: 1rem; margin-top: 0;">डिजिटल शैक्षिक प्रतिवेदन</p>
            <hr>
            <table class="marksheet-table">
                <tr><th>विवरण (Particulars)</th><th>नतिजा विवरण (Details)</th></tr>
                <tr><td>📋 <b>परीक्षाको विषय (Subject):</b></td><td>{topic}</td></tr>
                <tr><td>❓ <b>कुल प्रश्न संख्या (Total Custom Qs):</b></td><td>{total_qs} वटा</td></tr>
                <tr><td>✅ <b>सही उत्तर (Correct Answers):</b></td><td style="color: #2ecc71; font-weight: bold;">{correct_ans}</td></tr>
                <tr><td>❌ <b>गलत उत्तर (Wrong Answers):</b></td><td style="color: #e74c3c; font-weight: bold;">{wrong_ans}</td></tr>
                <tr><td>⏳ <b>लागेको कुल समय (Time Taken):</b></td><td><b>{mins} मिनेट {secs} सेकेन्ड</b></td></tr>
                <tr><td>📈 <b>प्राप्त प्रतिशत (Percentage):</b></td><td><b>{percentage}%</b></td></tr>
                <tr><td>📊 <b>नतिजा (Final Result):</b></td><td style="color: {status_color}; font-weight: bold; font-size: 1.2rem;">{result_status}</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("🔄 पुनः परीक्षा दिनुहोस् (Restart Quiz)"):
            reset_quiz()
            st.rerun()
            
    # --- ख) प्रश्नोत्तर र सजीव घडी खण्ड ---
    else:
        q_item = questions[current_idx]
        
        # शीर्ष दायाँ/बायाँ सन्तुलन मिलाउन कोलम विभाजन
        col_title, col_finish = st.columns([3, 1])
        with col_title:
            st.subheader(f"📝 {topic} (प्रश्न {current_idx + 1} / {total_qs})")
        with col_finish:
            # बीचमै परीक्षा सिध्याउने रातो बटन
            if st.button("🛑 Finish Quiz", help="परीक्षा बीचमै रोकेर नतिजा हेर्नुहोस्"):
                st.session_state["quiz_finished"] = True
                st.session_state["total_time_taken"] = round(time.time() - st.session_state["start_time"])
                st.rerun()

        st.progress((current_idx) / total_qs)
        
        # --- HTML/JS आधारित सजीव घडी (भिडियो रेकर्डिङका लागि १००% स्मूथ) ---
        # यसले सर्भर रिरन बिना नै स्क्रिनमा सेकेन्ड-सेकेन्डको टिक-टिक देखाउँछ
        elapsed_init = round(time.time() - st.session_state["start_time"])
        st.markdown(
            f"""
            <div style="background: #eef2f7; padding: 10px 15px; border-radius: 6px; display: inline-block; margin-bottom: 15px;">
                ⏱️ <b>चालु समय:</b> <span id="live-timer" style="font-family: monospace; font-weight: bold; color: #1e3c72;">00:00</span>
            </div>
            <script>
                (function() {{
                    var startTime = Date.now() - ({elapsed_init} * 1000);
                    function updateTimer() {{
                        var diff = Date.now() - startTime;
                        var totalSecs = Math.floor(diff / 1000);
                        var mins = Math.floor(totalSecs / 60);
                        var secs = totalSecs % 60;
                        var display = (mins < 10 ? "0" + mins : mins) + " मिनेट " + (secs < 10 ? "0" + secs : secs) + " सेकेन्ड";
                        var el = document.getElementById("live-timer");
                        if (el) el.innerHTML = display;
                    }}
                    if (window.quizTimer) clearInterval(window.quizTimer);
                    window.quizTimer = setInterval(updateTimer, 1000);
                    updateTimer();
                }})();
            </script>
            """,
            unsafe_allow_html=True
        )
        
        user_choice = st.radio(q_item["q"], q_item["options"], key=f"q_{topic}_{current_idx}")
        
        st.write("")
        
        # उत्तर जाँच गर्ने मुख्य प्रक्रिया
        if not st.session_state["answered"]:
            if st.button("✔️ उत्तर जाँच्नुहोस्"):
                st.session_state["answered"] = True
                if user_choice == q_item["ans"]:
                    st.session_state["score"] += 1
                    st.success("🎉 सही उत्तर!")
                else:
                    st.error(f"❌ गलत उत्तर! सही उत्तर: **{q_item['ans']}** हो।")
                st.info(f"ℹ️ **व्याख्या / सङ्केत:** {q_item['hint']}")
                
                # ३ सेकेन्डको काउन्टडाउन बोर्ड देखाएर स्वचालित परिवर्तन गर्ने
                countdown_placeholder = st.empty()
                for i in range(3, 0, -1):
                    countdown_placeholder.warning(f"⏳ {i} सेकेन्डपछि प्रणाली आफैँ अर्को प्रश्नमा जाँदैछ...")
                    time.sleep(1)
                
                countdown_placeholder.empty()
                st.session_state["current_question"] += 1
                st.session_state["answered"] = False
                st.rerun()
        else:
            # सुरक्षित स्टेट ब्याकअप डिस्प्ले (यदि कतै पेज अड्किएमा)
            if user_choice == q_item["ans"]:
                st.success("🎉 सही उत्तर!")
            else:
                st.error(f"❌ गलत उत्तर! सही उत्तर: **{q_item['ans']}** हो।")
            st.info(f"ℹ️ **व्याख्या / सङ्केत:** {q_item['hint']}")
            
            st.session_state["current_question"] += 1
            st.session_state["answered"] = False
            st.rerun()
                
        st.markdown(f"⚙️ **हालको स्कोर: {st.session_state['score']} / {total_qs}**")
