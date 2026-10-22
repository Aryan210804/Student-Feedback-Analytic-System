import pandas as pd
import re

RATING_COLS = ["teaching_quality", "course_content", "lab_facilities", "support_staff", "overall_rating"]
TEXT_COLS = ["student_id", "department", "course", "instructor", "semester", "comment"]


def load_clean(path="feedback.csv"):
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = [re.sub(r"\s+", "_", str(column).strip().lower()) for column in df.columns]
    if "feedback_id" in df.columns:
        df = df.drop_duplicates(subset="feedback_id")
    else:
        df = df.drop_duplicates()
    for c in RATING_COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce").clip(1, 5)
        median = df[c].median()
        df[c] = df[c].fillna(median if pd.notna(median) else 3)
    for c in TEXT_COLS:
        df[c] = df[c].fillna("").astype(str).str.replace(r"\s+", " ", regex=True).str.strip()
    df["department"] = df["department"].str.title()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df.dropna(subset=["date"]).reset_index(drop=True)
