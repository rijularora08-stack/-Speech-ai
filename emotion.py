from transformers import pipeline

emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None
)


def detect_emotions(text):

    if not text:
        return []

    result = emotion_classifier(text[:512])[0]

    return sorted(
        result,
        key=lambda x: x["score"],
        reverse=True
    )
