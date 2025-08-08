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

# --- CSS ---
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
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    body {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hero section */
    .hero-text {
        text-align: left;
        width: auto;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .hero-title {
        font-size: clamp(28px, 5vw, 42px);
        font-weight: 800;
        color: #14532d;
        line-height: 1.2;
        margin-bottom: 16px;
        background: linear-gradient(135deg, #14532d 0%, #15803d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-size: clamp(16px, 2.5vw, 20px);
        color: #64748b;
        line-height: 1.6;
        margin-bottom: 32px;
        font-weight: 400;
    }

    /* Button styling */
    .button-wrapper {
        display: flex;
        justify-content: center;
        margin: 40px 0;
    }
    
    .green-btn {
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
        text-decoration: none;
        display: inline-block;
    }
    
    .green-btn:hover {
        background: linear-gradient(135deg, #14532d 0%, #15803d 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(21, 128, 61, 0.4);
    }
    
    /* Section titles */
    .section-title {
        font-size: clamp(24px, 4vw, 32px);
        font-weight: 700;
        text-align: center;
        margin: 60px 0 40px 0;
        color: #14532d;
        position: relative;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: linear-gradient(135deg, #15803d 0%, #16a34a 100%);
        border-radius: 2px;
    }
    
    /* Feature cards */
    .feature-row {
        display: flex;
        align-items: stretch;
        justify-content: center;
        flex-wrap: wrap;
        gap: 24px;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    .feature-box {
        background: linear-gradient(135deg, #15803d 0%, #16a34a 100%);
        border-radius: 16px;
        color: white;
        padding: 32px 24px;
        flex: 1;
        min-width: 280px;
        max-width: 350px;
        margin: 12px;
        box-shadow: 0 8px 32px rgba(21, 128, 61, 0.2);
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .feature-box:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(21, 128, 61, 0.3);
    }
    
    .feature-box:hover::before {
        opacity: 1;
    }
    
    .feature-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 12px;
        color: white;
    }
    
    .feature-description {
        font-size: 16px;
        line-height: 1.5;
        opacity: 0.95;
    }
    
    /* Logo container */
    .logo-container {
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    
    .logo-container:hover {
        transform: scale(1.05);
    }
    
    /* Steps section */
    .step-container {
        display: flex;
        flex-direction: row;
        justify-content: center;
        flex-wrap: wrap;
        gap: 32px;
        max-width: 1000px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    .step-box {
        text-align: center;
        flex: 1;
        min-width: 250px;
        max-width: 300px;
        padding: 24px;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        border: 1px solid rgba(21, 128, 61, 0.1);
    }
    
    .step-box:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
        border-color: rgba(21, 128, 61, 0.2);
    }
    
    .step-circle {
        background: linear-gradient(135deg, #15803d 0%, #16a34a 100%);
        color: white;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 24px;
        font-weight: 700;
        margin: 0 auto 20px auto;
        box-shadow: 0 4px 15px rgba(21, 128, 61, 0.3);
        transition: all 0.3s ease;
    }
    
    .step-box:hover .step-circle {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(21, 128, 61, 0.4);
    }
    
    .step-title {
        font-size: 18px;
        font-weight: 700;
        color: #14532d;
        margin-bottom: 8px;
    }
    
    .step-description {
        font-size: 14px;
        color: #64748b;
        line-height: 1.5;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .feature-row, .step-container {
            flex-direction: column;
            align-items: center;
        }
        
        .feature-box, .step-box {
            width: 100%;
            max-width: 400px;
            margin: 12px 0;
        }
        
        .hero-title {
            text-align: center;
        }
        
        .hero-subtitle {
            text-align: center;
        }
    }
    
    /* Footer styling */
    .footer {
        margin-top: 80px;
        padding: 20px;
        border-top: 1px solid rgba(21, 128, 61, 0.1);
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
    }
    </style>
""", unsafe_allow_html=True)

# --- Text + Logo ---
logo = Image.open("PSlogo.jpeg") 
buffered = BytesIO()
logo.save(buffered, format="PNG")
logo_b64 = base64.b64encode(buffered.getvalue()).decode()

st.markdown(f"""
    <div style="text-align: center; margin-top: 20px;">
        <img src="data:image/png;base64,{logo_b64}" width="250" class="logo-container" />
        <div class="hero-text" style="max-width: 800px; margin: 0 auto; text-align: center;">
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
    ("Smart Question Bank", "Thousands of role-specific questions tailored to your industry and level."),
    ("AI Mock Interviews", "Realistic simulations with adaptive AI-driven agents."),
    ("Answer Templates", "Use proven response frameworks to structure your answers.")
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
        <div style='text-align: center; font-size: 0.9em; color: #64748b;'>
        © Developed by Arya Mane and Ameya Phansalkar
        </div>
    </div>
""", unsafe_allow_html=True)
