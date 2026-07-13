from transformers import pipeline


summarizer_model = None


def load_summarizer():

    global summarizer_model

    if summarizer_model is None:

        summarizer_model = pipeline(
            task="text2text-generation",
            model="google/flan-t5-small"
        )

    return summarizer_model



def generate_summary(text):

    if not text:
        return "No text available"


    model = load_summarizer()


    result = model(
        "Summarize this text: " + text[:2000],
        max_length=150,
        min_length=40,
        do_sample=False
    )


    return result[0]["generated_text"]
