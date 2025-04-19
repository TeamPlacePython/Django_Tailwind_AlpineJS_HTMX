import re
from itertools import groupby


def extract_number(category):
    match = re.search(r"M-(\d+)", category.name if category else "")
    return int(match[1]) if match else float("inf")


def group_results_by_event_and_category(results):
    """
    Prend une liste ou queryset de Result,
    et retourne une liste groupée par event et catégorie.
    """
    # ⚠️ Ici on trie avec des champs comparables
    results = sorted(
        results,
        key=lambda r: (
            r.event.id,
            r.member.sports_category.id if r.member.sports_category else 0,
        ),
    )

    grouped_results = []
    grouped_results.extend(
        {
            "event_title": event.title,
            "event_date": event.date,
            "sports_category": category.name if category else "Inconnu",
            "sort_key": (
                -event.date.timestamp(),
                extract_number(category),
            ),
            "members": list(group),
        }
        for (event, category), group in groupby(
            results, key=lambda r: (r.event, r.member.sports_category)
        )
    )
    grouped_results.sort(key=lambda x: x["sort_key"])
    return grouped_results
