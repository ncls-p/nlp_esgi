import pandas as pd
import re


def make_dataset(filename):
    return pd.read_json(filename, lines=True)


def parse_presto_labels(sentence, target):
    words = re.findall(r"[\w\u0900-\u097F]+|[^\w\s]", sentence)

    task = target.split("(")[0].strip()

    labels_dict = {}
    for label, value in re.findall(
        r"(\w+)\s«\s([\w\s;.,!?()]+)\s»", target.split("(")[1].split(")")[0].strip()
    ):
        labels_dict[value.strip()] = label

    labels = [labels_dict.get(word.strip(), 0) for word in words]

    return {
        "sentence": sentence,
        "words": words,
        "labels": labels,
        "task": task,
    }


def get_presto_labels(filename):
    df = make_dataset(filename)
    labels = set()

    for target in df["target"]:
        task = target.split("(")[0].strip()
        labels.add(task)

        for label, _ in re.findall(
            r"(\w+)\s«\s([\w\s;.,!?()]+)\s»", target.split("(")[1].split(")")[0].strip()
        ):
            labels.add(label)

    return sorted(list(labels))
