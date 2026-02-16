# BananaA.I. 🍌

BananaA.I. is a Streamlit-based web application designed to predict the ripeness and remaining shelf life of bananas. Using a machine learning model, the app analyzes images of bananas to estimate how many days they have left before spoiling.

## Features

- **Dual Input Methods**: upload an image from your device or use your webcam directly within the app.
- **Instant Analysis**: Rapidly processes images to provide immediate feedback.
- **Visual Dashboard**: Displays the estimated days left, a textual condition status (Fresh, Ripe, Overripe), and a visual progress bar.
- **Responsive Design**: Dark-mode themed UI for a modern aesthetic.

## Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Machine Learning**: TensorFlow Lite (TFLite) for efficient model inference.
- **Image Processing**: Python Imaging Library (Pillow) and NumPy.

## Prerequisites

Ensure you have Python installed on your system. This application relies on the following Python packages:
- `streamlit`
- `numpy`
- `Pillow`
- `tensorflow-cpu` (or `tensorflow`)

## Installation

1.  **Clone the repository** (if applicable) or navigate to the project directory:

    ```bash
    cd bananaai
    ```

2.  **Install dependencies**:

    It is recommended to use a virtual environment.

    ```bash
    pip install -r requirements.txt
    ```

3.  **Verify Model**:
    Ensure the TFLite model file is located at `model/banana_ripeness_model.tflite`.

## Usage

To start the application open this link it works better using a phone main camera -https://howlongtillbananasgobad-evsauuzazgviygkstwlhn3.streamlit.app/

#The following method is for running the app on your own machine.--

To start the application, run the following command in your terminal:

```bash
streamlit run app.py
```

Alternatively, if you are on Windows, you can simply double-click the `run_app.bat` file.

The application will open in your default web browser (usually at `http://localhost:8501`).

## How it Works

1.  **Load Model**: The app loads a pre-trained TensorFlow Lite regression model at startup.
2.  **Input**: Users provide an image via upload or camera.
3.  **Preprocessing**: The image is resized to 224x224 (or model specific input), converted to RGB, and normalized (if required by the model).
4.  **Inference**: The model predicts a numerical value representing the days remaining.
5.  **Output**: The application displays the days left, classifies the condition based on the days, and shows a color-coded indicator (Green for fresh, Yellow for ripe, Red for spoilage).

## Project Structure

- `app.py`: The main Streamlit application script.
- `requirements.txt`: List of Python dependencies.
- `model/`: Directory containing the machine learning model (`banana_ripeness_model.tflite`).
- `run_app.bat`: Batch script for easy execution on Windows.
