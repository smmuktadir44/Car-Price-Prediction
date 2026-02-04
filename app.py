# Essential Libraries
import streamlit as st
import joblib
import pandas as pd
import time

# Page config
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for stunning dark visuals
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Orbitron:wght@400;700;900&display=swap');
    
    /* Main app styling with dark theme */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Animated background particles effect */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(88, 86, 214, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(138, 43, 226, 0.05) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        position: relative;
        z-index: 1;
    }
    
    /* Title styling with glow effect */
    h1 {
        color: #fff;
        text-align: center;
        font-weight: 900;
        font-size: 4rem !important;
        font-family: 'Orbitron', sans-serif;
        text-shadow: 
            0 0 10px rgba(138, 43, 226, 0.8),
            0 0 20px rgba(138, 43, 226, 0.6),
            0 0 30px rgba(138, 43, 226, 0.4),
            0 0 40px rgba(138, 43, 226, 0.2);
        margin-bottom: 0.5rem !important;
        animation: glow 2s ease-in-out infinite alternate;
        letter-spacing: 3px;
    }
    
    @keyframes glow {
        from {
            text-shadow: 
                0 0 10px rgba(138, 43, 226, 0.8),
                0 0 20px rgba(138, 43, 226, 0.6),
                0 0 30px rgba(138, 43, 226, 0.4);
        }
        to {
            text-shadow: 
                0 0 20px rgba(138, 43, 226, 1),
                0 0 30px rgba(138, 43, 226, 0.8),
                0 0 40px rgba(138, 43, 226, 0.6),
                0 0 50px rgba(138, 43, 226, 0.4);
        }
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.3rem;
        margin-bottom: 2.5rem;
        animation: fadeIn 1.5s ease-in-out;
        letter-spacing: 1px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
    }
    
    /* Card containers with glass morphism */
    .card {
        background: rgba(30, 30, 50, 0.7);
        border-radius: 25px;
        padding: 2.5rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 1px 1px rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1.5rem;
        animation: fadeInUp 0.8s ease-in-out;
        position: relative;
        overflow: hidden;
        display: none;
    }
    
    /* Card shine effect */
    .card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(255, 255, 255, 0.03),
            transparent
        );
        transform: rotate(45deg);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    /* Section headers */
    .section-header {
        color: #a78bfa;
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 3px solid;
        border-image: linear-gradient(90deg, #a78bfa, #ec4899) 1;
        display: flex;
        align-items: center;
        gap: 0.7rem;
        text-shadow: 0 2px 10px rgba(167, 139, 250, 0.3);
    }
    
    /* Input fields */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 12px;
        border: 2px solid rgba(167, 139, 250, 0.3);
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: rgba(20, 20, 35, 0.6) !important;
        color: #fff !important;
        font-weight: 500;
    }
    
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #a78bfa;
        box-shadow: 
            0 0 0 3px rgba(167, 139, 250, 0.2),
            0 0 20px rgba(167, 139, 250, 0.3);
        background: rgba(30, 30, 50, 0.8) !important;
    }
    
    /* Labels */
    .stNumberInput > label,
    .stSelectbox > label {
        color: #e0e7ff !important;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    
    /* Ensure all text in widgets is visible */
    [data-testid="stNumberInput"] label,
    [data-testid="stSelectbox"] label,
    [data-testid="stNumberInput"] p,
    [data-testid="stSelectbox"] p {
        color: #e0e7ff !important;
    }
    
    /* Custom label styling */
    .custom-label {
        color: #c4b5fd !important;
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Widget container text */
    .stNumberInput, .stSelectbox {
        color: #fff !important;
    }
    
    /* Dropdown options */
    .stSelectbox option {
        background-color: #1e1e32;
        color: #fff;
    }
    
    /* Predict button with gradient and glow */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        padding: 1.3rem 2rem;
        border-radius: 18px;
        border: none;
        box-shadow: 
            0 6px 25px rgba(102, 126, 234, 0.5),
            0 0 30px rgba(118, 75, 162, 0.3);
        transition: all 0.4s ease;
        margin-top: 2rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-family: 'Orbitron', sans-serif;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 
            0 10px 35px rgba(102, 126, 234, 0.7),
            0 0 50px rgba(118, 75, 162, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1);
    }
    
    /* Success message with neon glow */
    .success-box {
        background: linear-gradient(135deg, #0f766e 0%, #14b8a6 50%, #2dd4bf 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        font-size: 1.6rem;
        font-weight: 700;
        box-shadow: 
            0 10px 40px rgba(20, 184, 166, 0.4),
            0 0 60px rgba(20, 184, 166, 0.2),
            inset 0 1px 1px rgba(255, 255, 255, 0.2);
        animation: bounceIn 0.6s ease-in-out, pulse 2s ease-in-out infinite;
        margin-top: 2rem;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    @keyframes pulse {
        0%, 100% {
            box-shadow: 
                0 10px 40px rgba(20, 184, 166, 0.4),
                0 0 60px rgba(20, 184, 166, 0.2);
        }
        50% {
            box-shadow: 
                0 10px 50px rgba(20, 184, 166, 0.6),
                0 0 80px rgba(20, 184, 166, 0.4);
        }
    }
    
    .price-value {
        font-size: 3rem;
        font-weight: 900;
        margin-top: 0.8rem;
        font-family: 'Orbitron', sans-serif;
        text-shadow: 
            0 0 10px rgba(255, 255, 255, 0.5),
            0 2px 4px rgba(0, 0, 0, 0.3);
        letter-spacing: 2px;
    }
    
    /* Error message */
    .stAlert {
        border-radius: 15px;
        animation: shake 0.5s ease-in-out;
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    /* Icon styling */
    .icon {
        font-size: 2rem;
        margin-right: 0.5rem;
        filter: drop-shadow(0 0 5px rgba(167, 139, 250, 0.5));
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes bounceIn {
        0% {
            opacity: 0;
            transform: scale(0.3);
        }
        50% {
            opacity: 1;
            transform: scale(1.05);
        }
        70% {
            transform: scale(0.9);
        }
        100% {
            transform: scale(1);
        }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
    
    /* Grid layout improvements */
    .row-widget.stHorizontal {
        gap: 1rem;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        color: #fff !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        font-family: 'Orbitron', sans-serif;
    }
    
    [data-testid="stMetricLabel"] {
        color: #c4b5fd !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    [data-testid="stMetric"] {
        background: rgba(30, 30, 50, 0.5);
        padding: 1.2rem;
        border-radius: 15px;
        border: 1px solid rgba(167, 139, 250, 0.2);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Make sure card content is visible */
    .card * {
        color: #fff;
    }
    
    .card .section-header {
        color: #a78bfa !important;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-color: #a78bfa !important;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 30, 50, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea, #764ba2);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #764ba2, #f093fb);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        h1 {
            font-size: 2.5rem !important;
        }
        .card {
            padding: 1.5rem;
        }
        .price-value {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Load the model
@st.cache_resource
def load_model():
    try:
        return joblib.load('car_price_pipeline.pkl')
    except:
        return None

model = load_model()

# Header with enhanced styling
st.markdown("<h1>🚗 CAR PRICE PREDICTOR</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>⚡ Get instant price estimates using advanced AI & machine learning ⚡</p>", unsafe_allow_html=True)

if model is None:
    st.error("⚠️ Model file 'car_price_pipeline.pkl' not found. Please ensure it's in the same directory.")
    st.stop()

# Create two columns for better layout
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'><span class='icon'>🔧</span>Basic Information</div>", unsafe_allow_html=True)
    
    st.markdown("<p class='custom-label'>📅 Year</p>", unsafe_allow_html=True)
    year = st.number_input("Year", min_value=1990, max_value=2025, value=2015, step=1, label_visibility="collapsed")
    
    st.markdown("<p class='custom-label'>🛣️ Kilometers Driven</p>", unsafe_allow_html=True)
    km_driven = st.number_input("KM Driven", min_value=0, max_value=1000000, value=50000, step=1000, label_visibility="collapsed")
    
    st.markdown("<p class='custom-label'>⛽ Fuel Type</p>", unsafe_allow_html=True)
    fuel = st.selectbox("Fuel Type", ['Diesel', 'Petrol', 'CNG', 'LPG'], label_visibility="collapsed")
    
    st.markdown("<p class='custom-label'>👤 Seller Type</p>", unsafe_allow_html=True)
    seller_type = st.selectbox("Seller Type", ['Individual', 'Dealer', 'Trustmark Dealer'], label_visibility="collapsed")
    
    st.markdown("<p class='custom-label'>⚙️ Transmission</p>", unsafe_allow_html=True)
    transmission = st.selectbox("Transmission", ['Manual', 'Automatic'], label_visibility="collapsed")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'><span class='icon'>📊</span>Technical Specifications</div>", unsafe_allow_html=True)
    
    st.markdown("<p class='custom-label'>🔑 Owner Type</p>", unsafe_allow_html=True)
    owner = st.selectbox("Owner Type", ['First Owner', 'Second Owner', 'Third Owner', 'Fourth & Above Owner'], label_visibility="collapsed")
    
    st.markdown("<p class='custom-label'>⛽ Mileage (kmpl)</p>", unsafe_allow_html=True)
    mileage = st.number_input("Mileage", min_value=0.0, max_value=100.0, value=20.0, step=0.1, label_visibility="collapsed")
    
    st.markdown("<p class='custom-label'>🔩 Engine CC</p>", unsafe_allow_html=True)
    engine = st.number_input("Engine CC", min_value=600, max_value=7000, value=1200, step=50, label_visibility="collapsed")
    
    st.markdown("<p class='custom-label'>⚡ Max Power (bhp)</p>", unsafe_allow_html=True)
    max_power = st.number_input("Max Power", min_value=30.0, max_value=1000.0, value=80.0, step=1.0, label_visibility="collapsed")
    
    st.markdown("<p class='custom-label'>💺 Number of Seats</p>", unsafe_allow_html=True)
    seats = st.number_input("Seats", min_value=2, max_value=14, value=5, step=1, label_visibility="collapsed")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Predict button (full width)
st.markdown("<div class='card'>", unsafe_allow_html=True)

if st.button("🎯 Predict Price"):
    # Show loading animation
    with st.spinner('🔮 Analyzing vehicle data with AI...'):
        time.sleep(0.8)  # Small delay for effect
        
        # Prepare input data
        input_df = pd.DataFrame([[
            fuel, seller_type, transmission, owner, year, km_driven, 
            mileage, engine, max_power, seats
        ]], columns=[
            'fuel', 'seller_type', 'transmission', 'owner', 
            'year', 'km_driven', 'mileage', 'engine', 'max_power', 'seats'
        ])
        
        try:
            # Make prediction
            prediction = model.predict(input_df)[0]
            
            # Display result with animation
            st.markdown(f"""
                <div class='success-box'>
                    <div>✨ ESTIMATED CAR PRICE ✨</div>
                    <div class='price-value'>৳ {prediction:,.2f}</div>
                    <div style='font-size: 1.1rem; margin-top: 1rem; opacity: 0.95; font-weight: 500;'>
                        🤖 AI-Powered Market Analysis
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Add some additional insights
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                age = 2025 - year
                st.metric("🕐 Vehicle Age", f"{age} years")
            
            with col2:
                km_per_year = km_driven / max(age, 1)
                st.metric("📏 Avg KM/Year", f"{km_per_year:,.0f}")
            
            with col3:
                condition = "Excellent" if km_driven < 30000 else "Good" if km_driven < 60000 else "Fair"
                st.metric("⭐ Condition", condition)
                
        except Exception as e:
            st.error(f"❌ Error making prediction: {str(e)}")
            st.info("💡 Please check that all inputs are valid and try again.")

st.markdown("</div>", unsafe_allow_html=True)

# Footer with enhanced styling
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: rgba(255, 255, 255, 0.7); font-size: 0.95rem;'>
    <p style='margin-bottom: 0.5rem;'>
        <span style='font-size: 1.2rem;'>🤖</span> 
        <span style='color: #a78bfa; font-weight: 600;'>Powered by Machine Learning</span> 
        <span style='margin: 0 1rem;'>|</span> 
        Made with <span style='color: #ec4899;'>❤️</span> using 
        <span style='color: #a78bfa; font-weight: 600;'>Streamlit</span>
    </p>
    <p style='font-size: 0.85rem; opacity: 0.6; margin-top: 0.3rem;'>
        © 2025 AI Car Price Predictor • All Rights Reserved
    </p>
</div>
""", unsafe_allow_html=True)