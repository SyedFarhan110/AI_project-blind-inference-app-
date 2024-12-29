 AI_project-blind-inference-app
 <br>
This is an application build for blind student to understand graphs or images more easily
<br>
Design by: Syed Farhan Ali Raza and team mates
<br>

Here is an overview of your project that can be used as a GitHub README:


Image Inference App

A versatile web application that allows users to upload images, provide prompts (text or voice), and get descriptive results using advanced machine learning models. The app supports multiple models, including HuggingFace, Phi-3.5 Vision, and Groq. It is built using Streamlit and includes features like text-to-speech, voice input, and file downloads (text/audio).

Features

- Model Selection: Choose from pre-defined models for image inference:
  - HuggingFaceM4/Docmatix-Florence-2
  - maxiw/Phi-3.5-vision
  - Groq
- Image Upload: Supports multiple image formats (png, jpg, jpeg, bmp).
- Prompt Customization: Provide a detailed prompt for image analysis, or use voice input for convenience.
- Mode Selection: Pre-defined prompts based on the mode:
  - Default Mode: Describes the image for a blind person.
  - Logic Component Mode: Focuses on logic components in the image.
  - Circuit Diagram Mode: Explains circuit diagrams for problem-solving.
  - Custom Mode: Allows custom prompts for unique requirements.
- Text-to-Speech (TTS): Converts output descriptions into audio and plays them.
- File Downloads: Download results as:
  - Text (.txt)
  - Audio (.mp3)
  - Combined Text and Audio (.zip)
- Voice Input: Capture prompts via microphone using speech recognition.

 Requirements

 Python Libraries
- groq
- streamlit
- pyttsx3
- speech_recognition
- gradio_client
- Pillow

Install dependencies using:

bash
pip install -r requirements.txt


 Additional Setup
- Groq API Key: Required for using the Groq model. Replace the placeholder in the code with your API key.
- Microphone access is needed for voice input functionality.

 Usage

1. Clone the repository:

   bash
   git clone <repository-url>
   cd <repository-folder>
   

2. Run the Streamlit application:

   bash
   streamlit run app.py
   

3. Open the application in your browser and interact with the features:
   - Upload an image.
   - Select a model and mode.
   - Provide a text or voice prompt.
   - Submit and wait for results.

 Outputs

- View the processed image description in the app.
- Listen to the generated description using TTS.
- Download results as text, audio, or combined files.

 Architecture

- Frontend: Built with Streamlit for an interactive and user-friendly interface.
- Backend: Integrates various ML models for image inference.
- Voice and TTS: Powered by pyttsx3 and speech_recognition.

 Future Enhancements

- Expand model support.
- Add multilingual TTS support.
- Enhance result visualization for technical diagrams.

