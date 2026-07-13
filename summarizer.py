from transformers import pipeline


# Load summarization model
summarizer_model = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)


def generate_summary(text):

    if not text:
        return "No text available"


    # Split long transcripts
    max_length = 1000

    chunks = [
        text[i:i+max_length]
        for i in range(0, len(text), max_length)
    ]


    summaries = []


    for chunk in chunks:

        result = summarizer_model(
            chunk,
            max_length=150,
            min_length=40,
            do_sample=False
        )

        summaries.append(
            result[0]["summary_text"]
        )


    return " ".join(summaries)
