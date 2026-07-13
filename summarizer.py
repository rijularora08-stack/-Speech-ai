
from transformers import pipeline


# Load summarization model
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)


def summarize_text(text):
    """
    Generate summary from transcript
    """

    if not text or len(text.strip()) == 0:
        return "No transcript available"

    try:
        # Split long transcripts
        max_length = 1024
        chunks = [
            text[i:i+max_length]
            for i in range(0, len(text), max_length)
        ]

        summaries = []

        for chunk in chunks:
            result = summarizer(
                chunk,
                max_length=150,
                min_length=40,
                do_sample=False
            )

            summaries.append(
                result[0]["summary_text"]
            )

        return "\n\n".join(summaries)

    except Exception as e:
        return f"Summarization error: {e}"
