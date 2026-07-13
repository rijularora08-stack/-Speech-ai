import json
import os


HISTORY_FILE = "history.json"


def save_history(record):

    history = load_history()

    history.append(record)

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            history,
            f,
            indent=4,
            ensure_ascii=False
        )


def load_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)

    except Exception:
        return []
