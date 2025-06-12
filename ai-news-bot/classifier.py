# classifier.py

from typing import List, Dict
from transformers import pipeline
from config import settings

def classify_articles(
    articles: List[Dict[str, str]]
) -> Dict[str, List[Dict[str, str]]]:
    """
    Zero‐shot classify each article into one of the configured topics,
    or into 'Other' if the top‐score is below the threshold.

    Args:
        articles: List of dicts with keys 'title', 'link', 'summary', 'published'.

    Returns:
        A dict mapping each topic label (and 'Other') to a list of article dicts.
    """
    # Initialize the zero‐shot classifier once
    classifier = pipeline(
        task="zero-shot-classification",
        model="facebook/bart-large-mnli"
    )

    # Prepare empty buckets for each label + an 'Other' bucket
    buckets: Dict[str, List[Dict[str, str]]] = {
        label: [] for label in settings.topic_labels
    }
    buckets["Other"] = []

    # Classify each article
    for art in articles:
        text = f"{art['title']} {art['summary']}"
        result = classifier(text, settings.topic_labels)

        top_score = result["scores"][0]
        top_label = result["labels"][0]

        # Assign to top label if above threshold; else "Other"
        if top_score >= settings.threshold:
            buckets[top_label].append(art)
        else:
            buckets["Other"].append(art)

    return buckets
