# classifier.py
```python
from transformers import pipeline
from config import TOPIC_LABELS, THRESHOLD


def classify_articles(articles):
    """
    Zero-shot classify each article into one of TOPIC_LABELS,
    or 'Other' if below threshold. Returns: { label: [articles], 'Other': [...] }
    """
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    buckets = {label: [] for label in TOPIC_LABELS}
    buckets["Other"] = []

    for art in articles:
        text = f"{art['title']} {art['summary']}"
        result = classifier(text, TOPIC_LABELS)
        if result['scores'][0] >= THRESHOLD:
            chosen = result['labels'][0]
        else:
            chosen = 'Other'
        buckets[chosen].append(art)

    return buckets
