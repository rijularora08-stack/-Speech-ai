
from pyannote.audio import Pipeline
import torch
import os


def diarize_audio(audio_path, hf_token=None):
    """
    Detects different speakers in audio
    """

    if hf_token is None:
        return "Hugging Face token required for speaker diarization."

    try:
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=hf_token
        )

        if torch.cuda.is_available():
            pipeline.to(torch.device("cuda"))

        diarization = pipeline(audio_path)

        result = ""

        for turn, _, speaker in diarization.itertracks(yield_label=True):
            result += (
                f"{speaker}: "
                f"{turn.start:.2f}s - "
                f"{turn.end:.2f}s\n"
            )

        return result

    except Exception as e:
        return f"Diarization error: {e}"
