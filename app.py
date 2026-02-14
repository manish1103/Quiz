from flask import Flask, render_template, request, redirect, url_for, session
import json, os

app = Flask(__name__)
app.secret_key = "quiz_secret_key_123"

# Load questions
with open("questions.json", "r", encoding="utf-8") as f:
    QUESTIONS_DATA = json.load(f)

# Leaderboard setup
if not os.path.exists("data"):
    os.makedirs("data")

LEADERBOARD_FILE = os.path.join("data", "leaderboard.json")

def save_score(username, score, category):
    data = []
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = []

    data.append({"username": username, "score": score, "category": category})

    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()  
        category = request.form.get("category", "")

        if not name or not category:
            return render_template(
                "index.html",
                categories=list(QUESTIONS_DATA.keys()),
                error="Please enter your name and select a category."
            )

        session["username"] = name
        session["category"] = category
        return redirect(url_for("quiz"))

    return render_template("index.html", categories=list(QUESTIONS_DATA.keys()))


@app.route("/quiz", methods=["GET"])
def quiz():
    category = session.get("category")
    username = session.get("username")
    if not category or not username:
        return redirect(url_for("index"))

    questions = QUESTIONS_DATA.get(category, [])
    return render_template("quiz.html", questions=questions, category=category, username=username)


@app.route("/submit", methods=["POST"])
def submit():
    category = session.get("category")
    username = session.get("username")
    if not category or not username:
        return redirect(url_for("index"))

    questions = QUESTIONS_DATA.get(category, [])
    score = 0
    results = []

    for i, q in enumerate(questions, start=1):
        form_key = f"q{i}"
        selected = request.form.get(form_key)
        correct_idx = int(q["answer"])

        if selected:
            try:
                sel_idx = int(selected)
            except:
                sel_idx = None
        else:
            sel_idx = None

        selected_text = (
            q["options"][sel_idx - 1] if sel_idx and 1 <= sel_idx <= len(q["options"]) else "Not Attempted"
        )
        correct_text = q["options"][correct_idx - 1]
        is_correct = (sel_idx == correct_idx)

        if is_correct:
            score += 1

        results.append({
            "question": q["question"],
            "selected_text": selected_text,
            "correct_text": correct_text,
            "is_correct": is_correct
        })

    save_score(username, score, category)

    session.pop("category", None)
    session.pop("username", None)

    return render_template(
        "result.html",
        name=username,
        score=score,
        total=len(questions),
        results=results
    )


@app.route("/restart")
def restart():
    session.pop("category", None)
    session.pop("username", None)
    return redirect(url_for("index"))


    
    if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

