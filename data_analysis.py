import re
from collections import Counter
from data_cleaning import RATING_COLS

POSITIVE = {"good", "great", "clear", "clearly", "excellent", "helpful", "supportive", "approachable", "loved",
            "useful", "interactive", "organised", "practical", "best", "amazing", "engaging", "decent"}
NEGATIVE = {"poor", "boring", "outdated", "slow", "confusing", "broken", "crowded", "noisy", "bad", "late",
            "difficult", "fast", "worst", "average", "unclear", "improve"}
STOP = {"the", "a", "an", "and", "is", "are", "was", "were", "to", "of", "in", "on", "for", "but", "not", "too",
        "very", "some", "others", "overall", "course", "more", "than", "often", "much", "enough", "could", "it"}


def sentiment_label(text, rating):
    """Simple lexicon score; falls back to the rating when the text has no signal."""
    words = re.findall(r"[a-z']+", text.lower())
    score = sum(w in POSITIVE for w in words) - sum(w in NEGATIVE for w in words)
    if score == 0:
        score = 1 if rating >= 4 else -1 if rating <= 2 else 0
    return "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"


def summarize(df):
    df = df.copy()
    if df.empty:
        sentiments = {"Positive": 0, "Negative": 0, "Neutral": 0}
        return {
            "kpis": {"total": 0, "avg_rating": 0, "positive_pct": 0, "courses": 0},
            "categories": {c.replace("_", " ").title(): 0 for c in RATING_COLS[:-1]},
            "ratings": {str(rating): 0 for rating in range(1, 6)},
            "sentiment": sentiments,
            "monthly": {"labels": [], "values": []},
            "departments": {"labels": [], "values": []},
            "top_courses": {},
            "bottom_courses": {},
            "keywords": [],
            "recent": [],
        }

    df["sentiment"] = [sentiment_label(str(c), r) for c, r in zip(df["comment"], df["overall_rating"])]
    sent = df["sentiment"].value_counts()
    words = Counter(w for c in df["comment"] for w in re.findall(r"[a-z]{4,}", c.lower()) if w not in STOP)
    monthly = df.groupby(df["date"].dt.to_period("M"))["overall_rating"].mean().round(2)
    dept = df.groupby("department")["overall_rating"].mean().round(2).sort_values(ascending=False)
    course = df.groupby("course")["overall_rating"].mean().round(2).sort_values(ascending=False)
    recent = df.sort_values("date", ascending=False).head(10)
    return {
        "kpis": {
            "total": int(len(df)),
            "avg_rating": round(float(df["overall_rating"].mean()), 2),
            "positive_pct": round(100 * float(sent.get("Positive", 0)) / len(df), 1),
            "courses": int(df["course"].nunique()),
        },
        "categories": {c.replace("_", " ").title(): round(float(df[c].mean()), 2) for c in RATING_COLS[:-1]},
        "ratings": {str(rating): int(df["overall_rating"].round().eq(rating).sum()) for rating in range(1, 6)},
        "sentiment": {label: int(sent.get(label, 0)) for label in ("Positive", "Negative", "Neutral")},
        "monthly": {"labels": [str(p) for p in monthly.index], "values": monthly.tolist()},
        "departments": {"labels": dept.index.tolist(), "values": dept.tolist()},
        "top_courses": course.head(3).to_dict(),
        "bottom_courses": course.tail(3).to_dict(),
        "keywords": words.most_common(10),
        "recent": [{"date": r.date.strftime("%d %b %Y"), "course": r.course, "rating": int(r.overall_rating),
                    "sentiment": r.sentiment, "comment": r.comment} for r in recent.itertuples()],
    }
