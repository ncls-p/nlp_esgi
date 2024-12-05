import re

import pandas as pd


def make_dataset(filename):
    return pd.read_json(filename, lines=True)


def parse_presto_labels(sentence, target):
    words = parse_words(sentence)
    task = parse_task(target)
    labels = parse_labels(words, target)

    return {
        "sentence": sentence,
        "words": words,
        "labels": labels,
        "task": task,
    }


def parse_words(sentence):
    return re.findall(r"[\w\u0900-\u097F]+|[^\w\s]", sentence)


def parse_task(target):
    return target.split("(")[0].strip()


def parse_labels(words, target):
    labels = [0] * len(words)

    if "(" in target and ")" in target:
        pairs_text = target.split("(")[1].split(")")[0].strip()
        if pairs_text:
            for label, value in re.findall(
                r"(\w+)\s«\s([\w\s;.,!?()]+)\s»", pairs_text
            ):
                value = value.strip()
                value_words = value.split()

                for i in range(len(words)):
                    if i + len(value_words) <= len(words):
                        if (
                            " ".join(words[i : i + len(value_words)]).lower()
                            == value.lower()
                        ):
                            for j in range(len(value_words)):
                                labels[i + j] = label
                        elif words[i].lower() == value.lower():
                            labels[i] = label

    return labels


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
