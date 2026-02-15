
import streamlit as st
import numpy as np
from PIL import Image
import os
import tensorflow as tf

# --- Configuration ---
st.set_page_config(
    page_title="BananaA.I.",
    page_icon="🍌",
    layout="centered"
)

# Custom CSS for aesthetic improvements
st.markdown("""
<style>
    .stApp {
        background-color: #121212;
        color: #ffffff;
    }
    h1 {
        color: #FFD700;
        text-align: center;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        color: #aaaaaa;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .result-card {
        background-color: #1e1e1e;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #333;
        margin-top: 2rem;
    }
    .days-left {
        font-size: 3rem;
        font-weight: bold;
        color: #FFD700;
    }
    .metric-label {
        color: #dddddd;
        font-size: 1rem;
    }
    /* Mirror the camera preview */
    [data-testid="stCamera"] video {
        transform: scaleX(-1);
    }
</style>
""", unsafe_allow_html=True)

# --- Model Loading ---
@st.cache_resource
def load_model():
    model_path = "model/banana_ripeness_model.tflite"
    if not os.path.exists(model_path):
        return None, f"Model file not found at {model_path}"
    
    try:
        interpreter = tf.lite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        return (interpreter, input_details, output_details), None
    except Exception as e:
        return None, str(e)

# --- Logic ---
def predict(interpreter_data, image):
    interpreter, input_details, output_details = interpreter_data
    
    # Preprocess
    target_size = (224, 224)
    # Get input shape from model if possible
    input_shape = input_details[0]['shape']
    if len(input_shape) == 4:
        target_size = (input_shape[1], input_shape[2])
        
    image = image.convert('RGB').resize(target_size)
    img_array = np.array(image, dtype=np.float32)
    
    # Check if model expects normalized input (float32) or int8
    if input_details[0]['dtype'] == np.float32:
        img_array = img_array / 255.0
    elif input_details[0]['dtype'] == np.uint8:
        # If it's uint8, keep it 0-255 (but cast to uint8)
        img_array = img_array.astype(np.uint8)
    
    img_array = np.expand_dims(img_array, axis=0) # Add batch dimension

    # Inference
    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    # Post-process
    days_left = float(output_data[0][0]) if output_data.ndim > 1 else float(output_data[0])
    return days_left

# --- UI ---
st.title("🍌 BananaA.I.")
st.markdown('<p class="subtitle">Advanced Ripeness Prediction System</p>', unsafe_allow_html=True)

model_data, error = load_model()

if error:
    st.error(f"Failed to load model: {error}")
    st.info("Ensure 'model/banana_ripeness_model.tflite' exists and TensorFlow is installed.")
else:
    # Tabs
    tab1, tab2 = st.tabs(["📁 Upload Image", "📸 Use Webcam"])
    
    image = None
    
    with tab1:
        uploaded_file = st.file_uploader("Choose a banana image...", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
    with tab2:
        camera_image = st.camera_input("Take a picture")
        if camera_image:
            image = Image.open(camera_image)
            # st.image(image, caption="captured", use_column_width=True) # camera_input shows it already

    if image:
        with st.spinner("Analyzing ripeness..."):
            try:
                days = predict(model_data, image)
                
                # Clamp and Format
                days = max(0, min(15, days))
                
                # Determine Color
                color = "#4dff4d" # Green
                status = "Fresh"
                if days < 7:
                    color = "#FFD700" # Yellow
                    status = "Ripe"
                if days < 3:
                    color = "#ff4d4d" # Red
                    status = "Overripe / Spoiling"

                st.markdown(f"""
                <div class="result-card">
                    <div class="metric-label">Estimated Shelf Life</div>
                    <div class="days-left" style="color: {color};">{days:.1f} Days</div>
                    <div style="margin-top: 10px; color: #888;">Condition: <span style="color: {color}; font-weight: bold;">{status}</span></div>
                    <div style="width: 100%; background-color: #333; height: 10px; border-radius: 5px; margin-top: 15px; overflow: hidden;">
                        <div style="width: {(days/15)*100}%; background-color: {color}; height: 100%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error during prediction: {str(e)}")
