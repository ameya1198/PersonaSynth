import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import base64
from io import BytesIO

# --- Page Config ---
st.set_page_config(
    page_title="PersonaSynth | AI Interview Simulator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Modern Minimal CSS ---
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
    
    /* Hero section */
    .hero-section {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    .hero-content {
        max-width: 800px;
        margin: 0 auto;
    }
    
    .logo {
        width: 120px;
        height: auto;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    
    .hero-title {
        font-size: clamp(2.5rem, 5vw, 4rem);
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 1.5rem;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: clamp(1.1rem, 2vw, 1.25rem);
        color: #64748b;
        margin-bottom: 3rem;
        line-height: 1.6;
        font-weight: 400;
    }
    
    .cta-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 1rem 2.5rem;
        background: #0f172a;
        color: white;
        text-decoration: none;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.2s ease;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
    }
    
    .cta-button:hover {
        background: #1e293b;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.2);
        color: white;
        text-decoration: none;
    }
    
    /* Features section */
    .features-section {
        padding: 5rem 2rem;
        background: white;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        color: #0f172a;
        margin-bottom: 3rem;
        letter-spacing: -0.02em;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .feature-card {
        padding: 2.5rem 2rem;
        background: #f8fafc;
        border-radius: 16px;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(15, 23, 42, 0.1);
        border-color: #cbd5e1;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 1rem;
    }
    
    .feature-description {
        color: #64748b;
        line-height: 1.6;
    }
    
    /* How it works section */
    .how-it-works {
        padding: 5rem 2rem;
        background: #f8fafc;
    }
    
    .steps-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 3rem;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .step-card {
        text-align: center;
        position: relative;
    }
    
    .step-number {
        width: 60px;
        height: 60px;
        background: #0f172a;
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0 auto 1.5rem;
    }
    
    .step-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 1rem;
    }
    
    .step-description {
        color: #64748b;
        line-height: 1.6;
    }
    
    /* Footer */
    .footer {
        padding: 3rem 2rem;
        background: #0f172a;
        color: #94a3b8;
        text-align: center;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-section {
            padding: 1rem;
        }
        
        .features-section,
        .how-it-works {
            padding: 3rem 1rem;
        }
        
        .features-grid,
        .steps-grid {
            gap: 1.5rem;
        }
        
        .feature-card {
            padding: 2rem 1.5rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- Hero Section ---
logo = Image.open("PSlogo.jpeg") 
buffered = BytesIO()
logo.save(buffered, format="PNG")
logo_b64 = base64.b64encode(buffered.getvalue()).decode()

st.markdown(f"""
    <div class="hero-section">
        <div class="hero-content">
            <img src="data:image/png;base64,{logo_b64}" class="logo" />
            <h1 class="hero-title">Master Your Next Interview</h1>
            <p class="hero-subtitle">
                Practice with AI-powered interview simulations tailored to your industry. 
                Get real-time feedback and build confidence for your dream job.
            </p>
            <a href="?nav=InterviewSimulator" class="cta-button">
                Start Practicing Now
            </a>
        </div>
    </div>
""", unsafe_allow_html=True)

# Handle navigation
if st.query_params.get("nav") == "InterviewSimulator":
    st.switch_page("pages/InterviewSimulator.py")

# --- Features Section ---
st.markdown("""
    <div class="features-section">
        <h2 class="section-title">Why Choose PersonaSynth?</h2>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <h3 class="feature-title">Industry-Specific</h3>
                <p class="feature-description">
                    Practice with interviewers from Tech, Finance, Healthcare, Marketing, and Education sectors.
                </p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <h3 class="feature-title">AI-Powered</h3>
                <p class="feature-description">
                    Realistic conversations with AI agents that adapt to your responses and experience level.
                </p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h3 class="feature-title">Detailed Feedback</h3>
                <p class="feature-description">
                    Get comprehensive performance analysis with scores and actionable improvement suggestions.
                </p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- How It Works Section ---
st.markdown("""
    <div class="how-it-works">
        <h2 class="section-title">How It Works</h2>
        <div class="steps-grid">
            <div class="step-card">
                <div class="step-number">1</div>
                <h3 class="step-title">Choose Your Interviewer</h3>
                <p class="step-description">
                    Select from various industry professionals and specializations.
                </p>
            </div>
            <div class="step-card">
                <div class="step-number">2</div>
                <h3 class="step-title">Practice Interview</h3>
                <p class="step-description">
                    Engage in a 6-round conversation with adaptive AI responses.
                </p>
            </div>
            <div class="step-card">
                <div class="step-number">3</div>
                <h3 class="step-title">Get Feedback</h3>
                <p class="step-description">
                    Receive detailed analysis and improve your interview skills.
                </p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
    <div class="footer">
        <p>© 2024 PersonaSynth - Developed by Arya Mane and Ameya Phansalkar</p>
    </div>
""", unsafe_allow_html=True)