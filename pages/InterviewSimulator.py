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

# === Modern Minimal CSS ===
st.markdown("""
    <style>
    /* Reset and base styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Main app styling */
    .stApp {
        background: #ffffff;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #1a1a1a;
    }
    
    /* Header */
    .header {
        padding: 1rem 2rem;
        background: white;
        border-bottom: 1px solid #e2e8f0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .logo {
        width: 40px;
        height: auto;
        cursor: pointer;
        opacity: 0.8;
        transition: opacity 0.2s ease;
    }
    
    .logo:hover {
        opacity: 1;
    }
    
    /* Main container */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    /* Setup section */
    .setup-section {
        background: #f8fafc;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid #e2e8f0;
    }
    
    .setup-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Enhanced selectbox styling */
    .stSelectbox > div > div {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        transition: all 0.2s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #cbd5e1;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #0f172a;
        box-shadow: 0 0 0 3px rgba(15, 23, 42, 0.1);
    }
    
    /* Info box styling */
    .info-box {
        background: #eff6ff;
        border: 1px solid #dbeafe;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #3b82f6;
    }
    
    .info-title {
        font-weight: 600;
        color: #1e40af;
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
    }
    
    .info-description {
        color: #1e40af;
        line-height: 1.5;
        font-size: 0.9rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: #0f172a;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s ease;
        width: 100%;
        margin: 1rem 0;
    }
    
    .stButton > button:hover {
        background: #1e293b;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
    }
    
    /* Chat container */
    .chat-container {
        background: white;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        overflow: hidden;
        margin-top: 2rem;
    }
    
    .chat-header {
        background: #f8fafc;
        padding: 1.5rem 2rem;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .round-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .round-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0f172a;
    }
    
    .round-counter {
        background: #0f172a;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    /* Progress bar */
    .progress-container {
        background: #e2e8f0;
        height: 6px;
        border-radius: 3px;
        overflow: hidden;
    }
    
    .progress-bar {
        background: #0f172a;
        height: 100%;
        border-radius: 3px;
        transition: width 0.3s ease;
    }
    
    /* Chat messages */
    .chat-messages {
        padding: 2rem;
        min-height: 400px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    .message {
        margin-bottom: 1.5rem;
        display: flex;
        gap: 1rem;
    }
    
    .message.user {
        flex-direction: row-reverse;
    }
    
    .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        flex-shrink: 0;
    }
    
    .message-avatar.agent {
        background: #eff6ff;
        color: #3b82f6;
    }
    
    .message-avatar.user {
        background: #f0fdf4;
        color: #16a34a;
    }
    
    .message-content {
        background: #f8fafc;
        padding: 1rem 1.25rem;
        border-radius: 16px;
        max-width: 70%;
        border: 1px solid #e2e8f0;
        line-height: 1.5;
    }
    
    .message.user .message-content {
        background: #f0fdf4;
        border-color: #dcfce7;
    }
    
    .message-sender {
        font-size: 0.8rem;
        font-weight: 600;
        color: #64748b;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Chat input */
    .stChatInput > div {
        border-top: 1px solid #e2e8f0;
        background: #f8fafc;
        padding: 1rem 2rem;
    }
    
    .stChatInput input {
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.2s ease;
    }
    
    .stChatInput input:focus {
        border-color: #0f172a;
        box-shadow: 0 0 0 3px rgba(15, 23, 42, 0.1);
        outline: none;
    }
    
    /* Success and warning messages */
    .stSuccess {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 12px;
        color: #166534;
    }
    
    .stWarning {
        background: #fffbeb;
        border: 1px solid #fed7aa;
        border-radius: 12px;
        color: #92400e;
    }
    
    /* Feedback section */
    .feedback-container {
        background: #f8fafc;
        border-radius: 16px;
        padding: 2rem;
        margin-top: 2rem;
        border: 1px solid #e2e8f0;
    }
    
    .feedback-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .skill-item {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
    }
    
    .skill-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .skill-name {
        font-weight: 600;
        color: #0f172a;
    }
    
    .skill-score {
        background: #0f172a;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .skill-progress {
        background: #e2e8f0;
        height: 8px;
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: 0.75rem;
    }
    
    .skill-progress-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.8s ease;
    }
    
    .skill-comment {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-container {
            padding: 1rem;
        }
        
        .setup-section {
            padding: 1.5rem;
        }
        
        .chat-messages {
            padding: 1rem;
        }
        
        .message-content {
            max-width: 85%;
        }
        
        .round-info {
            flex-direction: column;
            gap: 1rem;
            align-items: flex-start;
        }
    }
    
    /* Scrollbar styling */
    .chat-messages::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 3px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    </style>
""", unsafe_allow_html=True)

# === Header ===
logo = Image.open("Synthlogo.png") 
buffered = BytesIO()
logo.save(buffered, format="PNG")
logo_b64 = base64.b64encode(buffered.getvalue()).decode()

