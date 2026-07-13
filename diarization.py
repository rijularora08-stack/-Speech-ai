from pyannote.audio import Pipeline
import torch


def perform_diarization(audio_path, hf_token=None):

    if not hf_token:
        return "Hugging Face token missing."

    try:

        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=hf_token
        )

        if torch.cuda.is_available():
            pipeline.to(torch.device("cuda"))

        diarization = pipeline(audio_path)

        speakers = []

        for turn, _, speaker in diarization.itertracks(
            yield_label=True
        ):
            speakers.append(
                {
                    "speaker": speaker,
                    "start": round(turn.start, 2),
                    "end": round(turn.end, 2)
                }
            )

        return speakers

    except Exception as e:
        return [
            {
                "error": str(e)
            }
        ]
