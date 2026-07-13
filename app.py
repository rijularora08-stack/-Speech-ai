import streamlit as st
import os
import tempfile
import json
from pathlib import Path
import pandas as pd

# Import project modules
from utils import (
    save_uploaded_file,
    transcribe_audio,
    extract_audio_from_video
)

from summarizer import generate_summary
from diarization import perform_diarization
from emotion import detect_emotions
from threat import detect_threats
from history import (
    save_history,
    load_history
)
from exports import (
    export_pdf,
    export_docx,
    export_txt,
    export_csv
)

            # -----------------------------
            # Export Section
            # -----------------------------

            st.header("Download Results")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                pdf_file = export_pdf(transcript, summary)
                st.download_button(
                    "📄 PDF",
                    pdf_file,
                    file_name="transcript.pdf",
                    mime="application/pdf"
                )

            with col2:
                docx_file = export_docx(transcript, summary)
                st.download_button(
                    "📝 DOCX",
                    docx_file,
                    file_name="transcript.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            with col3:
                txt_file = export_txt(transcript)
                st.download_button(
                    "📃 TXT",
                    txt_file,
                    file_name="transcript.txt",
                    mime="text/plain"
                )

            with col4:
                csv_file = export_csv(emotions)
                st.download_button(
                    "📊 CSV",
                    csv_file,
                    file_name="emotion_results.csv",
                    mime="text/csv"
                )

            # -----------------------------
            # Save History
            # -----------------------------

            history_record = {
                "filename": uploaded_file.name,
                "transcript": transcript,
                "summary": summary,
                "emotions": emotions,
                "threats": threats
            }

            save_history(history_record)

            st.success("Saved to History Successfully!")

# -----------------------------
# History Page
# -----------------------------
elif menu == "History":

    st.title("📚 Previous History")

    history = load_history()

    if len(history) == 0:
        st.info("No previous records found.")

    else:

        for item in reversed(history):

            with st.expander(item["filename"]):

                st.subheader("Transcript")
                st.write(item["transcript"])

                st.subheader("Summary")
                st.write(item["summary"])

                if "emotions" in item:
                    st.dataframe(pd.DataFrame(item["emotions"]))

                if "threats" in item:
                    st.dataframe(pd.DataFrame(item["threats"]))
                  # -----------------------------
# Permanent Archive
# -----------------------------
elif menu == "Permanent Archive":

    st.title("📁 Permanent Archive")

    archive = load_history()

    if archive:

        filenames = [item["filename"] for item in archive]

        selected = st.selectbox(
            "Choose File",
            filenames
        )

        for item in archive:

            if item["filename"] == selected:

                st.write(item["transcript"])

                st.write(item["summary"])
              # -----------------------------
# About
# -----------------------------
elif menu == "About":

    st.title("ℹ️ About")

    st.markdown("""
### AI Speech Intelligence

This application provides:

- 🎙 Speech Transcription
- 👥 Speaker Diarization
- 😊 Emotion Detection
- ⚠ Threat Detection
- 📝 AI Summarization
- 📄 Export to PDF, DOCX, TXT & CSV
- 📚 History Management
- ☁ Deployment Ready

Developed using:

- Streamlit
- Faster Whisper
- Hugging Face Transformers
- PyTorch
- FFmpeg
""")
