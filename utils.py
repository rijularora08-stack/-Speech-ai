
import os
import tempfile
from pathlib import Path

from faster_whisper import WhisperModel
from moviepy.editor import VideoFileClip

# Load Whisper model only once
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

# ----------------------------------
# Save uploaded file
# ----------------------------------

def save_uploaded_file(uploaded_file):

    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)

    file_path = os.path.join(
        temp_dir,
        uploaded_file.name
    )

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


# ----------------------------------
# Extract audio from video
# ----------------------------------

def extract_audio_from_video(video_path):

    audio_path = (
        Path(video_path).stem + ".wav"
    )

    audio_path = os.path.join(
        "temp_files",
        audio_path
    )

    clip = VideoFileClip(video_path)

    clip.audio.write_audiofile(
        audio_path,
        logger=None
    )

    clip.close()

    return audio_path


# ----------------------------------
# Transcribe Audio
# ----------------------------------

def transcribe_audio(audio_path):

    segments, info = model.transcribe(
        audio_path,
        beam_size=5
    )

    transcript = ""

    for segment in segments:

        transcript += (
            f"[{segment.start:.2f} - "
            f"{segment.end:.2f}] "
            f"{segment.text}\n"
        )

  
    return transcript
  import librosa

# ----------------------------------
# Detect Language
# ----------------------------------

def detect_language(audio_path):

    _, info = model.transcribe(
        audio_path,
        beam_size=5
    )

    return info.language


# ----------------------------------
# Audio Duration
# ----------------------------------

def get_audio_duration(audio_path):

    duration = librosa.get_duration(
        path=audio_path
    )

    return round(duration, 2)


# ----------------------------------
# Format Seconds
# ----------------------------------

def format_timestamp(seconds):

    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    return f"{hrs:02}:{mins:02}:{secs:02}"


# ----------------------------------
# Transcript with Timestamps
# ----------------------------------

def transcribe_with_segments(audio_path):

    segments, info = model.transcribe(
        audio_path,
        beam_size=5
    )

    results = []

    for segment in segments:

        results.append(
            {
                "start": format_timestamp(segment.start),
                "end": format_timestamp(segment.end),
                "text": segment.text
            }
        )

    return results


# ----------------------------------
# Search Transcript
# ----------------------------------

def search_transcript(transcript, keyword):

    keyword = keyword.lower()

    lines = transcript.split("\n")

    matches = []

    for line in lines:

        if keyword in line.lower():
            matches.append(line)

    return matches


# ----------------------------------
# Delete Temporary File
# ----------------------------------

def cleanup_file(file_path):

    try:

        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception:
        pass
