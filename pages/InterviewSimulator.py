import streamlit as st
import importlib
import time
import re
from PIL import Image
import base64
from io import BytesIO

# === Page Config===
st.set_page_config(
    page_title="Interview Simulator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === CSS ===
st.markdown("""
    <style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #15803d; 
        color: #14532d;
    }
    
    section[data-testid="stSidebar"] .css-1d391kg {
        color: black !important;
        font-weight: bold;
    }
    
    /* Enhanced selectbox styling */
    div[data-baseweb="select"] {
        background: white;
        border-radius: 16px;
        padding: 12px 16px;
        border: 2px solid #e2e8f0;
        font-size: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    div[data-baseweb="select"]:hover {
        cursor: pointer;
        border-color: #15803d;
        box-shadow: 0 6px 20px rgba(21, 128, 61, 0.15);
    }
    
    div[data-baseweb="select"] > div {
        color: #1e293b;
        font-weight: 500;
    }
    
    div[data-baseweb="select"] > div:hover {
        color: #15803d;
        cursor: pointer;
    }
    
    /* Logo styling */
    .logo-container {
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    
    .logo-container:hover {
        transform: scale(1.05);
    }
    
    /* Info box styling */
    .info-box {
        background: white;
        padding: 20px 24px;
        border-radius: 16px;
        margin: 20px 0;
        border-left: 4px solid #15803d;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .info-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
    }
    
    .info-title {
        font-weight: 700;
        color: #14532d;
        margin-bottom: 8px;
    }
    
    .info-description {
        color: #64748b;
        line-height: 1.6;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #15803d 0%, #16a34a 100%);
        color: white;
        font-size: 18px;
        font-weight: 600;
        padding: 16px 48px;
        border-radius: 12px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(21, 128, 61, 0.3);
        width: 100%;
        margin: 20px 0;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #14532d 0%, #15803d 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(21, 128, 61, 0.4);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #15803d 0%, #16a34a 100%);
        border-radius: 10px;
    }
    
    /* Chat bubble improvements */
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .round-indicator {
        background: white;
        padding: 16px 24px;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(21, 128, 61, 0.1);
    }
    
    .round-title {
        font-size: 20px;
        font-weight: 700;
        color: #14532d;
        margin-bottom: 12px;
    }
    
    /* Chat input styling */
    .stChatInput > div > div > div > div {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 16px;
        padding: 12px 16px;
        transition: all 0.3s ease;
    }
    
    .stChatInput > div > div > div > div:focus-within {
        border-color: #15803d;
        box-shadow: 0 0 0 3px rgba(21, 128, 61, 0.1);
    }
    
    /* Warning and success messages */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Feedback section */
    .feedback-container {
        background: white;
        padding: 32px;
        border-radius: 20px;
        margin: 24px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(21, 128, 61, 0.1);
    }
    
    .feedback-title {
        font-size: 24px;
        font-weight: 700;
        color: #14532d;
        margin-bottom: 24px;
        text-align: center;
    }
    
    .skill-item {
        margin-bottom: 24px;
        padding: 20px;
        background: #f8fafc;
        border-radius: 12px;
        border-left: 4px solid #15803d;
    }
    
    .skill-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    
    .skill-name {
        font-weight: 600;
        color: #1e293b;
        font-size: 16px;
    }
    
    .skill-score {
        font-size: 14px;
        font-weight: 600;
        color: #64748b;
    }
    
    .progress-bar {
        height: 8px;
        background-color: #e2e8f0;
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: 8px;
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.8s ease-in-out;
    }
    
    .skill-comment {
        font-size: 14px;
        color: #64748b;
        line-height: 1.5;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .chat-container {
            padding: 10px;
        }
        
        .feedback-container {
            padding: 20px;
            margin: 16px 0;
        }
        
        .stButton > button {
            padding: 14px 32px;
            font-size: 16px;
        }
    }
    </style>
""", unsafe_allow_html=True)

logo = Image.open("Synthlogo.png") 
buffered = BytesIO()
logo.save(buffered, format="PNG")
logo_b64 = base64.b64encode(buffered.getvalue()).decode()
st.markdown(f"""
<div style="text-align: right;">
    <a href="/About">
        <img src="data:image/png;base64,{logo_b64}" width="60" class="logo-container" style="cursor:pointer;" />
    </a>
</div>
""", unsafe_allow_html=True)
# === Heuristic AI detection ===
def is_likely_ai_generated(text):
    text = text.strip().lower()
    gpt_starters = ["certainly", "as a", "in conclusion", "to begin with", "firstly", "secondly", "undoubtedly", 
                    "I appreciate the opportunity to answer that.", "I'm glad you brought that up.", 
                    "That’s a great question."]
    formality_flags = ["i would approach", "my methodology", "to summarize", "it is imperative", "in my professional opinion"]
    academic_flair = ["in this context", "moreover", "furthermore", "thus", "therefore"]

    if any(text.startswith(phrase) for phrase in gpt_starters):
        return True
    if any(flag in text for flag in formality_flags + academic_flair):
        return True
    word_count = len(text.split())
    if word_count > 75 and re.search(r'[.,;:]', text) and not re.search(r"\bum\b|\bi guess\b|\bi think\b", text):
        return True
    return False

# === Define industry ===
INDUSTRY_AGENTS = {
    "Tech & Software": {
        "Hiring Manager": "agents.tech.hiring_manager",
        "HR Interviewer": "agents.tech.hr_interviewer",
        "Technical Recruiter": {
            "Python": "agents.tech.technical_recruiter",
            "Java": "agents.tech.technical_recruiter",
            "SQL": "agents.tech.technical_recruiter",
            "C++": "agents.tech.technical_recruiter"
        }
    },
    "Finance": {
        "IB Analyst": "agents.finance.ib_analyst",
        "Financial Advisor": "agents.finance.financial_advisor",
        "Corporate Finance Manager": "agents.finance.corporate_finance_manager"
    },
    "Marketing & Sales": {
        "Sales Executive": "agents.marketing.sales_executive",
        "Brand Manager": "agents.marketing.brand_manager"
    },
    "Healthcare": {
        "Medical School Interviewer": "agents.healthcare.medical_school_interviewer",
        "Hospital Admin": "agents.healthcare.hospital_admin"
    },
    "Education": {
        "Academic Interviewer": "agents.education.academic_interviewer",
        "School Principal": "agents.education.school_principal"
    }
}

AGENT_IDEAL_USERS = {
    "Hiring Manager": "Mid-to-senior software engineers, technical PMs, and product leads.",
    "HR Interviewer": "Candidates prepping for behavioral rounds, fresh grads, career switchers.",
    "Technical Recruiter": "CS undergrads, bootcamp grads, and early-career developers.",
    "IB Analyst": "Undergraduate finance majors, MBAs targeting investment banks.",
    "Financial Advisor": "CFP candidates, finance grads, client-facing retail banking applicants.",
    "Corporate Finance Manager": "MBAs, FP&A analysts, professionals in internal finance roles.",
    "Sales Executive": "Sales reps, business development associates, SDRs/BDRs.",
    "Brand Manager": "Marketing grads, CPG aspirants, early-stage product marketers.",
    "Medical School Interviewer": "Pre-med students, BS/MD applicants, MCAT prep students.",
    "Hospital Admin": "MHA/MBA students, nursing managers, healthcare ops professionals.",
    "Academic Interviewer": "MS/PhD applicants, research assistants, teaching fellows.",
    "School Principal": "Aspiring teachers, K-12 educators, Ed Leadership applicants."
}

# === Session State Setup ===
for key, val in {
    "history": [], "current_prompt": None, "current_agent": None,
    "turn": 0, "started": False, "feedback": None, "active_key": ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# === No of Rounds ===
MAX_TURNS = 6

# === Industry and Agent Selection ===
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        industry = st.selectbox(
            "Industry",
            options=list(INDUSTRY_AGENTS.keys()),
            format_func=lambda x: {
                "Tech & Software": "Technology",
                "Finance": "Finance",
                "Marketing & Sales": "Marketing & Sales",
                "Healthcare": "Healthcare",
                "Education": "Education"
            }.get(x, str(x))
        )
    agents = INDUSTRY_AGENTS[industry]

    with col2:
        agent_options = list(agents.keys())
        selected_agent = st.selectbox(
            "Interviewer",
            options=agent_options,
            format_func=lambda x: str(x)
        )

# === Sub agents for languages ===
if isinstance(agents[selected_agent], dict):
    subroles = list(agents[selected_agent].keys())
    selected_subrole = st.selectbox("Select Specialization", subroles)
    module_path = agents[selected_agent][selected_subrole]
    agent_module = importlib.import_module(module_path)
    agent = agent_module.TechnicalRecruiter(language=selected_subrole)
else:
    selected_subrole = ""
    module_path = agents[selected_agent]
    agent_module = importlib.import_module(module_path)
    agent = getattr(agent_module, module_path.split('.')[-1])

# === Ideal Candidate Info ===
ideal_user_desc = AGENT_IDEAL_USERS.get(selected_agent)
if ideal_user_desc:
    st.markdown(f"""
    <div class="info-box">
        <div class="info-title">💡 Ideal Candidates</div>
        <div class="info-description">{ideal_user_desc}</div>
    </div>
    """, unsafe_allow_html=True)

# === Reset session state on agent change ===
new_key = f"{industry}-{selected_agent}-{selected_subrole}"
if st.session_state.active_key != new_key:
    st.session_state.active_key = new_key
    for key in ["history", "current_prompt", "current_agent", "turn", "started", "feedback"]:
        st.session_state[key] = [] if key == "history" else 0 if key == "turn" else None if key == "feedback" else False
        
# === Start Interview Button ===
with st.container():
    clicked = st.button("Start Your Interview!", key="start")

    if "started" not in st.session_state:
        st.session_state.started = False

    if not st.session_state.started and clicked:
        st.session_state.started = True
        first_q = agent.ask_question([])
        st.session_state.history.append({
            "agent": agent.name,
            "question": first_q,
            "user": ""
        })
# === Chat Interface ===
if st.session_state.started:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    def chat_bubble(content, sender, color, align_right=False):
        tail = f"""
            content: \"\";
            position: absolute;
            top: 12px;
            {'left' if not align_right else 'right'}: -12px;
            width: 0;
            height: 0;
            border: 8px solid transparent;
            border-{'right' if not align_right else 'left'}-color: {color};
        """
        align = "margin-left: auto;" if align_right else "margin-right: auto;"
        return f"""
            <div style='{align} max-width: 70%; display: flex; flex-direction: column;'>
                <div style='position: relative; padding: 16px 20px; margin: 8px; border-radius: 20px; background: {color}; color: white; font-size: 15px; font-weight: 400; box-shadow: 0 4px 12px rgba(0,0,0,0.15); line-height: 1.5;'>
                    <div style='font-weight: 600; margin-bottom: 8px; opacity: 0.9;'>{sender}</div>
                    <div>{content}</div>
                    <div style='{tail}'></div>
                </div>
            </div>
        """

    agent_color = "linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%)"
    user_color = "linear-gradient(135deg, #15803d 0%, #16a34a 100%)"

    num_completed = len([m for m in st.session_state.history if m["user"]])
    current_round = num_completed + 1
    
    st.markdown(f"""
    <div class="round-indicator">
        <div class="round-title">Round {min(current_round, MAX_TURNS)} of {MAX_TURNS}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(min(current_round, MAX_TURNS) / MAX_TURNS)

    for turn in st.session_state.history:
        if turn["question"]:
            st.markdown(chat_bubble(turn["question"], turn["agent"], agent_color, align_right=False), unsafe_allow_html=True)
        if turn["user"]:
            st.markdown(chat_bubble(turn["user"], "🧑 You", user_color, align_right=True), unsafe_allow_html=True)

    if num_completed < MAX_TURNS:
        user_input = st.chat_input("Your response")
        if user_input:
            ai_flag = is_likely_ai_generated(user_input)
            st.session_state.history[-1]["user"] = user_input
            st.markdown(chat_bubble(user_input, "🧑 You", user_color, align_right=True), unsafe_allow_html=True)
            if ai_flag:
                st.warning("⚠️ This response seems overly formal or AI-generated. Try answering more naturally for better feedback.")
            with st.spinner("Agent is typing..."):
                time.sleep(5.0)

            if num_completed + 1 < MAX_TURNS:
                new_q = agent.ask_question(st.session_state.history)
                st.session_state.history.append({
                    "agent": agent.name,
                    "question": new_q,
                    "user": ""
                })
            else:
                st.session_state.history.append({
                    "agent": agent.name,
                    "question": "Thank you for that thoughtful response. I really appreciate the way you articulated your experience. That concludes our interview today. Wishing you the very best ahead!",
                    "user": ""
                })
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
# === Interview Completion & Feedback ===
    elif num_completed == MAX_TURNS:
        st.success("🎉 Interview Complete! Great job!")

        if st.session_state.feedback is None:
            if st.button("📊 Get Detailed Feedback"):
                from feedback_evaluator import evaluator
                full_transcript = "\n".join(
                    [f"{m['agent']}: {m['question']}\nUser: {m['user']}" for m in st.session_state.history]
                )
                with st.spinner("🔍 Analyzing your performance..."):
                    st.session_state.feedback = evaluator.evaluate(full_transcript)

        if isinstance(st.session_state.feedback, dict):
            st.markdown("""
            <div class="feedback-container">
                <div class="feedback-title">📈 Your Interview Performance</div>
            """, unsafe_allow_html=True)
            
            for skill, value in st.session_state.feedback.items():
                if skill == "Summary":
                    continue
                if isinstance(value, (list, tuple)) and len(value) == 2:
                    score, comment = value
                    color = '#e63946' if score < 5 else '#15803d' if score >= 7 else '#f59e0b'
                    st.markdown(f"""
                    <div class="skill-item">
                        <div class="skill-header">
                            <div class="skill-name">{skill}</div>
                            <div class="skill-score">{score}/10</div>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {score * 10}%; background: {color};"></div>
                        </div>
                        <div class="skill-comment">{comment}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("### 📝 Overall Summary")
            summary = st.session_state.feedback.get("Summary", "No summary available.")
            st.info(summary)

        elif st.session_state.feedback:
            st.markdown("### 📊 Interview Feedback")
            st.markdown(st.session_state.feedback)

        if st.button("🔄 Restart Interview", help="Click to start over"):
            for key in ["history", "current_prompt", "current_agent", "turn", "started", "feedback"]:
                if key == "history":
                    st.session_state[key] = []
                elif key == "turn":
                    st.session_state[key] = 0
                elif key == "feedback":
                    st.session_state[key] = None
                else:
                    st.session_state[key] = False
            st.rerun()
 