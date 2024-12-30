from groq import Groq
import base64
import streamlit as st
import pyttsx3
import speech_recognition as sr  # Import the speech recognition library
from gradio_client import Client as Client2, handle_file
from PIL import Image
import tempfile
import os
import zipfile

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

class ImageInferenceApp:
    def __init__(self):
        self.client = None
        self.groq_client = None
        self.tts_engine = pyttsx3.init()  # Initialize the TTS engine

    def speak_result(self, text):
        """Convert the given text to speech and save it as an audio file."""
        audio_file_path = "output_audio.mp3"
        self.tts_engine.save_to_file(text, audio_file_path)
        self.tts_engine.runAndWait()  # Wait until the speech is finished
        return audio_file_path

    def speak_result_no_file(self, text):
        """Speak the result without saving it to a file."""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()  # Wait until the speech is finished

    def process_image(self, model_name, image_path, prompt):
        try:
            if model_name == "maxiw/Phi-3.5-vision":
                result = self.client.predict(
                    image=handle_file(image_path),
                    text_input=prompt,
                    model_id="microsoft/Phi-3.5-vision-instruct",
                    api_name="/run_example"
                )
            elif model_name == "HuggingFaceM4/Docmatix-Florence-2":
                result = self.client.predict(
                    image=handle_file(image_path),
                    text_input=prompt,
                    api_name="/process_image"
                )
            elif model_name == "Groq":
                base64_image = encode_image(image_path)
                self.groq_client = Groq(api_key="")  # Replace with your actual API key
                chat_completion = self.groq_client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}",
                                    },
                                },
                            ],
                        }
                    ],
                    model="llama-3.2-90b-vision-preview",
                )
                result = chat_completion.choices[0].message.content
            else:
                return "Error: Unsupported model selected."
            
            return result
        except Exception as e:
            return f"Error: {str(e)}"

# Function to capture voice input
def capture_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak your prompt.")
        try:
            audio = recognizer.listen(source, timeout=5)
            voice_text = recognizer.recognize_google(audio)  # Use Google’s speech recognition API
            st.success(f"Recognized prompt: {voice_text}")
            return voice_text
        except sr.WaitTimeoutError:
            st.error("Listening timed out. Please try again.")
        except sr.UnknownValueError:
            st.error("Sorry, could not understand the audio. Please try again.")
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")
    return ""

def main():
    st.title('Image Inference App')

    if "image_uploaded" not in st.session_state:
        st.session_state.image_uploaded = False
    
    if "result_available" not in st.session_state:
        st.session_state.result_available = False

    app = ImageInferenceApp()

    model_name = st.selectbox('Select Model:', [
        "HuggingFaceM4/Docmatix-Florence-2",
        "maxiw/Phi-3.5-vision",
        "Groq"
    ], help="Select the model you want to use for image inference.")

    image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg", "bmp"], help="Upload an image file for processing.")
    
    if image_file is not None:
        image = Image.open(image_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        if not st.session_state.image_uploaded:
            st.success("Image uploaded successfully!")
            app.speak_result_no_file("Image uploaded successfully!")
            st.session_state.image_uploaded = True
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            tmp_file.write(image_file.getbuffer())
            tmp_file_path = tmp_file.name

    # Mode selection using a dropdown menu
    mode = st.selectbox(
        'Select Mode:',
        [
            "Default Mode",
            "Logic Component Mode",
            "Circuit Diagram Mode",
            "Custom Mode"
        ],
        help="Choose the mode for image description."
    )

    # Set the default prompt based on selected mode
    if mode == "Logic Component Mode":
        default_prompt = "Recognize and describe the image for a blind person of logic components, do not mention the colours."
    elif mode == "Circuit Diagram Mode":
        default_prompt = "Please explain this circuit diagram without hallucination and its components in 6 lines so I can solve a numerical in it?"
    elif mode == "Custom Mode":
        default_prompt = ""  # No default prompt for custom mode
    else:  # Default Mode
        default_prompt = "Describe the image for a blind person."

    prompt = st.text_area(
        'Enter your prompt here...',
        value=default_prompt,
        help="Enter a prompt for the model. This will guide the description."
    )

    # Voice input button
    if st.button('Use Voice Input', help="Click to input the prompt using your voice."):
        voice_text = capture_voice_input()
        if voice_text:
            st.session_state.voice_prompt = voice_text
            st.text_area("Voice Recognized Prompt:", value=voice_text, height=100)

    if st.button('Submit', help="Submit the image and prompt for processing."):
        if model_name and image_file and prompt:
            if model_name != "Groq":
                app.client = Client2(model_name)
            submission_message = "Image submitted for interpretation..."
            st.info(submission_message)
            app.speak_result_no_file(submission_message)
            
            wait_message = "Please wait..."
            app.speak_result_no_file(wait_message)
            
            with st.spinner("Please wait..."):
                result = app.process_image(model_name, tmp_file_path, prompt)
            
            st.text_area('Output:', value=result, height=200)
            
            if result:
                app.speak_result_no_file(result)
                
                audio_file_path = app.speak_result(result)
                st.audio(audio_file_path, format='audio/mp3')

                st.session_state.result_available = True

                # Download buttons for text and audio files
                if st.session_state.result_available:
                    st.download_button(
                        label="Download Text",
                        data=result,
                        file_name="output_text.txt",
                        mime="text/plain",
                        key="text_download"
                    )

                    st.download_button(
                        label="Download Audio",
                        data=open(audio_file_path, 'rb').read(),
                        file_name="output_audio.mp3",
                        mime="audio/mp3",
                        key="audio_download"
                    )

                    # Create a zip file containing both text and audio files
                    zip_file_path = "output_files.zip"
                    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                        zipf.write(audio_file_path, arcname="output_audio.mp3")
                        zipf.writestr("output_text.txt", result)

                    # Provide a download button for the zip file
                    with open(zip_file_path, 'rb') as f:
                        st.download_button(
                            label="Download Both Audio and Text",
                            data=f,
                            file_name="output_files.zip",
                            mime="application/zip",
                            key="zip_download"
                        )
            else:
                st.warning("No result to speak.")
        else:
            st.error("Please fill in all fields.")

if __name__ == "__main__":
    main()
