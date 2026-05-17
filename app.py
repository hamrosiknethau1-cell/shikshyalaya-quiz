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


# --- ३. प्रीमियम र अत्यधिक आकर्षक कलफुल CSS स्टाइल ---
st.markdown(
    """
    <style>
    /* मुख्य ब्याकग्राउन्ड */
    .stApp { 
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%) !important; 
    }
    
    /* वाटरमार्क */
    .stApp::before {
        content: "SHIKSHYALAYA QUIZ HUB";
        position: fixed; top: 50%; left: 50%;
        transform: translate(-50%, -50%) rotate(-30deg);
        font-size: 6rem; font-weight: 900;
        color: rgba(30, 60, 114, 0.03); z-index: -1;  
        pointer-events: none; white-space: nowrap;
    }
    
    /* शीर्षकहरू */
    h1 { color: #1e3c72 !important; font-weight: 800 !important; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); }
    h2, h3 { color: #2a5298 !important; font-weight: bold !important; }
    
    /* रेडियो बटन (प्रश्नोत्तर विकल्पहरू) स्टाइल */
    div[data-testid="stRadio"] {
        background-color: #ffffff !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        border-left: 5px solid #2a5298 !important;
        margin-bottom: 20px !important;
    }
    div[data-testid="stRadio"] label p {
        font-size: 1.2rem !important; color: #111111 !important; font-weight: 600 !important;
    }
    
    /* बटनहरूको प्रीमियम लुक */
    div.stButton > button {
        background: linear-gradient(to right, #1e3c72, #2a5298) !important;
        color: white !important; border-radius: 8px !important; font-weight: bold !important;
        font-size: 1.05rem !important; padding: 0.6rem 2.2rem !important;
        border: none !important; box-shadow: 0 4px 10px rgba(42, 82, 152, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(42, 82, 152, 0.4) !important;
    }
    
    /* प्रोग्रेस बार */
    div[data-testid="stProgress"] > div > div > div {
        background-color: #2a5298 !important;
    }
    
    /* सजीव घडी बक्स */
    .timer-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: #ffffff !important; padding: 12px 20px; 
        border-radius: 8px; display: inline-block; 
        margin-bottom: 20px; font-weight: bold;
        box-shadow: 0 4px 10px rgba(30, 60, 114, 0.2);
    }
    
    /* मार्कसिट कार्ड डिजाइन */
    .marksheet-card {
        background: #ffffff; padding: 30px; border-radius: 16px; 
        border-top: 10px solid #1e3c72; box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    .marksheet-table {
        width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 1.15rem;
        border-radius: 8px; overflow: hidden;
    }
    .marksheet-table th { background-color: #1e3c72; color: white; text-align: left; padding: 14px; }
    .marksheet-table td { padding: 14px; border-bottom: 1px solid #eeeeee; color: #333333; }
    .marksheet-table tr:nth-child(even) { background-color: #f9fbfd; }
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

# प्रश्न संख्या रोज्ने व्यवस्था
if topic != "गृहपृष्ठ (Home)":
    st.session_state["num_questions_selected"] = st.sidebar.selectbox(
        "❓ प्रश्न संख्या छान्नुहोस्:",
        (5, 10, 15, 20),
        index=1,
        disabled=st.session_state["current_question"] > 0 or st.session_state["quiz_finished"]
    )
    st.sidebar.caption("नेाट: परीक्षा सुरु भएपछि प्रश्न संख्या परिवर्तन गर्न मिल्दैन।")

st.sidebar.write("---")
if st.sidebar.button("🔒 लगआउट (Logout)"):
    logout()
    st.rerun()


# ६. प्रश्नहरूको वृहत डाटाबेस
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
        {"q": "१०. स्थानीय तहको व्यवस्थापकीय अधिकार कुन धारामा उल्लेख छ?", "options": ["धारा २२६", "धारा २३०", "धारा २२१"], "ans": "धारा २२१", "hint": "यसले गाउँ सभा र नगर सभाको व्यवस्थापकीय अधिकारलाई सुनिश्चित गर्छ।"}
    ],
    "सैनिक ऐन, २०६३": [
        {"q": "१. सैनिक ऐन, २०६३ प्रमाणीकरण कहिले भएको हो?", "options": ["२०६३ कार्तिक २३", "२०६३ मंसिर २३", "२०६३ पुस २३"], "ans": "२०६३ मंसिर २३", "hint": "यो ऐन तत्कालीन व्यवस्थापिका-संसदले पारित गरेपछि लालमोहर लागेको हो।"},
        {"q": "२. सैनिक ऐन, २०६३ बमोजिम नेपाली सेनाको नियन्त्रण, प्रयोग र व्यवस्थापन कसले गर्छ?", "options": ["नेपाल सरकार", "प्रधानसेनापति", "रक्षामन्त्री"], "ans": "नेपाल सरकार", "hint": "ऐनको धारा ४ बमोजिम यो अधिकार मन्त्रिपरिषद्मा निहित हुन्छ।"},
        {"q": "३. सैनिक ऐन, २०६३ मा कति परिच्छेदहरू रहेका छन्?", "options": ["१५ वटा", "१३ वटा", "१० वटा"], "ans": "१३ वटा", "hint": "यस ऐनमा सैनिक अदालत, अनुशासन र सेवा सर्त सम्बन्धी व्यवस्थाहरू समेटिएका छन्।"},
        {"q": "४. राष्ट्रिय सुरक्षा परिषद्को अध्यक्ष को हुने संवैधानिक / कानुनी व्यवस्था छ?", "options": ["रक्षामन्त्री", "प्रधानसेनापति", "प्रधानमन्त्री"], "ans": "प्रधानमन्त्री", "hint": "सेना परिचालनको सिफारिस गर्ने यो उच्च निकायको नेतृत्व देशको कार्यकारी प्रमुखले गर्छन्।"},
        {"q": "५. सैनिक ऐन अनुसार प्रधानसेनापतिको पदावधि कति वर्षको हुनेछ?", "options": ["३ वर्ष", "४ वर्ष", "५ वर्ष"], "ans": "३ वर्ष", "hint": "धारा १४ अनुसार प्रधानसेनापति आफ्नो पदमा निश्चित अवधिसम्म मात्र रहन पाउँछन्।"}
    ],
    "मुलुकी देवानी संहिता": [
        {"q": "१. मुलुकी देवानी संहिता, २०७४ कहिलेदेखि लागू भयो?", "options": ["२०७४ भदौ १ गते", "२०७५ असोज १ गते", "२०७५ भदौ १ गते"], "ans": "२०७५ भदौ १ गते", "hint": "यो कानुन पुरानो मुलुकी ऐन, २०२० लाई प्रतिस्थापन गर्दै लागू भएको हो।"},
        {"q": "२. देवानी संहिता अनुसार कति वर्ष उमेर पूरा भएपछि विवाह गर्न योग्य मानिन्छ?", "options": ["२० वर्ष", "१८ वर्ष", "२१ वर्ष"], "ans": "२० वर्ष", "hint": "नयाँ कानुनी प्रावधानले केटा र केटी दुवैका लागि एउटै उमेर हद तोकेको छ।"},
        {"q": "३. देवानी कानूनको सामान्य सिद्धान्त अन्तर्गत कानूनको अज्ञानता के मानिन्छ?", "options": ["क्षम्य हुन्छ", "क्षम्य हुँदैन", "अदालतको इच्छामा भर पर्छ"], "ans": "क्षम्य हुँदैन", "hint": "'मलाई यो कानुन थाहा थिएन' भनेर कसुर वा दायित्वबाट उम्किन पाइँदैन।"}
    ]
}

# ७. मुख्य सञ्चालन भाग
if topic == "गृहपृष्ठ (Home)":
    st.subheader("🏠 शिक्षालय क्विजमा स्वागत छ!")
    st.write("देब्रेपट्टिको मेनु बारबाट आफू अनुकूलको विषय रोज्नुहोस् र कतिवटा प्रश्नको परीक्षा दिने हो सो पनि चयन गर्नुहोस्।")
    st.info("📊 **मुख्य सुविधाहरू:** अब आफूले चाहेको प्रश्न संख्या रोज्न र परीक्षाको बिचमै **🛑 Finish Quiz** गरी मार्कसिट निकाल्न सकिन्छ।")

elif topic in raw_quiz_data:
    limit = st.session_state["num_questions_selected"]
    questions = raw_quiz_data[topic][:limit]
    total_qs = len(questions)
    
    if st.session_state["start_time"] is None:
        st.session_state["start_time"] = time.time()
        
    current_idx = st.session_state["current_question"]
    
    # --- क) कलफुल मार्कसिट डिस्प्ले खण्ड (Finish Quiz वा प्रश्न समाप्त भएपछि) ---
    if current_idx >= total_qs or st.session_state["quiz_finished"]:
        st.balloons()
        
        if st.session_state["total_time_taken"] == 0:
            st.session_state["total_time_taken"] = round(time.time() - st.session_state["start_time"])
            
        elapsed_time = st.session_state["total_time_taken"]
        mins = elapsed_time // 60
        secs = elapsed_time % 60
        
        correct_ans = st.session_state["score"]
        attempted_qs = current_idx if current_idx <= total_qs else total_qs
        if attempted_qs == 0: attempted_qs = 1 
        
        wrong_ans = attempted_qs - correct_ans
        percentage = round((correct_ans / total_qs) * 100, 2)
        
        result_status = " उत्तीर्ण (PASSED) ✅" if percentage >= 40 else "अनुत्तीर्ण (FAILED) ❌"
        status_color = "#2ecc71" if percentage >= 40 else "#e74c3c"

        # प्रिमियम एचटीएमएल कार्ड मार्कसिट
        st.markdown(f"""
        <div class="marksheet-card">
            <h2 style="text-align: center; color: #1e3c72; margin-bottom: 5px;">📜 शिक्षालय परीक्षा मार्कसिट</h2>
            <p style="text-align: center; color: #666; font-size: 1rem; margin-top: 0;">डिजिटल शैक्षिक प्रतिवेदन</p>
            <hr style="border: 0; border-top: 1px solid #eee;">
            <table class="marksheet-table">
                <tr><th>विवरण (Particulars)</th><th>नतिजा विवरण (Details)</th></tr>
                <tr><td>📋 <b>परीक्षाको विषय (Subject):</b></td><td><b>{topic}</b></td></tr>
                <tr><td>❓ <b>कुल प्रश्न संख्या (Total Questions):</b></td><td>{total_qs} वटा</td></tr>
                <tr><td>✅ <b>सही उत्तर (Correct Answers):</b></td><td style="color: #2ecc71; font-weight: bold;">{correct_ans}</td></tr>
                <tr><td>❌ <b>गलत उत्तर (Wrong Answers):</b></td><td style="color: #e74c3c; font-weight: bold;">{wrong_ans}</td></tr>
                <tr><td>⏳ <b>लागेको कुल समय (Time Taken):</b></td><td><b>{mins} मिनेट {secs} सेकेन्ड</b></td></tr>
                <tr><td>📈 <b>प्राप्त प्रतिशत (Percentage):</b></td><td><b>{percentage}%</b></td></tr>
                <tr><td>📊 <b>नतिजा (Final Result):</b></td><td style="color: {status_color}; font-weight: bold; font-size: 1.25rem;">{result_status}</td></tr>
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
        
        col_title, col_finish = st.columns([3, 1.2])
        with col_title:
            st.subheader(f"📝 {topic} (प्रश्न {current_idx + 1} / {total_qs})")
        with col_finish:
            # बीचमै परीक्षा सिध्याउने रातो ब्याकग्राउन्डयुक्त बटन स्टाइल
            st.write("<div style='text-align: right;'>", unsafe_allow_html=True)
            if st.button("🛑 Finish Quiz", help="परीक्षा बीचमै रोकेर नतिजा हेर्नुहोस्"):
                st.session_state["quiz_finished"] = True
                st.session_state["total_time_taken"] = round(time.time() - st.session_state["start_time"])
                st.rerun()
            st.write("</div>", unsafe_allow_html=True)

        st.progress((current_idx) / total_qs)
        
        # स्मूथ लाइभ घडी बक्स
        elapsed_init = round(time.time() - st.session_state["start_time"])
        st.markdown(
            f"""
            <div class="timer-container">
                ⏳ चालु समय: <span id="live-timer" style="font-family: 'Courier New', monospace;">00:00</span>
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
        
        # प्रश्न र अप्सनहरू
        user_choice = st.radio(q_item["q"], q_item["options"], key=f"q_{topic}_{current_idx}")
        
        st.write("")
        
        # उत्तर जाँच गर्ने मुख्य प्रक्रिया र ३ सेकेन्ड अटो-नेक्स्ट
        if not st.session_state["answered"]:
            if st.button("✔️ उत्तर जाँच्नुहोस्"):
                st.session_state["answered"] = True
                if user_choice == q_item["ans"]:
                    st.session_state["score"] += 1
                    st.success("🎉 सही उत्तर!")
                else:
                    st.error(f"❌ गलत उत्तर! सही उत्तर: **{q_item['ans']}** हो।")
                st.info(f"ℹ️ **व्याख्या / सङ्केत:** {q_item['hint']}")
                
                # काउन्टडाउन बोर्ड देखाएर स्वचालित नेक्स्ट गर्ने
                countdown_placeholder = st.empty()
                for i in range(3, 0, -1):
                    countdown_placeholder.warning(f"⏳ {i} सेकेन्डपछि प्रणाली आफैँ अर्को प्रश्नमा जाँदैछ...")
                    time.sleep(1)
                
                countdown_placeholder.empty()
                st.session_state["current_question"] += 1
                st.session_state["answered"] = False
                st.rerun()
        else:
            if user_choice == q_item["ans"]:
                st.success("🎉 सही उत्तर!")
            else:
                st.error(f"❌ गलत उत्तर! सही उत्तर: **{q_item['ans']}** हो।")
            st.info(f"ℹ️ **व्याख्या / सङ्केत:** {q_item['hint']}")
            
            st.session_state["current_question"] += 1
            st.session_state["answered"] = False
            st.rerun()
                
        st.markdown(f"⚙️ **हालको स्कोर: {st.session_state['score']} / {total_qs}**")
