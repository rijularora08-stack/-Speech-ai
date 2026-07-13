from transformers import pipeline

# Load emotion detection model
emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None
)


def detect_emotion(text):
    """
    Detect emotions from transcript text
    """

    if not text or len(text.strip()) == 0:
        return "No text available"

    try:
        results = emotion_classifier(text[:512])

        emotions = results[0]

        emotions = sorted(
            emotions,
            key=lambda x: x["score"],
            reverse=True
        )

        top_emotions = []

        for item in emotions[:3]:
            top_emotions.append(
                f"{item['label']}: {round(item['score']*100,2)}%"
            )

        return "\n".join(top_emotions)

    except Exception as e:
        return f"Emotion detection error: {e}"
