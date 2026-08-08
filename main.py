import streamlit as st
import io
import pypdf
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Page configuration - MUST BE FIRST STREAMLIT CALL
st.set_page_config(page_title="AI Resume Analyser", page_icon="📄", layout="wide")
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Apply Font */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Cybertech Grid Glow Background */
    [data-testid="stAppViewContainer"] {
        background-color: #070913 !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.18) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(59, 130, 246, 0.14) 0px, transparent 50%),
            radial-gradient(at 50% 100%, rgba(139, 92, 246, 0.12) 0px, transparent 50%),
            linear-gradient(rgba(255, 255, 255, 0.006) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.006) 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 100%, 100% 100%, 30px 30px, 30px 30px !important;
        background-attachment: fixed !important;
    }
    
    /* Text elements styling */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, [data-testid="stWidgetLabel"] p {
        color: #F3F4F6 !important;
    }
    
    .badge {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
        border: 1px solid rgba(99, 102, 241, 0.35);
        color: #818CF8;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
        letter-spacing: 0.5px;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.1);
    }
    
    .main-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        background: linear-gradient(135deg, #818CF8 0%, #38BDF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        margin-bottom: 0.1rem;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        color: #9CA3AF !important;
        font-size: 1.15rem;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    /* Premium Glassmorphic Cards styling */
    .dashboard-card {
        background: rgba(255, 255, 255, 0.025) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .dashboard-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.12);
        border-color: rgba(99, 102, 241, 0.45) !important;
    }
    
    .card-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: #F3F4F6 !important;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Score card ring dashboard component */
    .score-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(59, 130, 246, 0.08) 100%) !important;
        border: 1px solid rgba(99, 102, 241, 0.25) !important;
        border-radius: 20px;
        padding: 24px;
        display: flex;
        align-items: center;
        gap: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.25);
    }
    
    .score-ring {
        width: 84px;
        height: 84px;
        border-radius: 50%;
        background: #070913 !important;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.25);
    }
    
    .score-number {
        font-size: 1.9rem;
        font-weight: 700;
        font-family: 'Space Grotesk', sans-serif;
        color: #F3F4F6 !important;
    }
    
    .score-label {
        font-size: 0.75rem;
        opacity: 0.6;
        color: #9CA3AF !important;
    }
    
    .score-info h3 {
        margin: 0 0 6px 0;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #F3F4F6 !important;
    }
    
    .score-info p {
        margin: 0;
        font-size: 0.95rem;
        opacity: 0.9;
        color: #D1D5DB !important;
        line-height: 1.4;
    }
    
    /* Custom button styling */
    div.stButton > button {
        background: linear-gradient(135deg, #6366F1 0%, #3B82F6 100%);
        color: white !important;
        font-weight: 600;
        border-radius: 14px;
        border: none;
        padding: 0.75rem 2.2rem;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        font-size: 1.05rem;
        letter-spacing: 0.5px;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, #4F46E5 0%, #2563EB 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.45);
    }
    
    div.stButton > button:active {
        transform: translateY(0);
    }

    /* Style sidebar */
    [data-testid="stSidebar"] {
        background-color: #04060b !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    .sidebar-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.4rem;
        margin-bottom: 1.5rem;
        color: #F3F4F6 !important;
    }
    
    .analysis-text {
        line-height: 1.8;
        font-size: 1rem;
        color: #E5E7EB !important;
    }
    
    /* Input fields and widgets customization */
    input, select, textarea {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #F3F4F6 !important;
        border-radius: 10px !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #F3F4F6 !important;
        border-radius: 10px !important;
    }
    
    /* Streamlit file uploader tweaks */
    div[data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.01) !important;
        border: 2px dashed rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px;
        padding: 10px;
    }
    
    /* Tab active indicator and color */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        color: #9CA3AF !important;
        border-radius: 10px 10px 0 0 !important;
        padding: 10px 16px !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #F3F4F6 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(99, 102, 241, 0.1) !important;
        border-color: rgba(99, 102, 241, 0.3) !important;
        color: #818CF8 !important;
        font-weight: bold !important;
    }
    
    /* ----------------- MOBILE RESPONSIVENESS MEDIA QUERIES ----------------- */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.1rem !important;
            text-align: center;
            margin-top: 1rem;
        }
        
        .subtitle {
            font-size: 0.95rem !important;
            text-align: center;
            margin-bottom: 1.8rem !important;
        }
        
        .score-card {
            flex-direction: column;
            text-align: center;
            padding: 18px !important;
            gap: 16px !important;
        }
        
        .score-ring {
            width: 72px;
            height: 72px;
        }
        
        .score-number {
            font-size: 1.6rem !important;
        }
        
        .dashboard-card {
            padding: 16px !important;
            margin-bottom: 14px !important;
        }
        
        /* Styled tabs padding & text size for mobile thumbs */
        .stTabs [data-baseweb="tab"] {
            padding: 8px 10px !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR CONFIGURATION -----------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ Control Center</div>', unsafe_allow_html=True)
    
    st.markdown("### Provider Configuration")
    provider = st.selectbox(
        "API Provider",
        options=["Gemini (Google)", "Grok (xAI)", "OpenAI"],
        index=0,
        help="Select the AI service provider you want to use."
    )
    
    # Provider-specific configurations
    if provider == "OpenAI":
        env_api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_AI_API_KEY")
        key_label = "OpenAI API Key Override"
        placeholder = "sk-..."
        help_text = "Provide your OpenAI API Key. If empty, the app will try to use the key configured in the .env file."
        model_options = ["gpt-4o", "gpt-4o-mini", "Custom..."]
        default_index = 0
    elif provider == "Grok (xAI)":
        # Grok (xAI)
        env_api_key = os.getenv("GROK_API_KEY") or os.getenv("XAI_API_KEY")
        key_label = "Grok API Key Override"
        placeholder = "xai-..."
        help_text = "Provide your Grok (xAI) API Key. If empty, the app will try to use GROK_API_KEY or XAI_API_KEY from the .env file."
        model_options = ["grok-4.5", "grok-4.3", "Custom..."]
        default_index = 0
    else:
        # Gemini (Google)
        env_api_key = os.getenv("GEMINI_API_KEY")
        key_label = "Gemini API Key Override"
        placeholder = "AIzaSy..."
        help_text = "Provide your Gemini API Key from Google AI Studio. If empty, the app will try to use GEMINI_API_KEY from the .env file."
        model_options = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-3.5-flash", "gemini-3.6-flash", "Custom..."]
        default_index = 0
        
    api_key_input = st.text_input(
        key_label, 
        type="password", 
        placeholder=placeholder, 
        help=help_text
    )
    
    # Determine key to use
    api_key = api_key_input if api_key_input else env_api_key
    
    if api_key:
        st.success(f"🔑 {provider} Key Configured")
    else:
        st.warning(f"⚠️ No {provider} Key found.")
        
    st.markdown("---")
    st.markdown("### Analysis Settings")
    
    # Model Selection
    selected_model = st.selectbox(
        "AI Engine Model",
        options=model_options,
        index=default_index,
        help=f"Select the {provider} model to use for analyzing your resume."
    )
    
    if selected_model == "Custom...":
        openai_model = st.text_input(
            "Enter Custom Model ID",
            placeholder="e.g. gemini-1.5-flash",
            help="Type the exact model ID you want to use from your provider's API docs."
        )
    else:
        openai_model = selected_model
    
    # Extra settings
    analysis_focus = st.multiselect(
        "Key Evaluation Areas",
        options=["Formatting & Layout", "Grammar & Tone", "Action Verbs & Impact", "Keywords Optimization"],
        default=["Formatting & Layout", "Action Verbs & Impact"],
        help="Select which specific dimensions you want the AI to pay extra attention to."
    )

# ----------------- MAIN VIEW -----------------
# Header
st.markdown('<div class="badge">✨ Powered by Generative AI</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">📄 AI Resume Analyser</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload your resume and get immediate expert feedback on your skills, experience, and job alignment.</p>', unsafe_allow_html=True)

# Main columns layout (which stack automatically on mobile screen sizes)
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="card-header">📂 Upload Document</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Drag and drop or browse your resume in PDF or TXT format", 
        type=["pdf", "txt"],
        label_visibility="collapsed"
    )
    
    st.markdown('<div class="card-header">🎯 Target Job Profile</div>', unsafe_allow_html=True)
    job_role = st.text_input(
        "What specific position or career field are you targeting?",
        placeholder="e.g. Frontend Engineer, Product Manager, Data Scientist (optional)",
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_button = st.button("Analyze Resume")

# ----------------- BUSINESS LOGIC -----------------
def extract_text_from_pdf(file):
    """Robust PDF text extraction using pypdf."""
    try:
        pdf_reader = pypdf.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        raise Exception(f"Failed to parse PDF document: {str(e)}")

def extract_text_from_file(uploaded_file):
    """Dispatches document to its appropriate parser based on file type."""
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    else:
        # Txt file path
        try:
            return uploaded_file.read().decode("utf-8")
        except Exception as e:
            raise Exception(f"Failed to read text file: {str(e)}")

def get_ai_analysis(resume_text, job_role, provider, model, focus_areas, api_key):
    """Sends prompt with structured tags to OpenAI/Grok/Gemini and parses response."""
    focus_str = ", ".join(focus_areas) if focus_areas else "General Quality"
    
    prompt = f"""You are an elite career advisor and executive recruiter. Please analyze the following resume contents.
    
    Target Job Role: {job_role if job_role else 'General / Not specified'}
    Special Focus Areas: {focus_str}

    Resume Text Content:
    ---
    {resume_text}
    ---

    Provide your evaluation in a clear, constructive, and highly professional style. You MUST divide your response using the following exact tag delimiters to structure the dashboard layout:
    
    [SCORE]
    (Provide a single numerical score between 0 and 100 representing the resume's match to the target job profile or general strength. Do not write any other text in this section, just the number.)

    [OVERVIEW]
    (Provide a high-level summary paragraph. Write about visual impression, career trajectory alignment, and an overall review.)
    
    [STRENGTHS]
    (Provide a list of 3-5 major strengths in the resume. Format as bullet points with bold headers.)
    
    [IMPROVEMENTS]
    (Provide a list of critical gaps, weak phrasing, formatting issues, or missed opportunities. Format as bullet points with bold headers.)
    
    [RECOMMENDATIONS]
    (Provide actionable, step-by-step improvements the user can make. Specifically tailor these for the target job role if specified.)
    
    Remember: Do not omit any tags, and write out each tag exactly as shown (in brackets).
    """

    try:
        if provider == "OpenAI":
            client = OpenAI(api_key=api_key)
        elif provider == "Grok (xAI)":
            client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
        else:
            # Gemini (Google) client setup using OpenAI compatible endpoint
            client = OpenAI(
                api_key=api_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )
            
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional resume consultant and career coach."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"{provider} API call failed: {str(e)}")

# Parse helper
def parse_analysis_result(text):
    """Parses response by brackets [TAG] into dictionary."""
    sections = {
        "score": "0",
        "overview": "",
        "strengths": "",
        "improvements": "",
        "recommendations": ""
    }
    
    try:
        # Finding segments
        score_idx = text.find("[SCORE]")
        overview_idx = text.find("[OVERVIEW]")
        strengths_idx = text.find("[STRENGTHS]")
        improvements_idx = text.find("[IMPROVEMENTS]")
        recommendations_idx = text.find("[RECOMMENDATIONS]")
        
        # Checking if all indices exist
        if all(idx != -1 for idx in [score_idx, overview_idx, strengths_idx, improvements_idx, recommendations_idx]):
            sections["score"] = text[score_idx + len("[SCORE]"):overview_idx].strip()
            sections["overview"] = text[overview_idx + len("[OVERVIEW]"):strengths_idx].strip()
            sections["strengths"] = text[strengths_idx + len("[STRENGTHS]"):improvements_idx].strip()
            sections["improvements"] = text[improvements_idx + len("[IMPROVEMENTS]"):recommendations_idx].strip()
            sections["recommendations"] = text[recommendations_idx + len("[RECOMMENDATIONS]"):].strip()
            return sections, True
        return {"full_text": text}, False
    except Exception:
        return {"full_text": text}, False

# Process Analysis
with col_right:
    st.markdown('<div class="card-header">📊 Analysis Dashboard</div>', unsafe_allow_html=True)
    
    if analyze_button:
        if not api_key:
            st.error(f"🔑 API Key not found! Please configure your {provider} API Key in the sidebar.")
        elif not uploaded_file:
            st.warning("📁 Please upload a resume file (PDF or TXT) first.")
        else:
            # We have everything we need
            with st.spinner("⏳ Analyzing resume... (Reading document)"):
                try:
                    file_content = extract_text_from_file(uploaded_file)
                    
                    if not file_content.strip():
                        st.error("❌ The uploaded file appears to be empty. Please upload a valid document.")
                        st.stop()
                        
                except Exception as e:
                    st.error(f"❌ Error parsing file: {str(e)}")
                    st.stop()
            
            with st.spinner(f"🧠 Consulting {provider} Career Advisor..."):
                try:
                    raw_result = get_ai_analysis(file_content, job_role, provider, openai_model, analysis_focus, api_key)
                    
                    sections, parsed_successfully = parse_analysis_result(raw_result)
                    
                    if parsed_successfully:
                        # Convert score to int to calculate ring styles
                        try:
                            score_val = int(sections["score"])
                        except ValueError:
                            score_val = 0
                            
                        # Ring color logic based on performance
                        if score_val >= 80:
                            ring_color = "#10B981"  # Emerald
                            score_status = "Excellent Match! Your resume aligns very closely with this profile."
                        elif score_val >= 60:
                            ring_color = "#F59E0B"  # Amber
                            score_status = "Good Potential. Some details can be optimized for better suitability."
                        else:
                            ring_color = "#EF4444"  # Crimson
                            score_status = "Needs Improvement. High skill gaps or layout issues detected."
                            
                        # Render score board component
                        st.markdown(f"""
                        <div class="score-card">
                            <div class="score-ring" style="border: 4px solid {ring_color};">
                                <span class="score-number">{score_val}</span>
                                <span class="score-label">/100</span>
                            </div>
                            <div class="score-info">
                                <h3>Suitability Rating</h3>
                                <p>{score_status}</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Rendering beautifully structured tabs!
                        tab_overview, tab_strengths, tab_improvements, tab_recommendations = st.tabs([
                            "📊 Executive Summary", 
                            "💪 Key Strengths", 
                            "🔍 Critical Gaps", 
                            "🎯 Recommendations"
                        ])
                        
                        with tab_overview:
                            st.markdown(f'<div class="dashboard-card"><div class="analysis-text">{sections["overview"]}</div></div>', unsafe_allow_html=True)
                            
                        with tab_strengths:
                            st.markdown(f'<div class="dashboard-card"><div class="analysis-text">{sections["strengths"]}</div></div>', unsafe_allow_html=True)
                            
                        with tab_improvements:
                            st.markdown(f'<div class="dashboard-card"><div class="analysis-text">{sections["improvements"]}</div></div>', unsafe_allow_html=True)
                            
                        with tab_recommendations:
                            st.markdown(f'<div class="dashboard-card"><div class="analysis-text">{sections["recommendations"]}</div></div>', unsafe_allow_html=True)
                    else:
                        # Fallback to standard Markdown render
                        st.markdown(raw_result)
                    
                    st.success("🎉 Analysis completed successfully!")
                    
                    # Store result in session state for download functionality
                    st.session_state["raw_result"] = raw_result
                    st.session_state["provider"] = provider
                    st.session_state["job_role"] = job_role
                    
                except Exception as e:
                    st.error(f"❌ Error during AI evaluation: {str(e)}")
    
    # Download Button Section
    if "raw_result" in st.session_state:
        st.markdown("<br>", unsafe_allow_html=True)
        report_data = st.session_state["raw_result"]
        state_provider = st.session_state.get("provider", "eval")
        state_job = st.session_state.get("job_role", "")
        
        # Clean file names
        role_suffix = f"_{state_job.lower().replace(' ', '_')}" if state_job else ""
        filename = f"resume_{state_provider.lower()}_evaluation{role_suffix}.md"
        
        st.download_button(
            label="📥 Download Detailed Report (.md)",
            data=report_data,
            file_name=filename,
            mime="text/markdown"
        )
    else:
        st.info("Your analysis results will appear here after you click the 'Analyze Resume' button.")
