import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import base64
from io import BytesIO

# --- Page Config ---
st.set_page_config(
    page_title="PersonaSynth | Interview Assistant",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Enhanced CSS ---
st.markdown("""
    <style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    section[data-testid="stSidebar"] {
        background-color: #15803d; 
        color: #14532d;
    }
    section[data-testid="stSidebar"] .css-1d391kg {
        color: black;
        font-weight: bold;
    }
    
    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        min-height: 100vh;
    }
    
    body {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #f8fafc;
    }
    
    /* Hero section */
    .hero-container {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 100%);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 48px 32px;
        margin: 32px auto;
        max-width: 1000px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(148, 163, 184, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(21, 128, 61, 0.1) 0%, rgba(22, 163, 74, 0.05) 100%);
        pointer-events: none;
    }
    
    .hero-text {
        text-align: center;
        position: relative;
        z-index: 1;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .hero-title {
        font-size: clamp(32px, 6vw, 56px);
        font-weight: 900;
        color: #f8fafc;
        line-height: 1.1;
        margin-bottom: 24px;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    
    .hero-subtitle {
        font-size: clamp(18px, 3vw, 22px);
        color: #cbd5e1;
        line-height: 1.7;
        margin-bottom: 40px;
        font-weight: 400;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }

    /* Enhanced button styling */
    .button-wrapper {
        display: flex;
        justify-content: center;
        margin: 48px 0;
        position: relative;
        z-index: 1;
    }
    
    .green-btn {
        background: linear-gradient(135deg, #15803d 0%, #16a34a 100%);
        color: white;
        font-size: 20px;
        font-weight: 700;
        padding: 20px 56px;
        border-radius: 16px;
        border: none;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 25px rgba(21, 128, 61, 0.4), 0 4px 12px rgba(0, 0, 0, 0.15);
        text-decoration: none;
        display: inline-block;
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .green-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.6s;
    }
    
    .green-btn:hover::before {
        left: 100%;
    }
    
    .green-btn:hover {
        background: linear-gradient(135deg, #14532d 0%, #15803d 100%);
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 20px 40px rgba(21, 128, 61, 0.5), 0 8px 20px rgba(0, 0, 0, 0.2);
    }
    
    /* Section titles */
    .section-title {
        font-size: clamp(28px, 5vw, 40px);
        font-weight: 800;
        text-align: center;
        margin: 80px 0 48px 0;
        color: #f8fafc;
        position: relative;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -12px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 4px;
        background: linear-gradient(135deg, #15803d 0%, #16a34a 100%);
        border-radius: 2px;
        box-shadow: 0 2px 8px rgba(21, 128, 61, 0.4);
    }
    
    /* Enhanced feature cards */
    .feature-row {
        display: flex;
        align-items: stretch;
        justify-content: center;
        flex-wrap: wrap;
        gap: 32px;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 24px;
    }
    
    .feature-box {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.9) 100%);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        color: #f8fafc;
        padding: 40px 32px;
        flex: 1;
        min-width: 300px;
        max-width: 380px;
        margin: 16px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3), 0 8px 16px rgba(0, 0, 0, 0.2);
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .feature-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(21, 128, 61, 0.1) 0%, rgba(22, 163, 74, 0.05) 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .feature-box:hover {
        transform: translateY(-12px) scale(1.02);
        box-shadow: 0 32px 64px rgba(0, 0, 0, 0.4), 0 16px 32px rgba(21, 128, 61, 0.2);
        border-color: rgba(21, 128, 61, 0.3);
    }
    
    .feature-box:hover::before {
        opacity: 1;
    }
    
    .feature-title {
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 16px;
        color: #f8fafc;
        position: relative;
        z-index: 1;
    }
    
    .feature-description {
        font-size: 16px;
        line-height: 1.6;
        opacity: 0.9;
        color: #cbd5e1;
        position: relative;
        z-index: 1;
    }
    
    /* Logo container */
    .logo-container {
        margin-bottom: 32px;
        transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
    }
    
    .logo-container:hover {
        transform: scale(1.1) rotate(2deg);
    }
    
    /* Enhanced steps section */
    .step-container {
        display: flex;
        flex-direction: row;
        justify-content: center;
        flex-wrap: wrap;
        gap: 40px;
        max-width: 1100px;
        margin: 0 auto;
        padding: 0 24px;
    }
    
    .step-box {
        text-align: center;
        flex: 1;
        min-width: 280px;
        max-width: 320px;
        padding: 32px 24px;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.9) 100%);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        box-shadow: 0 16px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(148, 163, 184, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .step-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(21, 128, 61, 0.1) 0%, rgba(22, 163, 74, 0.05) 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .step-box:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 24px 48px rgba(0, 0, 0, 0.4), 0 12px 24px rgba(21, 128, 61, 0.2);
        border-color: rgba(21, 128, 61, 0.3);
    }
    
    .step-box:hover::before {
        opacity: 1;
    }
    
    .step-circle {
        background: linear-gradient(135deg, #15803d 0%, #16a34a 100%);
        color: white;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 32px;
        font-weight: 900;
        margin: 0 auto 24px auto;
        box-shadow: 0 8px 20px rgba(21, 128, 61, 0.4), 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        z-index: 1;
    }
    
    .step-box:hover .step-circle {
        transform: scale(1.15) rotate(5deg);
        box-shadow: 0 12px 30px rgba(21, 128, 61, 0.5), 0 6px 12px rgba(0, 0, 0, 0.3);
    }
    
    .step-title {
        font-size: 20px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 12px;
        position: relative;
        z-index: 1;
    }
    
    .step-description {
        font-size: 15px;
        color: #cbd5e1;
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }
    
    /* Enhanced animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(40px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .feature-box:nth-child(1) { animation: float 6s ease-in-out infinite; }
    .feature-box:nth-child(2) { animation: float 6s ease-in-out infinite 2s; }
    .feature-box:nth-child(3) { animation: float 6s ease-in-out infinite 4s; }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-container {
            margin: 16px;
            padding: 32px 24px;
        }
        
        .feature-row, .step-container {
            flex-direction: column;
            align-items: center;
            gap: 24px;
        }
        
        .feature-box, .step-box {
            width: 100%;
            max-width: 400px;
            margin: 12px 0;
        }
        
        .section-title {
            margin: 60px 0 32px 0;
        }
    }
    
    /* Footer styling */
    .footer {
        margin-top: 100px;
        padding: 32px 24px;
        border-top: 1px solid rgba(148, 163, 184, 0.2);
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 100%);
        backdrop-filter: blur(20px);
        text-align: center;
    }
    
    .footer-text {
        color: #cbd5e1;
        font-size: 16px;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# --- Text + Logo ---
logo = Image.open("PSlogo.jpeg") 
buffered = BytesIO()
logo.save(buffered, format="PNG")
logo_b64 = base64.b64encode(buffered.getvalue()).decode()

st.markdown(f"""
    <div class="hero-container">
        <div style="text-align: center; margin-bottom: 32px;">
            <img src="data:image/png;base64,{logo_b64}" width="280" class="logo-container" />
        </div>
        <div class="hero-text">
            <div class="hero-title">Prepare Smarter, Interview Better</div>
            <div class="hero-subtitle">
                Whether you're preparing for your first job interview or aiming to level up your career, PersonaSynth empowers you to practice with lifelike AI personas tailored to your industry and role. Our adaptive interview engine provides personalized questions, real-time feedback, and actionable insights—so you can walk into every interview with confidence and clarity.
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- Button ---
st.markdown("""
    <div class="button-wrapper">
         <a href="?nav=InterviewSimulator">
            <button class="green-btn" type="submit">
               Start Your Prep!
            </button>
        </a>
    </div>
""", unsafe_allow_html=True)

if st.query_params.get("nav") == "InterviewSimulator":
    st.switch_page("pages/InterviewSimulator.py")

st.markdown('<div class="section-title">Why Choose PersonaSynth?</div>', unsafe_allow_html=True)
st.markdown('<div class="feature-row">', unsafe_allow_html=True)

features = [
    ("🎯 Smart Question Bank", "Thousands of role-specific questions tailored to your industry and level."),
    ("🤖 AI Mock Interviews", "Realistic simulations with adaptive AI-driven agents."),
    ("📝 Answer Templates", "Use proven response frameworks to structure your answers.")
]

for icon, text in features:
    st.markdown(f'<div class="feature-box"><div class="feature-title">{icon}</div><div class="feature-description">{text}</div></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">How It Works?</div>', unsafe_allow_html=True)
st.markdown('<div class="step-container">', unsafe_allow_html=True)

steps = [
    ("1", "Select a Persona", "Choose your interviewer – recruiter, manager, or expert."),
    ("2", "Practice Interviews", "Respond to adaptive questions in real time."),
    ("3", "Get Feedback", "Review your performance and improve confidently.")
]

for num, title, desc in steps:
    st.markdown(f"""
        <div class="step-box">
            <div class="step-circle">{num}</div>
            <div class="step-title">{title}</div>
            <div class="step-description">{desc}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="footer">
        <div class="footer-text">
        © Developed by Arya Mane and Ameya Phansalkar
        </div>
    </div>
""", unsafe_allow_html=True)