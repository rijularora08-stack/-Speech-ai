import os
import tempfile
import whisper


@staticmethod
def save_uploaded_file(uploaded_file):

    temp_dir = tempfile.gettempdir()

    file_path = os.path.join(
        temp_dir,
        uploaded_file.name
    )

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path



def transcribe_audio(audio_path):

    model = whisper.load_model("base")

    result = model.transcribe(
        audio_path
    )

    return result["text"]



def extract_audio_from_video(video_path):

    import moviepy.editor as mp

    video = mp.VideoFileClip(video_path)

    audio_path = video_path + ".mp3"

    video.audio.write_audiofile(
        audio_path
    )

    return audio_path
