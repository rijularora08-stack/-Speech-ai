import streamlit as st
import os
import tempfile
import pandas as pd

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


st.set_page_config(
    page_title="AI Speech Intelligence",
    page_icon="🎙️",
    layout="wide"
)


# Sidebar Menu
menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Analyze",
        "History",
        "Permanent Archive",
        "About"
    ]
)


# -----------------------------
# Analyze Page
# -----------------------------

if menu == "Analyze":

    st.title("🎙️ AI Speech Intelligence")

    uploaded_file = st.file_uploader(
        "Upload Audio / Video",
        type=[
            "mp3",
            "wav",
            "m4a",
            "mp4",
            "mov"
        ]
    )


    if uploaded_file:

        with tempfile.TemporaryDirectory() as temp_dir:

            file_path = save_uploaded_file(
                uploaded_file,
                temp_dir
            )


            if uploaded_file.type.startswith("video"):

                st.info("Extracting audio...")
                file_path = extract_audio_from_video(
                    file_path
                )


            if st.button("Analyze"):

                with st.spinner("Processing..."):


                    # Transcription
                    st.subheader("📝 Transcript")

                    transcript = transcribe_audio(
                        file_path
                    )

                    st.write(transcript)



                    # Summary
                    st.subheader("📌 Summary")

                    summary = generate_summary(
                        transcript
                    )

                    st.write(summary)



                    # Diarization
                    st.subheader("👥 Speaker Diarization")

                    speakers = perform_diarization(
                        file_path
                    )

                    st.write(speakers)



                    # Emotion
                    st.subheader("😊 Emotion Detection")

                    emotions = detect_emotions(
                        transcript
                    )

                    st.dataframe(
                        pd.DataFrame(emotions)
                    )



                    # Threat Detection
                    st.subheader("⚠ Threat Detection")

                    threats = detect_threats(
                        transcript
                    )

                    st.dataframe(
                        pd.DataFrame(threats)
                    )



                    # -----------------------------
                    # Export Section
                    # -----------------------------

                    st.header("Download Results")

                    col1, col2, col3, col4 = st.columns(4)


                    with col1:

                        pdf_file = export_pdf(
                            transcript,
                            summary
                        )

                        st.download_button(
                            "📄 PDF",
                            pdf_file,
                            file_name="transcript.pdf",
                            mime="application/pdf"
                        )


                    with col2:

                        docx_file = export_docx(
                            transcript,
                            summary
                        )

                        st.download_button(
                            "📝 DOCX",
                            docx_file,
                            file_name="transcript.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )


                    with col3:

                        txt_file = export_txt(
                            transcript
                        )

                        st.download_button(
                            "📃 TXT",
                            txt_file,
                            file_name="transcript.txt",
                            mime="text/plain"
                        )


                    with col4:

                        csv_file = export_csv(
                            emotions
                        )

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


                    save_history(
                        history_record
                    )


                    st.success(
                        "Saved to History Successfully!"
                    )



# -----------------------------
# History Page
# -----------------------------

elif menu == "History":

    st.title("📚 Previous History")


    history = load_history()


    if len(history) == 0:

        st.info(
            "No previous records found."
        )


    else:

        for item in reversed(history):

            with st.expander(
                item["filename"]
            ):

                st.subheader(
                    "Transcript"
                )

                st.write(
                    item["transcript"]
                )


                st.subheader(
                    "Summary"
                )

                st.write(
                    item["summary"]
                )


                if "emotions" in item:

                    st.dataframe(
                        pd.DataFrame(
                            item["emotions"]
                        )
                    )


                if "threats" in item:

                    st.dataframe(
                        pd.DataFrame(
                            item["threats"]
                        )
                    )



# -----------------------------
# Permanent Archive
# -----------------------------

elif menu == "Permanent Archive":

    st.title("📁 Permanent Archive")


    archive = load_history()


    if archive:

        filenames = [
            item["filename"]
            for item in archive
        ]


        selected = st.selectbox(
            "Choose File",
            filenames
        )


        for item in archive:

            if item["filename"] == selected:

                st.write(
                    item["transcript"]
                )

                st.write(
                    item["summary"]
                )


    else:

        st.info(
            "Archive empty."
        )



# -----------------------------
# About
# -----------------------------

elif menu == "About":

    st.title("ℹ️ About")


    st.markdown(
"""
### AI Speech Intelligence

Features:

- 🎙 Speech Transcription
- 👥 Speaker Diarization
- 😊 Emotion Detection
- ⚠ Threat Detection
- 📝 AI Summarization
- 📄 PDF, DOCX, TXT & CSV Export
- 📚 History Management
- ☁ Deployment Ready

Built using:

- Streamlit
- Faster Whisper
- Hugging Face Transformers
- PyTorch
- FFmpeg
"""
)
