import csv
import os
from datetime import date
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
import pandas as pd
from data_cleaning import load_clean
from data_analysis import summarize

app = Flask(__name__)
app.secret_key = "change-me"
CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feedback.csv")
FIELDS = ["feedback_id", "date", "student_id", "department", "course", "instructor", "semester",
          "teaching_quality", "course_content", "lab_facilities", "support_staff", "overall_rating", "comment"]


@app.route("/")
def index():
    return render_template("index.html", s=summarize(load_clean(CSV)))


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", s=summarize(load_clean(CSV)))


@app.route("/api/summary")
def api_summary():
    return jsonify(summarize(load_clean(CSV)))


@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    df = load_clean(CSV)
    if request.method == "POST":
        f = request.form
        try:
            ratings = [int(f[k]) for k in FIELDS[7:12]]
        except (KeyError, ValueError):
            flash("Choose a rating from 1 to 5 for every category.", "error")
            return render_template("feedback.html", courses=sorted(df.course.unique())), 400
        if not all(1 <= rating <= 5 for rating in ratings):
            flash("Choose a rating from 1 to 5 for every category.", "error")
            return render_template("feedback.html", courses=sorted(df.course.unique())), 400
        raw_feedback_ids = pd.read_csv(CSV, usecols=["feedback_id"])["feedback_id"]
        feedback_ids = pd.to_numeric(raw_feedback_ids, errors="coerce")
        next_id = int(feedback_ids.max()) + 1 if feedback_ids.notna().any() else 1
        row = [next_id, date.today().isoformat(), f.get("student_id", "").strip(),
               f.get("department", "").strip(), f.get("course", "").strip(), f.get("instructor", "").strip(),
               f.get("semester", "").strip(), *ratings, f.get("comment", "").strip()]
        with open(CSV, "a", newline="", encoding="utf-8") as fh:
            csv.writer(fh).writerow(row)
        flash("Thanks, your feedback was saved.", "ok")
        return redirect(url_for("feedback"))
    return render_template("feedback.html", courses=sorted(df.course.unique()))


if __name__ == "__main__":
    app.run(debug=True)
