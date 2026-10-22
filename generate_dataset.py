"""Creates a synthetic feedback.csv (500 rows). Run: python generate_dataset.py"""
import csv
import random
from datetime import date, timedelta
import os

random.seed(42)
DEPTS = {
    "Computer Science": ["Data Structures", "Machine Learning", "Database Systems", "Operating Systems"],
    "Electronics": ["Digital Circuits", "Signal Processing", "VLSI Design"],
    "Mechanical": ["Thermodynamics", "Fluid Mechanics", "CAD/CAM"],
    "Management": ["Marketing", "Financial Accounting", "Business Analytics"],
}
INSTR = ["Dr. Sharma", "Prof. Verma", "Dr. Iyer", "Prof. Khan", "Dr. Gupta", "Prof. Rao"]
POS = ["Explains concepts very clearly.", "Great practical examples and projects.", "The labs were well organised.",
       "Very supportive and approachable teacher.", "Course content is up to date and useful.", "Loved the interactive sessions."]
NEG = ["Lectures move too fast.", "Syllabus is outdated and boring.", "Lab equipment is poor and often broken.",
       "Too much theory, not enough practice.", "Assignments are confusing and feedback is slow.", "Classes are crowded and noisy."]
NEU = ["Course is okay overall.", "Some topics were good, others average.", "Decent teaching but could improve."]
def clip(x): return max(1, min(5, round(x)))
rows = []
for i in range(1, 501):
    dept = random.choice(list(DEPTS)); course = random.choice(DEPTS[dept]); ins = random.choice(INSTR)
    base = random.gauss(3.6, 0.9)
    r = [clip(base + random.gauss(0, 0.6)) for _ in range(4)]
    overall = clip(sum(r) / 4 + random.gauss(0, 0.3))
    pool = POS if overall >= 4 else NEG if overall <= 2 else NEU
    comment = " ".join(random.sample(pool, k=min(2, len(pool))))
    d = date(2025, 8, 1) + timedelta(days=random.randint(0, 420))
    rows.append([i, d.isoformat(), f"S{random.randint(1000, 1300)}", dept, course, ins,
                 random.choice(["Sem 1", "Sem 2", "Sem 3", "Sem 4"]), *r, overall, comment])
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feedback.csv")
with open(output_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["feedback_id", "date", "student_id", "department", "course", "instructor", "semester",
                "teaching_quality", "course_content", "lab_facilities", "support_staff", "overall_rating", "comment"])
    w.writerows(rows)
print("feedback.csv created:", len(rows), "rows")
