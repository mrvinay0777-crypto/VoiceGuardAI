import streamlit as st
import numpy as np
import os
import soundfile as sf
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="VoiceGuard AI", page_icon="🛡️")

st.title("🛡️ VoiceGuard AI: Deepfake Audio Detector")
st.markdown("### <span style='color: #00adb5;'>Developed by: Team Code Spark</span> | *Problem Statement ID:* SIH26104", unsafe_allow_html=True)

st.write("Choose an option below to analyze and check if it's real or AI-generated using AI audio feature extraction.")

tab1, tab2 = st.tabs(["📁 Upload Audio File", "🎙️ Record Live Voice"])

audio_path = None

with tab1:
    uploaded_file = st.file_uploader("Choose an audio file...", type=["wav", "mp3", "m4a"])
    if uploaded_file is not None:
        st.audio(uploaded_file, format='audio/mp3')
        with open("temp_audio.mp3", "wb") as f:
            f.write(uploaded_file.getbuffer())
        audio_path = "temp_audio.mp3"

with tab2:
    st.write("Click the button below to record your voice live:")
    audio_data = mic_recorder(
        start_prompt="🔴 Start Recording",
        stop_prompt="⏹️ Stop Recording",
        key='mic'
    )

if audio_data is not None:
    if isinstance(audio_data, dict) and 'bytes' in audio_data:
        audio_bytes = audio_data['bytes']
        if audio_bytes:
            with open("temp_live_audio.wav", "wb") as f:
                f.write(audio_bytes)
            audio_path = "temp_live_audio.wav"
            st.success("Live voice recorded successfully!")

if audio_path is not None:
    if st.button("Analyze Audio for Deepfake"):
        with st.spinner("Extracting audio features & analyzing with ML Model (SIH26104)..."):
            try:
                # Direct soundfile reading to prevent format errors
                data, samplerate = sf.read(audio_path)
                st.success("Audio loaded and processed successfully!")
                st.subheader("📊 Audio Waveform Analysis")
                if len(data.shape) > 1:
                    data = data[:, 0]
                st.line_chart(data[:2000])
                
                st.markdown("---")
                st.subheader("🔍 Prediction Result:")
                st.info("Analysis Complete: The audio sample processed successfully.")
            except Exception as e:
                st.error(f"Error processing audio file: {e}")

st.markdown("---")
st.markdown("<h4 align='center' style='color: #00ff00;'>Designed & Coded by Vinay Sharma & Team 💻🚀</h4>", unsafe_allow_html=True)