st.markdown(f"""
<div class="header">
    <div></div>
    <a href="/About">
        <img src="data:image/png;base64,{logo_b64}" class="logo" />
    </a>
</div>
""", unsafe_allow_html=True)

# === Heuristic AI detection ===
def is_likely_ai_generated(text):
    text = text.strip().lower()
    gpt_starters = ["certainly", "as a", "in conclusion", "to begin with", "firstly", "secondly", "undoubtedly", 
                    "I appreciate the opportunity to answer that.", "I'm glad you brought that up.", 
                    "That's a great question."]
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

# === Main Container ===
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# === Setup Section ===
st.markdown("""
<div class="setup-section">
    <h2 class="setup-title">🎯 Interview Setup</h2>
</div>
""", unsafe_allow_html=True)

# === Industry and Agent Selection ===
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        industry = st.selectbox(
            "Select Industry",
            options=list(INDUSTRY_AGENTS.keys()),
            format_func=lambda x: {
                "Tech & Software": "💻 Technology",
                "Finance": "💰 Finance",
                "Marketing & Sales": "📈 Marketing & Sales",
                "Healthcare": "🏥 Healthcare",
                "Education": "🎓 Education"
            }.get(x, str(x))
        )
    agents = INDUSTRY_AGENTS[industry]

    with col2:
        agent_options = list(agents.keys())
        selected_agent = st.selectbox(
            "Choose Interviewer",
            options=agent_options,
            format_func=lambda x: f"👤 {str(x)}"
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
        <div class="info-title">💡 Ideal for</div>
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
    clicked = st.button("🚀 Start Interview", key="start")

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
    num_completed = len([m for m in st.session_state.history if m["user"]])
    current_round = num_completed + 1
    progress = min(current_round, MAX_TURNS) / MAX_TURNS * 100
    
    st.markdown(f"""
    <div class="chat-container">
        <div class="chat-header">
            <div class="round-info">
                <div class="round-title">Interview in Progress</div>
                <div class="round-counter">Round {min(current_round, MAX_TURNS)} of {MAX_TURNS}</div>
            </div>
            <div class="progress-container">
                <div class="progress-bar" style="width: {progress}%"></div>
            </div>
        </div>
        <div class="chat-messages">
    """, unsafe_allow_html=True)

    # Display messages
    for turn in st.session_state.history:
        if turn["question"]:
            st.markdown(f"""
            <div class="message agent">
                <div class="message-avatar agent">🤖</div>
                <div class="message-content">
                    <div class="message-sender">{turn['agent']}</div>
                    {turn["question"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        if turn["user"]:
            st.markdown(f"""
            <div class="message user">
                <div class="message-avatar user">👤</div>
                <div class="message-content">
                    <div class="message-sender">You</div>
                    {turn["user"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # Chat input
    if num_completed < MAX_TURNS:
        user_input = st.chat_input("Type your response here...")
        if user_input:
            ai_flag = is_likely_ai_generated(user_input)
            st.session_state.history[-1]["user"] = user_input
            
            if ai_flag:
                st.warning("⚠️ This response seems overly formal. Try answering more naturally for better feedback.")
            
            with st.spinner("🤖 Interviewer is thinking..."):
                time.sleep(2.0)

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
                    "question": "Thank you for that thoughtful response. That concludes our interview today. Best of luck!",
                    "user": ""
                })
            st.rerun()
    
    # Interview completion
    elif num_completed == MAX_TURNS:
        st.success("🎉 Interview Complete! Great job!")

        if st.session_state.feedback is None:
            if st.button("📊 Get Performance Analysis"):
                from feedback_evaluator import evaluator
                full_transcript = "\n".join(
                    [f"{m['agent']}: {m['question']}\nUser: {m['user']}" for m in st.session_state.history]
                )
                with st.spinner("🔍 Analyzing your performance..."):
                    st.session_state.feedback = evaluator.evaluate(full_transcript)

        if isinstance(st.session_state.feedback, dict):
            st.markdown("""
            <div class="feedback-container">
                <div class="feedback-title">📈 Performance Analysis</div>
            """, unsafe_allow_html=True)
            
            for skill, value in st.session_state.feedback.items():
                if skill == "Summary":
                    continue
                if isinstance(value, (list, tuple)) and len(value) == 2:
                    score, comment = value
                    color = '#dc2626' if score < 5 else '#16a34a' if score >= 7 else '#f59e0b'
                    st.markdown(f"""
                    <div class="skill-item">
                        <div class="skill-header">
                            <div class="skill-name">{skill}</div>
                            <div class="skill-score">{score}/10</div>
                        </div>
                        <div class="skill-progress">
                            <div class="skill-progress-fill" style="width: {score * 10}%; background: {color};"></div>
                        </div>
                        <div class="skill-comment">{comment}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
            
            summary = st.session_state.feedback.get("Summary", "No summary available.")
            st.info(f"**Overall Summary:** {summary}")

        if st.button("🔄 Start New Interview"):
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

st.markdown('</div>', unsafe_allow_html=True)