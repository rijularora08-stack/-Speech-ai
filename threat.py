def detect_threats(text):

    if not text:
        return []

    keywords = [
        "kill",
        "attack",
        "bomb",
        "weapon",
        "harm",
        "suicide",
        "threat",
        "danger"
    ]

    results = []

    text_lower = text.lower()

    for word in keywords:

        if word in text_lower:
            results.append(
                {
                    "keyword": word,
                    "status": "Detected"
                }
            )

    return results
