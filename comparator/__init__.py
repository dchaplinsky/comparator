__version__ = "1.0.0"

__all__ = ["full_compare"]


import re
from functools import reduce
from itertools import permutations, product, islice, zip_longest
from operator import mul
from Levenshtein import jaro, jaro_winkler


def _smart_jaro(a, b, func=jaro):
    if func(a[1:], b[1:]) > 0.99:
        return True

    if func(a, b[1:]) > 0.99:
        return True

    if func(a[1:], b) > 0.99:
        return True

    chunk_distance = max([func(a, b)])
    if abs(len(a) - len(b)) >= 3:
        chunk_distance -= 0.2

    return chunk_distance


def _compare_two_names(
    name1, name2, max_splits=7, straight_limit=0.70, smart_limit=0.96
):

    straight_similarity = jaro(name1, name2)
    if straight_similarity > smart_limit:
        return True

    if straight_similarity > straight_limit:
        min_pair_distance = 1
        for a, b in zip_longest(name1.split(" "), name2.split(" ")):
            if a is not None and b is not None:
                chunk_distance = _smart_jaro(a, b, func=jaro_winkler)
                min_pair_distance = min(chunk_distance, min_pair_distance)

        if min_pair_distance > 0.88:
            return True

    return False


def _normalize_name(s):
    return (
        re.sub(r"\s+", " ", s.strip().replace("-", " "))
        .replace(".", "")
        .replace(",", "")
        .replace('"', "")
        .replace("'", "")
        .replace("’", "")
        .replace("є", "е")
        .replace("i", "и")
        .replace("і", "и")
        .replace("ь", "")
        .replace("'", "")
        .replace('"', "")
        .replace("`", "")
        .replace("конст", "кост")
        .replace("’", "")
        .replace("ʼ", "")
    )


def _slugify_name(s):
    s = s.replace(" ", "")

    return re.sub(r"\d+", "", s)


def _thorough_compare(name1, name2, max_splits=7):
    splits = name2.split(" ")
    limit = reduce(mul, range(1, max_splits + 1))

    for opt in islice(permutations(splits), limit):
        if _compare_two_names(name1, " ".join(opt)):
            return True

    return False


def full_compare(name1, name2):
    name1 = _normalize_name(name1)
    name2 = _normalize_name(name2)
    slugified_name1 = _slugify_name(name1)
    slugified_name2 = _slugify_name(name2)

    if slugified_name1 == slugified_name2:
        return True

    if slugified_name1.startswith(slugified_name2) and len(slugified_name2) >= 10:
        return True

    if slugified_name2.startswith(slugified_name1) and len(slugified_name1) >= 10:
        return True

    if slugified_name1.endswith(slugified_name2) and len(slugified_name2) >= 10:
        return True

    if slugified_name2.endswith(slugified_name1) and len(slugified_name1) >= 10:
        return True

    if jaro(slugified_name1, slugified_name2) > 0.95:
        return True

    if jaro(slugified_name2, slugified_name1) > 0.95:
        return True

    if _compare_two_names(name1, name2):
        return True

    if _compare_two_names(name2, name1):
        return True

    return _thorough_compare(name1, name2) or _thorough_compare(name2, name1)


def test_file(csv_file, debug):
    import csv
    from veryprettytable import VeryPrettyTable

    pt = VeryPrettyTable([" ", "Positive", "Negative"])

    with open(csv_file, "r") as fp:
        r = csv.DictReader(fp)

        res = {True: {True: 0, False: 0}, False: {True: 0, False: 0}}

        for l in r:
            expected = l["ground truth"].lower() in ["true", "1", "on"]
            predicted = full_compare(l["name1"], l["name2"])
            if predicted != expected and debug:
                print(predicted, expected, l["name1"], l["name2"])

            res[predicted][expected] += 1

    for predicted in [True, False]:
        pt.add_row(
            [
                "Predicted positive" if predicted else "Predicted negative",
                res[predicted][True],
                res[predicted][False],
            ]
        )

    precision = res[True][True] / (res[True][True] + res[True][False])
    recall = res[True][True] / (res[True][True] + res[False][True])
    f1 = 2 * precision * recall / (precision + recall)

    print(pt)

    print("Precision: {:5.2f}".format(precision))
    print("Recall: {:5.2f}".format(recall))
    print("F1 score: {:5.2f}".format(f1))


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        test_file(sys.argv[1], len(sys.argv) > 2)
    else:
        print(
            "Supply .csv file with ground truth data to calculate precision/recall/f1 metrics"
        )
