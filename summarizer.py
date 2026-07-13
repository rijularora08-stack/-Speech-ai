from transformers import pipeline


summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)


def generate_summary(text):

    if not text:
        return "No transcript available"

    try:
        chunks = [
            text[i:i+1000]
            for i in range(0, len(text), 1000)
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
        return f"Summary error: {e}"
